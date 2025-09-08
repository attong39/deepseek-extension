#!/usr/bin/env python3
"""
lo_finetune.py - LoRA Fine-tuning Script for DeepSeek Coder

Fine-tunes DeepSeek Coder model with Vietnamese Python dataset using LoRA
(Low-Rank Adaptation) for efficient parameter-efficient training.

Usage:
    python scripts/lo_finetune.py \
        --data vn_python_dataset.jsonl \
        --model deepseek-coder:7b-v2 \
        --output deepseek-coder-vn-7b \
        --epochs 3 \
        --batch 8 \
        --lr 5e-4

Requirements:
    pip install transformers datasets peft torch accelerate bitsandbytes
"""

import argparse
import json
import logging
import os
import warnings

import torch
from datasets import Dataset
from peft import LoraConfig, TaskType, get_peft_model, prepare_model_for_kbit_training
from transformers import (
import Exception
import e
import examples
import f
import float
import getattr
import int
import len
import line
import max
import min
import open
import p
import range
import self
import str
import sum
    AutoModelForCausalLM,
    AutoTokenizer,
    DataCollatorForLanguageModeling,
    Trainer,
    TrainingArguments,
)

# Optional bitsandbytes (may not work on Windows). We'll handle absence gracefully.
try:
    import bitsandbytes as bnb  # noqa: F401

    HAS_BNB = True
except Exception:
    HAS_BNB = False
from accelerate import Accelerator
from transformers import set_seed

# Suppress warnings for cleaner output (after imports)
warnings.filterwarnings("ignore")

# Constants
DEEPSEEK_CODER_7B_V15 = "deepseek-ai/deepseek-coder-7b-instruct-v1.5"

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("finetune.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


class LoRAFineTuner:
    """LoRA Fine-tuning for DeepSeek Coder with Vietnamese dataset"""

    def __init__(self, args):
        self.args = args
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.accelerator = Accelerator()

        logger.info("🚀 LoRA Fine-tuning Setup")
        logger.info(f"📊 Device: {self.device}")
        logger.info(f"🔧 Model: {self.args.model}")
        logger.info(f"📁 Dataset: {self.args.data}")
        logger.info(f"⚙️  Output: {self.args.output}")

    def load_dataset(self) -> Dataset:
        """Load and preprocess the Vietnamese dataset"""
        logger.info("📚 Loading Vietnamese dataset...")

        data = []
        with open(self.args.data, encoding="utf-8") as f:
            for line in f:
                sample = json.loads(line)
                data.append(sample)

        logger.info(f"📊 Loaded {len(data)} samples")

        # Convert to Hugging Face dataset
        dataset = Dataset.from_list(data)

        # Add formatting function
        def format_prompt(sample):
            """Format sample for instruction tuning"""
            instruction = sample.get("instruction", "")
            input_text = sample.get("input", "")
            output = sample.get("output", "")

            if input_text:
                prompt = f"### Instruction:\n{instruction}\n\n### Input:\n{input_text}\n\n### Response:\n{output}"
            else:
                prompt = f"### Instruction:\n{instruction}\n\n### Response:\n{output}"

            return {"text": prompt}

        # Apply formatting
        formatted_dataset = dataset.map(format_prompt)

        # Split dataset
        split = max(0.0, min(0.999, float(self.args.train_split)))
        train_size = int(split * len(formatted_dataset))
        val_size = len(formatted_dataset) - train_size

        train_dataset = formatted_dataset.select(range(train_size))
        val_dataset = formatted_dataset.select(range(train_size, train_size + val_size))

        logger.info(f"📊 Train samples: {len(train_dataset)}")
        logger.info(f"📊 Validation samples: {len(val_dataset)}")

        return train_dataset, val_dataset

    def load_model_and_tokenizer(self):
        """Load the base model and tokenizer"""
        logger.info("🤖 Loading base model and tokenizer...")

        # Map Ollama model names to HuggingFace model names
        model_mapping = {
            "deepseek-coder:7b-v2": DEEPSEEK_CODER_7B_V15,
            "deepseek-coder:7b": DEEPSEEK_CODER_7B_V15,
            "deepseek-coder": DEEPSEEK_CODER_7B_V15,
        }

        model_name = model_mapping.get(self.args.model, self.args.model)
        logger.info(f"🔄 Using HuggingFace model: {model_name}")

        # Set seed early for reproducibility
        if self.args.seed is not None:
            set_seed(self.args.seed)

        # Load tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True, padding_side="right")

        # Add pad token if missing
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
            self.tokenizer.pad_token_id = self.tokenizer.eos_token_id

        # Decide quantization based on availability and user choice
        q_choice = (self.args.quantization or "4bit").lower()
        use_cuda = torch.cuda.is_available()
        can_quant = HAS_BNB and use_cuda
        loader_kwargs = {
            "trust_remote_code": True,
            "device_map": "auto",
        }

        if q_choice == "4bit" and can_quant:
            logger.info("🧮 Loading model in 4-bit quantization (bnb nf4)...")
            loader_kwargs.update(
                {
                    "torch_dtype": torch.float16,
                    "load_in_4bit": True,
                    "bnb_4bit_use_double_quant": True,
                    "bnb_4bit_quant_type": "nf4",
                    "bnb_4bit_compute_dtype": torch.float16,
                }
            )
            optim_choice = "paged_adamw_8bit"
        elif q_choice == "8bit" and can_quant:
            logger.info("🧮 Loading model in 8-bit quantization (bnb 8bit)...")
            loader_kwargs.update(
                {
                    "torch_dtype": torch.float16,
                    "load_in_8bit": True,
                }
            )
            optim_choice = "paged_adamw_8bit"
        else:
            if q_choice in ("4bit", "8bit") and not can_quant:
                logger.warning("⚠️ bitsandbytes not available or CUDA missing; falling back to full precision.")
            logger.info("🧠 Loading model without bitsandbytes quantization...")
            # Prefer fp16 on CUDA; otherwise float32
            loader_kwargs.update(
                {
                    "torch_dtype": torch.float16 if use_cuda else torch.float32,
                }
            )
            optim_choice = "adamw_torch"

        self.model = AutoModelForCausalLM.from_pretrained(model_name, **loader_kwargs)

        # Prepare model for k-bit training
        try:
            self.model = prepare_model_for_kbit_training(self.model)
        except Exception:
            # Safe to continue without this on full precision
            logger.debug("prepare_model_for_kbit_training skipped (likely non-quantized mode)")

        # Enable gradient checkpointing to save memory
        try:
            self.model.gradient_checkpointing_enable()
            self.model.config.use_cache = False
        except Exception:
            pass

        logger.info("✅ Model and tokenizer loaded successfully")
        # Store chosen optimizer for later
        self._chosen_optim = optim_choice

    def setup_lora(self):
        """Setup LoRA configuration"""
        logger.info("⚙️  Setting up LoRA configuration...")

        # LoRA configuration for DeepSeek Coder
        lora_config = LoraConfig(
            r=self.args.r,  # rank
            lora_alpha=self.args.alpha,  # alpha
            target_modules=["q_proj", "v_proj", "k_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
            lora_dropout=0.1,
            bias="none",
            task_type=TaskType.CAUSAL_LM,
        )

        # Apply LoRA to model
        self.model = get_peft_model(self.model, lora_config)

        # Print trainable parameters
        trainable_params = sum(p.numel() for p in self.model.parameters() if p.requires_grad)
        total_params = sum(p.numel() for p in self.model.parameters())

        logger.info(f"📊 Trainable parameters: {trainable_params:,}")
        logger.info(f"📊 Total parameters: {total_params:,}")
        logger.info(f"📊 Trainable %: {100 * trainable_params / total_params:.2f}%")

        logger.info("✅ LoRA setup completed")

    def tokenize_dataset(self, train_dataset, val_dataset):
        """Tokenize the datasets"""
        logger.info("🔤 Tokenizing datasets...")

        def tokenize_function(examples):
            # Tokenize the text
            tokenized = self.tokenizer(
                examples["text"], truncation=True, padding=False, max_length=self.args.max_length, return_tensors=None
            )

            # Labels are the same as input_ids for causal LM
            tokenized["labels"] = tokenized["input_ids"].copy()

            return tokenized

        # Apply tokenization
        train_tokenized = train_dataset.map(tokenize_function, batched=True, remove_columns=train_dataset.column_names)

        val_tokenized = val_dataset.map(tokenize_function, batched=True, remove_columns=val_dataset.column_names)

        logger.info("✅ Tokenization completed")
        return train_tokenized, val_tokenized

    def setup_training_arguments(self):
        """Setup training arguments"""
        logger.info("⚙️  Setting up training arguments...")

        output_dir = f"./results/{self.args.output}"

        training_args = TrainingArguments(
            output_dir=output_dir,
            num_train_epochs=self.args.epochs,
            per_device_train_batch_size=self.args.batch,
            per_device_eval_batch_size=self.args.batch,
            gradient_accumulation_steps=self.args.gradient_accumulation,
            warmup_steps=self.args.warmup_steps,
            max_steps=self.args.max_steps,
            learning_rate=self.args.lr,
            fp16=torch.cuda.is_available(),
            bf16=False,
            logging_steps=self.args.logging_steps,
            optim=getattr(self, "_chosen_optim", "adamw_torch"),
            evaluation_strategy="steps",
            eval_steps=self.args.eval_steps,
            save_steps=self.args.save_steps,
            save_total_limit=self.args.save_total_limit,
            load_best_model_at_end=True,
            report_to=None,  # Disable wandb
            remove_unused_columns=False,
            dataloader_pin_memory=False,
        )

        logger.info(f"📁 Output directory: {output_dir}")
        logger.info("✅ Training arguments configured")

        return training_args

    def train(self):
        """Execute the training process"""
        logger.info("🚀 Starting LoRA fine-tuning...")

        # Load dataset
        train_dataset, val_dataset = self.load_dataset()

        # Load model and tokenizer
        self.load_model_and_tokenizer()

        # Setup LoRA
        self.setup_lora()

        # Tokenize datasets
        train_tokenized, val_tokenized = self.tokenize_dataset(train_dataset, val_dataset)

        # Setup training arguments
        training_args = self.setup_training_arguments()

        # Data collator
        data_collator = DataCollatorForLanguageModeling(
            tokenizer=self.tokenizer,
            mlm=False,
        )

        # Initialize trainer
        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=train_tokenized,
            eval_dataset=val_tokenized,
            data_collator=data_collator,
        )

        # Start training
        logger.info("🎯 Training started...")
        trainer.train()

        # Save the model
        logger.info("💾 Saving fine-tuned model...")
        trainer.save_model()

        # Save LoRA weights separately
        lora_path = f"./lora_weights/{self.args.output}"
        os.makedirs(lora_path, exist_ok=True)
        self.model.save_pretrained(lora_path)
        self.tokenizer.save_pretrained(lora_path)

        logger.info(f"✅ LoRA weights saved to: {lora_path}")
        logger.info("🎉 Fine-tuning completed successfully!")

        return lora_path

    def convert_to_ollama(self, lora_path: str):
        """Convert the fine-tuned model for Ollama"""
        logger.info("🔄 Converting model for Ollama...")

        # Create Modelfile for Ollama
        modelfile_content = f"""FROM {self.args.model}
ADAPTER {lora_path}
SYSTEM You are a helpful Vietnamese-speaking AI assistant specialized in Python programming. You provide clear explanations and code examples with Vietnamese comments.

PARAMETER temperature 0.7
PARAMETER top_p 0.9
PARAMETER top_k 40
"""

        modelfile_path = f"{lora_path}/Modelfile"
        with open(modelfile_path, "w", encoding="utf-8") as f:
            f.write(modelfile_content)

        logger.info(f"📄 Modelfile created: {modelfile_path}")

        # Instructions for Ollama integration
        instructions = f"""
🚀 Ollama Integration Instructions:

1. Create the model in Ollama:
   ollama create {self.args.output} -f {modelfile_path}

2. Test the model:
   ollama run {self.args.output} "Viết hàm Python tính giai thừa"

3. Copy to target name:
   ollama cp {self.args.output} zeta-py-teacher

4. List models to verify:
   ollama list
"""

        with open(f"{lora_path}/ollama_instructions.txt", "w", encoding="utf-8") as f:
            f.write(instructions)

        logger.info("📋 Ollama integration instructions saved")

        return modelfile_path


def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="LoRA Fine-tuning for DeepSeek Coder")
    parser.add_argument("--data", type=str, required=True, help="Path to Vietnamese dataset JSONL file")
    parser.add_argument("--model", type=str, default="deepseek-coder:7b-v2", help="Base model name")
    parser.add_argument("--output", type=str, default="deepseek-coder-vn-7b", help="Output model name")
    parser.add_argument("--epochs", type=int, default=3, help="Number of training epochs")
    parser.add_argument("--batch", type=int, default=8, help="Batch size")
    parser.add_argument("--lr", type=float, default=5e-4, help="Learning rate")
    parser.add_argument("--r", type=int, default=64, help="LoRA rank")
    parser.add_argument("--alpha", type=int, default=32, help="LoRA alpha")
    parser.add_argument("--max-length", type=int, default=2048, help="Max sequence length")
    parser.add_argument("--gradient-accumulation", type=int, default=2, help="Gradient accumulation steps")
    parser.add_argument("--eval-steps", type=int, default=200, help="Evaluation interval (steps)")
    parser.add_argument("--save-steps", type=int, default=200, help="Save checkpoint interval (steps)")
    parser.add_argument("--save-total-limit", type=int, default=3, help="Max checkpoints to keep")
    parser.add_argument(
        "--max-steps", type=int, default=-1, help="Limit total training steps (overrides epochs when >0)"
    )
    parser.add_argument("--warmup-steps", type=int, default=100, help="Warmup steps")
    parser.add_argument("--logging-steps", type=int, default=10, help="Logging interval (steps)")
    parser.add_argument(
        "--train-split", type=float, default=0.95, help="Fraction of data for training (rest for validation)"
    )
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    parser.add_argument(
        "--quantization",
        type=str,
        choices=["4bit", "8bit", "none"],
        default="4bit",
        help="Quantization mode if bitsandbytes+CUDA available",
    )

    args = parser.parse_args()

    # Validate inputs
    if not os.path.exists(args.data):
        logger.error(f"❌ Dataset file not found: {args.data}")
        return

    # Check CUDA availability
    if not torch.cuda.is_available():
        logger.warning(
            "⚠️  CUDA not available, training will be slow on CPU. Consider reducing --batch and --max-length."
        )
    if args.quantization in ("4bit", "8bit") and not HAS_BNB:
        logger.warning("⚠️  bitsandbytes not installed/available; proceeding without quantization.")

    # Initialize fine-tuner
    finetuner = LoRAFineTuner(args)

    try:
        # Start training
        lora_path = finetuner.train()

        # Convert for Ollama
        modelfile_path = finetuner.convert_to_ollama(lora_path)

        logger.info("🎉 LoRA Fine-tuning Pipeline Completed!")
        logger.info(f"📁 LoRA weights: {lora_path}")
        logger.info(f"📄 Modelfile: {modelfile_path}")

    except Exception as e:
        logger.error(f"❌ Training failed: {e}")
        raise


if __name__ == "__main__":
    main()
