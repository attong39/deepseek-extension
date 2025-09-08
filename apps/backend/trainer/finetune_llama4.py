"""Llama 4 Fine-tuning Service - QLoRA adapters cho student models.

Module này triển khai fine-tuning của Llama 4 (và variants)
sử dụng QLoRA để tạo adapters chuyên biệt.
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from pathlib import Path

import torch
import ImportError
import ValueError
import adapter_path
import bool
import config
import dataset_id
import dataset_path
import do_sample
import enumerate
import examples
import f
import float
import getattr
import i
import int
import k
import len
import list
import max_length
import open
import output_dir
import print
import prompt
import run_name
import self
import str
import temperature
import test_prompts
import tuple
import v
import zip

# Optional ML dependencies
try:
    from datasets import Dataset, load_from_disk

    ML_DATASETS_AVAILABLE = True
except ImportError:
    Dataset = None
    load_from_disk = None
    ML_DATASETS_AVAILABLE = False

try:
    from peft import LoraConfig, PeftModel, get_peft_model
    from transformers import (
        AutoModelForCausalLM,
        AutoTokenizer,
        BitsAndBytesConfig,
        DataCollatorForLanguageModeling,
        Trainer,
        TrainingArguments,
    )

    TRANSFORMERS_AVAILABLE = True
except ImportError:
    # Mock classes if not available
    LoraConfig = None
    get_peft_model = None
    PeftModel = None
    AutoModelForCausalLM = None
    AutoTokenizer = None
    BitsAndBytesConfig = None
    DataCollatorForLanguageModeling = None
    Trainer = None
    TrainingArguments = None
    TRANSFORMERS_AVAILABLE = False

from apps.backend.trainer.datasets.registry import DatasetStage, registry

logger = logging.getLogger(__name__)


@dataclass
class FineTuningConfig:
    """Cấu hình fine-tuning cho Llama models."""

    # Model settings
    base_model: str = "meta-llama/Llama-4-Scout"  # Hoặc Maverick
    model_max_length: int = 4096
    trust_remote_code: bool = True

    # LoRA settings
    lora_r: int = 16
    lora_alpha: int = 32
    lora_dropout: float = 0.1
    lora_target_modules: list[str] = None  # None = auto-detect

    # Quantization (QLoRA)
    load_in_4bit: bool = True
    bnb_4bit_compute_dtype: str = "float16"  # hoặc bfloat16
    bnb_4bit_quant_type: str = "nf4"
    bnb_4bit_use_double_quant: bool = True

    # Training hyperparameters
    learning_rate: float = 2e-4
    num_train_epochs: float = 1.0
    per_device_train_batch_size: int = 2
    per_device_eval_batch_size: int = 2
    gradient_accumulation_steps: int = 16
    warmup_steps: int = 100
    max_grad_norm: float = 1.0
    weight_decay: float = 0.01

    # Training behavior
    fp16: bool = False
    bf16: bool = True  # Tốt hơn cho training stability
    dataloader_num_workers: int = 4
    remove_unused_columns: bool = False

    # Logging & checkpointing
    logging_steps: int = 50
    save_steps: int = 1000
    eval_steps: int = 500
    save_total_limit: int = 3
    load_best_model_at_end: bool = True
    metric_for_best_model: str = "eval_loss"
    greater_is_better: bool = False

    # Output
    output_dir: str = "output/llama4-lora"
    run_name: str | None = None

    def __post_init__(self):
        """Set defaults sau khi init."""
        if self.lora_target_modules is None:
            # Common LoRA targets cho Llama architectures
            self.lora_target_modules = [
                "q_proj",
                "v_proj",
                "k_proj",
                "o_proj",
                "gate_proj",
                "up_proj",
                "down_proj",
            ]


class LlamaFineTuner:
    """Service fine-tune Llama models với QLoRA."""

    def __init__(self, config: FineTuningConfig | None = None):
        """Khởi tạo fine-tuner.

        Args:
            config: Cấu hình fine-tuning
        """
        self.config = config or FineTuningConfig()
        self.tokenizer: AutoTokenizer | None = None
        self.model: PeftModel | None = None

        # Validate CUDA availability
        if not torch.cuda.is_available():
            logger.warning("CUDA not available - fine-tuning sẽ rất chậm trên CPU")

    def prepare_model_and_tokenizer(self) -> tuple[PeftModel, AutoTokenizer]:
        """Load và prepare model + tokenizer với QLoRA config.

        Returns:
            Tuple (peft_model, tokenizer)
        """
        logger.info(f"Loading base model: {self.config.base_model}")

        # Load tokenizer
        tokenizer = AutoTokenizer.from_pretrained(
            self.config.base_model,
            trust_remote_code=self.config.trust_remote_code,
            model_max_length=self.config.model_max_length,
        )

        # Set pad token nếu chưa có
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token
            tokenizer.pad_token_id = tokenizer.eos_token_id

        # Quantization config for QLoRA
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=self.config.load_in_4bit,
            bnb_4bit_compute_dtype=getattr(torch, self.config.bnb_4bit_compute_dtype),
            bnb_4bit_quant_type=self.config.bnb_4bit_quant_type,
            bnb_4bit_use_double_quant=self.config.bnb_4bit_use_double_quant,
        )

        # Load base model
        base_model = AutoModelForCausalLM.from_pretrained(
            self.config.base_model,
            quantization_config=bnb_config,
            device_map="auto",  # Tự động distribute across GPUs
            trust_remote_code=self.config.trust_remote_code,
            torch_dtype=torch.float16,
        )

        # Prepare model for k-bit training
        base_model.gradient_checkpointing_enable()
        base_model = base_model.to(dtype=torch.float16)

        # LoRA config
        lora_config = LoraConfig(
            r=self.config.lora_r,
            lora_alpha=self.config.lora_alpha,
            target_modules=self.config.lora_target_modules,
            lora_dropout=self.config.lora_dropout,
            bias="none",
            task_type="CAUSAL_LM",
        )

        # Apply LoRA
        peft_model = get_peft_model(base_model, lora_config)
        peft_model.print_trainable_parameters()

        self.model = peft_model
        self.tokenizer = tokenizer

        return peft_model, tokenizer

    def prepare_dataset(self, dataset_path: str) -> tuple[Dataset, Dataset]:
        """Load và prepare dataset cho training.

        Args:
            dataset_path: Đường dẫn đến dataset (Huggingface format)

        Returns:
            Tuple (train_dataset, eval_dataset)
        """
        logger.info(f"Loading dataset from: {dataset_path}")

        # Load dataset
        if Path(dataset_path).is_dir():
            dataset = load_from_disk(dataset_path)
        else:
            raise ValueError(f"Dataset path not found: {dataset_path}")

        # Tokenize function
        def tokenize_function(examples):
            """Tokenize examples cho causal language modeling."""
            if self.tokenizer is None:
                raise ValueError("Tokenizer not initialized")

            # Format: prompt + response
            full_texts = []
            for prompt, response in zip(
                examples["prompt"], examples["response"], strict=False
            ):
                # Template có thể tuỳ chỉnh
                full_text = f"<|user|>\n{prompt}\n<|assistant|>\n{response}<|end|>"
                full_texts.append(full_text)

            # Tokenize
            tokenized = self.tokenizer(
                full_texts,
                truncation=True,
                padding=False,  # Padding sẽ làm trong data collator
                max_length=self.config.model_max_length,
                return_overflowing_tokens=False,
            )

            # Set labels = input_ids cho causal LM
            tokenized["labels"] = tokenized["input_ids"].copy()

            return tokenized

        # Apply tokenization
        tokenized_dataset = dataset.map(
            tokenize_function,
            batched=True,
            remove_columns=dataset["train"].column_names,
            desc="Tokenizing dataset",
        )

        train_dataset = tokenized_dataset["train"]
        eval_dataset = tokenized_dataset.get(
            "validation", tokenized_dataset.get("test")
        )

        # Nếu không có eval set, tách một phần từ train
        if eval_dataset is None:
            split = train_dataset.train_test_split(test_size=0.1, seed=42)
            train_dataset = split["train"]
            eval_dataset = split["test"]

        logger.info(
            f"Train samples: {len(train_dataset)}, Eval samples: {len(eval_dataset)}"
        )

        return train_dataset, eval_dataset

    def fine_tune(
        self,
        dataset_path: str,
        output_dir: str | None = None,
        run_name: str | None = None,
    ) -> str:
        """Thực hiện fine-tuning.

        Args:
            dataset_path: Đường dẫn dataset
            output_dir: Thư mục output (override config)
            run_name: Tên run (override config)

        Returns:
            Đường dẫn đến model đã train
        """
        # Override config if provided
        if output_dir:
            self.config.output_dir = output_dir
        if run_name:
            self.config.run_name = run_name

        # Prepare model và tokenizer
        model, tokenizer = self.prepare_model_and_tokenizer()

        # Prepare dataset
        train_dataset, eval_dataset = self.prepare_dataset(dataset_path)

        # Data collator
        data_collator = DataCollatorForLanguageModeling(
            tokenizer=tokenizer,
            mlm=False,  # Causal LM, không phải masked LM
        )

        # Training arguments
        training_args = TrainingArguments(
            output_dir=self.config.output_dir,
            num_train_epochs=self.config.num_train_epochs,
            per_device_train_batch_size=self.config.per_device_train_batch_size,
            per_device_eval_batch_size=self.config.per_device_eval_batch_size,
            gradient_accumulation_steps=self.config.gradient_accumulation_steps,
            learning_rate=self.config.learning_rate,
            warmup_steps=self.config.warmup_steps,
            max_grad_norm=self.config.max_grad_norm,
            weight_decay=self.config.weight_decay,
            fp16=self.config.fp16,
            bf16=self.config.bf16,
            logging_steps=self.config.logging_steps,
            eval_steps=self.config.eval_steps,
            save_steps=self.config.save_steps,
            save_total_limit=self.config.save_total_limit,
            load_best_model_at_end=self.config.load_best_model_at_end,
            metric_for_best_model=self.config.metric_for_best_model,
            greater_is_better=self.config.greater_is_better,
            dataloader_num_workers=self.config.dataloader_num_workers,
            remove_unused_columns=self.config.remove_unused_columns,
            run_name=self.config.run_name,
            report_to=None,  # Disable wandb/tensorboard by default
            evaluation_strategy="steps",
            save_strategy="steps",
        )

        # Trainer
        trainer = Trainer(
            model=model,
            args=training_args,
            train_dataset=train_dataset,
            eval_dataset=eval_dataset,
            data_collator=data_collator,
            tokenizer=tokenizer,
        )

        # Train
        logger.info("Starting fine-tuning...")
        trainer.train()

        # Save final model
        final_output_dir = Path(self.config.output_dir) / "final"
        trainer.save_model(str(final_output_dir))
        tokenizer.save_pretrained(str(final_output_dir))

        # Save training info
        training_info = {
            "base_model": self.config.base_model,
            "lora_config": {
                "r": self.config.lora_r,
                "alpha": self.config.lora_alpha,
                "target_modules": self.config.lora_target_modules,
                "dropout": self.config.lora_dropout,
            },
            "training_args": training_args.to_dict(),
            "final_eval_loss": trainer.state.log_history[-1].get("eval_loss", 0.0),
            "total_steps": trainer.state.global_step,
        }

        with open(final_output_dir / "training_info.json", "w") as f:
            json.dump(training_info, f, indent=2)

        logger.info(f"Fine-tuning complete. Model saved to: {final_output_dir}")
        return str(final_output_dir)

    def load_trained_model(self, adapter_path: str) -> tuple[PeftModel, AutoTokenizer]:
        """Load model đã được fine-tune.

        Args:
            adapter_path: Đường dẫn đến LoRA adapter

        Returns:
            Tuple (model, tokenizer)
        """
        logger.info(f"Loading trained model from: {adapter_path}")

        # Load tokenizer
        tokenizer = AutoTokenizer.from_pretrained(adapter_path)

        # Load base model
        base_model = AutoModelForCausalLM.from_pretrained(
            self.config.base_model,
            device_map="auto",
            torch_dtype=torch.float16,
        )

        # Load LoRA adapter
        model = PeftModel.from_pretrained(base_model, adapter_path)

        return model, tokenizer

    def generate_text(
        self,
        prompt: str,
        max_length: int = 512,
        temperature: float = 0.7,
        do_sample: bool = True,
    ) -> str:
        """Generate text với trained model.

        Args:
            prompt: Input prompt
            max_length: Độ dài tối đa
            temperature: Sampling temperature
            do_sample: Có dùng sampling không

        Returns:
            Generated text
        """
        if self.model is None or self.tokenizer is None:
            raise ValueError("Model chưa được load")

        # Format prompt
        formatted_prompt = f"<|user|>\n{prompt}\n<|assistant|>\n"

        # Tokenize
        inputs = self.tokenizer(formatted_prompt, return_tensors="pt")
        inputs = {k: v.to(self.model.device) for k, v in inputs.items()}

        # Generate
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_length=max_length,
                temperature=temperature,
                do_sample=do_sample,
                pad_token_id=self.tokenizer.eos_token_id,
            )

        # Decode
        generated = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

        # Extract response part
        if "<|assistant|>" in generated:
            response = generated.split("<|assistant|>")[-1].strip()
        else:
            response = generated

        return response


def fine_tune_from_dataset(
    dataset_id: str,
    output_dir: str = "output/llama4-lora",
    config: FineTuningConfig | None = None,
) -> str:
    """Convenience function để fine-tune từ dataset registry.

    Args:
        dataset_id: ID dataset trong registry
        output_dir: Thư mục output
        config: Config fine-tuning

    Returns:
        Đường dẫn model đã train
    """
    # Get dataset info
    dataset_lineage = registry.get_dataset(dataset_id)
    if not dataset_lineage:
        raise ValueError(f"Dataset {dataset_id} not found in registry")

    if dataset_lineage.stage != DatasetStage.LABELED:
        raise ValueError(
            f"Dataset {dataset_id} chưa ready cho training (stage: {dataset_lineage.stage})"
        )

    if not dataset_lineage.processed_path:
        raise ValueError(f"Dataset {dataset_id} không có processed_path")

    # Initialize fine-tuner
    tuner = LlamaFineTuner(config)

    # Fine-tune
    model_path = tuner.fine_tune(
        dataset_path=str(dataset_lineage.processed_path),
        output_dir=output_dir,
        run_name=f"finetune-{dataset_id}",
    )

    # Mark dataset as consumed
    registry.mark_used_in_training(dataset_id, f"finetune-{dataset_id}")

    return model_path


def load_and_test_model(adapter_path: str, test_prompts: list[str]) -> None:
    """Load model và test với vài prompts.

    Args:
        adapter_path: Đường dẫn LoRA adapter
        test_prompts: Danh sách prompts để test
    """
    tuner = LlamaFineTuner()
    model, tokenizer = tuner.load_trained_model(adapter_path)
    tuner.model = model
    tuner.tokenizer = tokenizer

    print(f"Model loaded from: {adapter_path}")
    print("Testing model with prompts:")
    print("=" * 50)

    for i, prompt in enumerate(test_prompts, 1):
        print(f"\nTest {i}: {prompt}")
        print("-" * 30)
        response = tuner.generate_text(prompt)
        print(response)
        print("=" * 50)
