"""


HuggingFace API Client.





Provides interface to HuggingFace models and datasets.


"""

import asyncio
import logging
import os
from datetime import UTC, datetime
from typing import Any

import httpx
import Exception
import RuntimeError
import all
import api_token
import base_url
import batch_size
import bool
import client
import context
import dict
import do_sample
import e
import exc
import float
import getattr
import i
import image_url
import inp
import int
import isinstance
import item
import len
import limit
import list
import max_length
import min_length
import model_id
import num_return_sequences
import options
import params
import prompt
import question
import range
import result
import search
import self
import str
import task
import temperature
import text
import timeout
import v
import x

logger = logging.getLogger(__name__)


class HuggingFaceClient:
    """Client for interacting with HuggingFace API."""

    def __init__(
        self,
        api_token: str | None = None,
        base_url: str = "https://api-inference.huggingface.co",
        timeout: int = 30,
    ):
        """


        Initialize HuggingFace client.





        Args:


            api_token: HuggingFace API token


            base_url: Base URL for HuggingFace API


            timeout: Request timeout in seconds


        """

        self.api_token = api_token or os.getenv("HUGGINGFACE_API_TOKEN")

        self.base_url = base_url.rstrip("/")

        self.timeout = timeout

        self.headers = {"Content-Type": "application/json", "User-Agent": "ZetaAI/1.0"}

        if self.api_token:
            self.headers["Authorization"] = f"Bearer {self.api_token}"

    async def query_model(
        self,
        model_id: str,
        inputs: str | dict[str, Any] | list[str],
        parameters: dict[str, Any] | None = None,
        options: dict[str, Any] | None = None,
    ) -> Any:
        """


        Query a HuggingFace model.





        Args:


            model_id: Model identifier on HuggingFace


            inputs: Input data for the model


            parameters: Model parameters


            options: Additional options





        Returns:


            Model response





        Raises:


            Exception: If API request fails


        """

        url = f"{self.base_url}/models/{model_id}"

        payload = {"inputs": inputs}

        if parameters:
            payload["parameters"] = parameters

        if options:
            payload["options"] = options

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.post(url, headers=self.headers, json=payload)

                response.raise_for_status()

                return response.json()

            except httpx.TimeoutException as exc:
                logger.error(f"Timeout querying HuggingFace model {model_id}")
                raise RuntimeError(f"Request timeout for model {model_id}") from exc

            except httpx.HTTPStatusError as exc:
                logger.error(f"HTTP error querying HuggingFace model {model_id}: {exc}")
                status_code = getattr(
                    getattr(exc, "response", None), "status_code", None
                )
                raise RuntimeError(f"API error: {status_code}") from exc

            except Exception as e:
                logger.error(f"Error querying HuggingFace model {model_id}: {e}")

                raise

    async def text_generation(
        self,
        model_id: str = "gpt2",
        prompt: str = "",
        max_length: int = 100,
        temperature: float = 0.7,
        num_return_sequences: int = 1,
        do_sample: bool = True,
    ) -> list[str]:
        """


        Generate text using a language model.





        Args:


            model_id: Model identifier


            prompt: Input prompt


            max_length: Maximum length of generated text


            temperature: Sampling temperature


            num_return_sequences: Number of sequences to generate


            do_sample: Whether to use sampling





        Returns:


            List of generated texts


        """

        parameters = {
            "max_length": max_length,
            "temperature": temperature,
            "num_return_sequences": num_return_sequences,
            "do_sample": do_sample,
            "return_full_text": False,
        }

        try:
            response = await self.query_model(
                model_id=model_id, inputs=prompt, parameters=parameters
            )

            if isinstance(response, list):
                items: list[str] = []
                for item in response:
                    if isinstance(item, dict):
                        items.append(item.get("generated_text", ""))
                    elif isinstance(item, str):
                        items.append(item)
                return items
            if isinstance(response, dict):
                return [response.get("generated_text", "")]
            if isinstance(response, str):
                return [response]
            return []

        except Exception as e:
            logger.error(f"Text generation failed: {e}")

            return []

    async def text_classification(
        self,
        model_id: str = "cardiffnlp/twitter-roberta-base-sentiment-latest",
        text: str = "",
    ) -> list[dict[str, Any]]:
        """


        Classify text using a classification model.





        Args:


            model_id: Classification model identifier


            text: Text to classify





        Returns:


            List of classification results with labels and scores


        """

        try:
            response = await self.query_model(model_id=model_id, inputs=text)

            if isinstance(response, list) and response:
                first = response[0]
                if isinstance(first, list):
                    return first  # type: ignore[return-value]
                if all(isinstance(x, dict) for x in response):
                    return response  # type: ignore[return-value]
                return []
            return []

        except Exception as e:
            logger.error(f"Text classification failed: {e}")

            return []

    async def question_answering(
        self,
        model_id: str = "distilbert-base-cased-distilled-squad",
        question: str = "",
        context: str = "",
    ) -> dict[str, Any]:
        """


        Answer questions based on context.





        Args:


            model_id: Question answering model identifier


            question: Question to answer


            context: Context containing the answer





        Returns:


            Answer with confidence score


        """

        inputs = {"question": question, "context": context}

        try:
            response = await self.query_model(model_id=model_id, inputs=inputs)

            if isinstance(response, dict):
                return {
                    "answer": response.get("answer", ""),
                    "score": response.get("score", 0.0),
                    "start": response.get("start", 0),
                    "end": response.get("end", 0),
                }
            # Some models may return a list with a dict
            if (
                isinstance(response, list)
                and response
                and isinstance(response[0], dict)
            ):
                first = response[0]
                return {
                    "answer": first.get("answer", ""),
                    "score": first.get("score", 0.0),
                    "start": first.get("start", 0),
                    "end": first.get("end", 0),
                }

            return {"answer": "", "score": 0.0, "start": 0, "end": 0}

        except Exception as e:
            logger.error(f"Question answering failed: {e}")

            return {"answer": "", "score": 0.0, "start": 0, "end": 0}

    async def text_summarization(
        self,
        model_id: str = "facebook/bart-large-cnn",
        text: str = "",
        max_length: int = 150,
        min_length: int = 30,
    ) -> str:
        """


        Summarize text using a summarization model.





        Args:


            model_id: Summarization model identifier


            text: Text to summarize


            max_length: Maximum summary length


            min_length: Minimum summary length





        Returns:


            Generated summary


        """

        parameters = {
            "max_length": max_length,
            "min_length": min_length,
            "do_sample": False,
        }

        try:
            response = await self.query_model(
                model_id=model_id, inputs=text, parameters=parameters
            )

            if (
                isinstance(response, list)
                and response
                and isinstance(response[0], dict)
            ):
                return response[0].get("summary_text", "")
            if isinstance(response, dict):
                return response.get("summary_text", "")
            return ""

        except Exception as e:
            logger.error(f"Text summarization failed: {e}")

            return ""

    async def feature_extraction(
        self, model_id: str = "sentence-transformers/all-MiniLM-L6-v2", text: str = ""
    ) -> list[float]:
        """


        Extract features/embeddings from text.





        Args:


            model_id: Feature extraction model identifier


            text: Text to extract features from





        Returns:


            Feature vector as list of floats


        """

        try:
            response = await self.query_model(
                model_id=model_id, inputs=text, options={"wait_for_model": True}
            )

            if isinstance(response, list) and response:
                first = response[0]
                if isinstance(first, list):
                    return [float(v) for v in first]
                if all(isinstance(x, (int, float)) for x in response):
                    return [float(v) for v in response]  # type: ignore[list-item]
            return []

        except Exception as e:
            logger.error(f"Feature extraction failed: {e}")

            return []

    async def image_classification(
        self, model_id: str = "google/vit-base-patch16-224", image_url: str = ""
    ) -> list[dict[str, Any]]:
        """


        Classify images using a vision model.





        Args:


            model_id: Image classification model identifier


            image_url: URL of the image to classify





        Returns:


            List of classification results with labels and scores


        """

        try:
            response = await self.query_model(model_id=model_id, inputs=image_url)

            return response if isinstance(response, list) else []

        except Exception as e:
            logger.error(f"Image classification failed: {e}")

            return []

    async def get_model_info(self, model_id: str) -> dict[str, Any]:
        """


        Get information about a specific model.





        Args:


            model_id: Model identifier





        Returns:


            Model information


        """

        url = f"https://huggingface.co/api/models/{model_id}"

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.get(url, headers=self.headers)

                response.raise_for_status()

                return response.json()

            except Exception as e:
                logger.error(f"Error getting model info for {model_id}: {e}")

                return {}

    async def list_models(
        self, search: str | None = None, task: str | None = None, limit: int = 20
    ) -> list[dict[str, Any]]:
        """


        List available models.





        Args:


            search: Search query


            task: Filter by task (e.g., 'text-generation', 'text-classification')


            limit: Maximum number of models to return





        Returns:


            List of model information


        """

        url = "https://huggingface.co/api/models"

        params: dict[str, Any] = {"limit": limit}

        if search:
            params["search"] = search

        if task:
            params["filter"] = task

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.get(url, params=params, headers=self.headers)

                response.raise_for_status()

                return response.json()

            except Exception as e:
                logger.error(f"Error listing models: {e}")

                return []

    async def check_model_status(self, model_id: str) -> dict[str, Any]:
        """


        Check if a model is loaded and ready.





        Args:


            model_id: Model identifier





        Returns:


            Model status information


        """

        try:
            # Send a simple query to check model status
            await self.query_model(
                model_id=model_id, inputs="test", options={"wait_for_model": False}
            )

            return {
                "model_id": model_id,
                "status": "ready",
                "loaded": True,
                "timestamp": datetime.now(UTC).isoformat(),
            }

        except Exception as e:
            return {
                "model_id": model_id,
                "status": "loading" if "loading" in str(e).lower() else "error",
                "loaded": False,
                "error": str(e),
                "timestamp": datetime.now(UTC).isoformat(),
            }

    async def batch_inference(
        self,
        model_id: str,
        inputs: list[str | dict[str, Any]],
        parameters: dict[str, Any] | None = None,
        batch_size: int = 10,
    ) -> list[dict[str, Any]]:
        """


        Run batch inference on multiple inputs.





        Args:


            model_id: Model identifier


            inputs: List of inputs to process


            parameters: Model parameters


            batch_size: Size of each batch





        Returns:


            List of results for each input


        """

        results = []

        for i in range(0, len(inputs), batch_size):
            batch = inputs[i : i + batch_size]

            try:
                # Process batch

                batch_results = await asyncio.gather(
                    *[self.query_model(model_id, inp, parameters) for inp in batch],
                    return_exceptions=True,
                )

                # Handle results and exceptions

                for result in batch_results:
                    if isinstance(result, Exception):
                        results.append({"error": str(result)})

                    else:
                        results.append(result)

                # Add delay between batches to avoid rate limiting

                if i + batch_size < len(inputs):
                    await asyncio.sleep(1)

            except Exception as e:
                logger.error(f"Batch inference failed: {e}")

                # Add error results for the entire batch

                results.extend([{"error": str(e)}] * len(batch))

        return results
