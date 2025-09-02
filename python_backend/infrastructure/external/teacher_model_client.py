"""
Teacher Model Client implementation.
Giao tiếp với external teacher models (OpenAI, DeepSeek, etc.)
"""

import asyncio
import time
from typing import Any, Dict, List, Optional

import aiohttp

from core.domain.entities import TeacherLabel
from core.domain.interfaces import MetricsServiceInterface, TeacherModelClientInterface


class MockTeacherModelClient(TeacherModelClientInterface):
    """
    Mock teacher model client cho testing và development.
    Simulate realistic API behavior với configurable delays và error rates.
    """

    def __init__(
        self,
        simulate_delay_ms: float = 100,
        error_rate: float = 0.05,
        metrics: Optional[MetricsServiceInterface] = None
    ):
        self.simulate_delay_ms = simulate_delay_ms
        self.error_rate = error_rate
        self.metrics = metrics
        self._call_count = 0

        # Mock responses cho different input patterns
        self._mock_responses = {
            "positive": ["positive", "good", "excellent", "great"],
            "negative": ["negative", "bad", "poor", "terrible"],
            "neutral": ["neutral", "okay", "average", "normal"],
            "question": ["question", "inquiry", "ask", "help"],
        }

    async def generate_label(self, input_text: str, model_config: Optional[Dict[str, Any]] = None) -> TeacherLabel:
        """Generate label từ mock teacher model"""
        start_time = time.time()
        self._call_count += 1

        if self.metrics:
            self.metrics.increment_counter("teacher_model_requests", {"client": "mock"})

        # Simulate network delay
        await asyncio.sleep(self.simulate_delay_ms / 1000)

        # Simulate errors
        if self._call_count % int(1 / max(self.error_rate, 0.001)) == 0:
            if self.metrics:
                self.metrics.increment_counter("teacher_model_errors", {"client": "mock", "type": "simulated"})
            raise RuntimeError("Simulated teacher model error")

        # Generate mock prediction based on input
        predicted_label, confidence = self._generate_mock_prediction(input_text)

        processing_time_ms = (time.time() - start_time) * 1000

        label = TeacherLabel(
            input_text=input_text,
            predicted_label=predicted_label,
            confidence_score=confidence,
            model_name="mock_teacher_v1",
            model_version="1.0.0",
            processing_time_ms=processing_time_ms,
            metadata={
                "mock": True,
                "call_count": self._call_count,
                **(model_config or {})
            }
        )

        if self.metrics:
            self.metrics.increment_counter("teacher_model_responses", {
                "client": "mock",
                "confidence": label.confidence_level.value
            })
            self.metrics.record_histogram("teacher_model_response_time_ms", processing_time_ms)

        return label

    def _generate_mock_prediction(self, input_text: str) -> tuple[str, float]:
        """Generate mock prediction based on input content"""
        text_lower = input_text.lower()

        # Determine label based on keywords
        if any(word in text_lower for word in ["good", "great", "excellent", "amazing", "love", "best"]):
            return "positive", 0.85 + (hash(input_text) % 15) / 100  # 0.85-0.99
        elif any(word in text_lower for word in ["bad", "terrible", "awful", "hate", "worst"]):
            return "negative", 0.80 + (hash(input_text) % 20) / 100  # 0.80-0.99
        elif any(word in text_lower for word in ["?", "how", "what", "when", "where", "why"]):
            return "question", 0.75 + (hash(input_text) % 20) / 100  # 0.75-0.94
        else:
            # Neutral với lower confidence
            return "neutral", 0.50 + (hash(input_text) % 30) / 100  # 0.50-0.79

    async def batch_generate_labels(self, input_texts: List[str], model_config: Optional[Dict[str, Any]] = None) -> List[TeacherLabel]:
        """Batch generate labels từ mock teacher model"""
        if not input_texts:
            return []

        # Simulate batch processing với concurrent calls
        tasks = [self.generate_label(text, model_config) for text in input_texts]

        # Sử dụng semaphore để limit concurrent requests
        semaphore = asyncio.Semaphore(10)  # Max 10 concurrent requests

        async def _bounded_generate(text: str) -> TeacherLabel:
            async with semaphore:
                return await self.generate_label(text, model_config)

        results = await asyncio.gather(
            *[_bounded_generate(text) for text in input_texts],
            return_exceptions=True
        )

        # Filter out exceptions
        labels = [result for result in results if isinstance(result, TeacherLabel)]

        if self.metrics:
            self.metrics.increment_counter("teacher_model_batch_requests", {
                "client": "mock",
                "batch_size": str(len(input_texts)),
                "success_count": str(len(labels))
            })

        return labels

    async def health_check(self) -> bool:
        """Health check cho mock teacher model"""
        try:
            # Simulate quick health check
            await asyncio.sleep(0.01)

            # Mock occasional health check failures
            if self._call_count % 50 == 0:  # Fail every 50th health check
                return False

            if self.metrics:
                self.metrics.increment_counter("teacher_model_health_checks", {"client": "mock", "status": "healthy"})

            return True

        except Exception:
            if self.metrics:
                self.metrics.increment_counter("teacher_model_health_checks", {"client": "mock", "status": "unhealthy"})
            return False


class OpenAITeacherModelClient(TeacherModelClientInterface):
    """
    OpenAI API client cho teacher model.
    Sử dụng GPT models cho text classification.
    """

    def __init__(
        self,
        api_key: str,
        model_name: str = "gpt-3.5-turbo",
        base_url: str = "https://api.openai.com/v1",
        timeout_seconds: int = 30,
        metrics: Optional[MetricsServiceInterface] = None
    ):
        self.api_key = api_key
        self.model_name = model_name
        self.base_url = base_url
        self.timeout_seconds = timeout_seconds
        self.metrics = metrics

        # Default prompt template
        self.prompt_template = """
Classify the following text into one of these categories: positive, negative, neutral, question.
Return only the category name and a confidence score (0-1).

Text: {input_text}

Response format: category:confidence
Example: positive:0.85
"""

    async def generate_label(self, input_text: str, model_config: Optional[Dict[str, Any]] = None) -> TeacherLabel:
        """Generate label từ OpenAI API"""
        start_time = time.time()

        if self.metrics:
            self.metrics.increment_counter("teacher_model_requests", {"client": "openai"})

        try:
            # Prepare request
            config = model_config or {}
            prompt = config.get("prompt_template", self.prompt_template).format(input_text=input_text)

            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

            payload = {
                "model": config.get("model_name", self.model_name),
                "messages": [{"role": "user", "content": prompt}],
                "temperature": config.get("temperature", 0.3),
                "max_tokens": config.get("max_tokens", 100)
            }

            # Make API request
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=self.timeout_seconds)) as session:
                async with session.post(f"{self.base_url}/chat/completions", json=payload, headers=headers) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        raise RuntimeError(f"OpenAI API error {response.status}: {error_text}")

                    data = await response.json()

            # Parse response
            content = data["choices"][0]["message"]["content"].strip()
            predicted_label, confidence_score = self._parse_openai_response(content)

            processing_time_ms = (time.time() - start_time) * 1000

            label = TeacherLabel(
                input_text=input_text,
                predicted_label=predicted_label,
                confidence_score=confidence_score,
                model_name=self.model_name,
                model_version="openai_api",
                processing_time_ms=processing_time_ms,
                metadata={
                    "openai_response": content,
                    "usage": data.get("usage", {}),
                    **(model_config or {})
                }
            )

            if self.metrics:
                self.metrics.increment_counter("teacher_model_responses", {
                    "client": "openai",
                    "confidence": label.confidence_level.value
                })
                self.metrics.record_histogram("teacher_model_response_time_ms", processing_time_ms)

            return label

        except Exception as e:
            processing_time_ms = (time.time() - start_time) * 1000
            if self.metrics:
                self.metrics.increment_counter("teacher_model_errors", {
                    "client": "openai",
                    "type": type(e).__name__
                })
                self.metrics.record_histogram("teacher_model_error_time_ms", processing_time_ms)
            raise

    def _parse_openai_response(self, content: str) -> tuple[str, float]:
        """Parse OpenAI response để extract label và confidence"""
        try:
            # Expected format: "category:confidence"
            if ":" in content:
                parts = content.split(":")
                label = parts[0].strip().lower()
                confidence = float(parts[1].strip())
                return label, max(0.0, min(1.0, confidence))
            else:
                # Fallback: extract just the label
                label = content.strip().lower()
                return label, 0.7  # Default confidence

        except Exception:
            # Ultimate fallback
            return "unknown", 0.5

    async def batch_generate_labels(self, input_texts: List[str], model_config: Optional[Dict[str, Any]] = None) -> List[TeacherLabel]:
        """Batch generate labels (sequential for OpenAI rate limits)"""
        results = []

        for text in input_texts:
            try:
                label = await self.generate_label(text, model_config)
                results.append(label)
                # Small delay để respect rate limits
                await asyncio.sleep(0.1)
            except Exception:
                # Log error nhưng continue với remaining texts
                if self.metrics:
                    self.metrics.increment_counter("teacher_model_batch_errors", {"client": "openai"})
                continue

        return results

    async def health_check(self) -> bool:
        """Health check cho OpenAI API"""
        try:
            # Simple test request
            test_label = await self.generate_label("test", {"max_tokens": 10})
            return True

        except Exception:
            if self.metrics:
                self.metrics.increment_counter("teacher_model_health_checks", {"client": "openai", "status": "unhealthy"})
            return False


# Factory function
def create_teacher_model_client(
    client_type: str = "mock",
    config: Optional[Dict[str, Any]] = None,
    metrics: Optional[MetricsServiceInterface] = None
) -> TeacherModelClientInterface:
    """
    Factory function để tạo teacher model client.
    
    Args:
        client_type: "mock" hoặc "openai"
        config: Configuration dict
        metrics: Metrics service
        
    Returns:
        TeacherModelClientInterface implementation
    """
    config = config or {}

    if client_type.lower() == "openai":
        return OpenAITeacherModelClient(
            api_key=config.get("api_key", ""),
            model_name=config.get("model_name", "gpt-3.5-turbo"),
            base_url=config.get("base_url", "https://api.openai.com/v1"),
            timeout_seconds=config.get("timeout_seconds", 30),
            metrics=metrics
        )
    else:  # Default to mock
        return MockTeacherModelClient(
            simulate_delay_ms=config.get("simulate_delay_ms", 100),
            error_rate=config.get("error_rate", 0.05),
            metrics=metrics
        )
