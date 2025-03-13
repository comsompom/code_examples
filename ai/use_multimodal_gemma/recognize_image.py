# pylint: disable=E0401
# pylint: disable=W1514
"""
Example of using the Gemma multimodal model with image recognition
the source of the model here:
https://huggingface.co/blog/gemma3
"""
import torch
from transformers import AutoProcessor, Gemma3ForConditionalGeneration
from huggingface_hub import login


with open('hf_token', 'r') as token_file:
    hf_token = token_file.read()

login(token=hf_token)


CKPT = "google/gemma-3-4b-it"
model = Gemma3ForConditionalGeneration.from_pretrained(
    CKPT, device_map="auto", torch_dtype=torch.bfloat16,
)
processor = AutoProcessor.from_pretrained(CKPT)

messages = [
    {
        "role": "user",
        "content": [
            {"type": "image", "image": "../entropia_ai/pics/pic1.png"},
            {"type": "text", "text": "What is drawing on the picture?"}
        ]
    }
]
inputs = processor.apply_chat_template(
    messages, add_generation_prompt=True, tokenize=True,
    return_dict=True, return_tensors="pt"
).to(model.device)

input_len = inputs["input_ids"].shape[-1]

generation = model.generate(**inputs, max_new_tokens=100, do_sample=False)
generation = generation[0][input_len:]

decoded = processor.decode(generation, skip_special_tokens=True)
print(decoded)
