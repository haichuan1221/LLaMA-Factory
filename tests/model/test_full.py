import os

import torch

from llamafactory.hparams import get_infer_args, get_train_args
from llamafactory.model import load_model, load_tokenizer


TINY_LLAMA = os.environ.get("TINY_LLAMA", "llamafactory/tiny-random-Llama-3")

TRAIN_ARGS = {
    "model_name_or_path": TINY_LLAMA,
    "stage": "sft",
    "do_train": True,
    "finetuning_type": "full",
    "dataset": "llamafactory/tiny-supervised-dataset",
    "dataset_dir": "ONLINE",
    "template": "llama3",
    "cutoff_len": 1024,
    "overwrite_cache": True,
    "output_dir": "dummy_dir",
    "overwrite_output_dir": True,
    "fp16": True,
}

INFER_ARGS = {
    "model_name_or_path": TINY_LLAMA,
    "finetuning_type": "full",
    "template": "llama3",
    "infer_dtype": "float16",
}


def test_full_train():
    model_args, _, _, finetuning_args, _ = get_train_args(TRAIN_ARGS)
    tokenizer_module = load_tokenizer(model_args)
    model = load_model(tokenizer_module["tokenizer"], model_args, finetuning_args, is_trainable=True)
    for param in model.parameters():
        assert param.requires_grad is True
        assert param.dtype == torch.float32


def test_full_inference():
    model_args, _, finetuning_args, _ = get_infer_args(INFER_ARGS)
    tokenizer_module = load_tokenizer(model_args)
    model = load_model(tokenizer_module["tokenizer"], model_args, finetuning_args, is_trainable=False)
    for param in model.parameters():
        assert param.requires_grad is False
        assert param.dtype == torch.float16
