# pylint: disable=E0401
"""Simple login code to hugging face hub"""
from huggingface_hub import login


with open('hf_token', 'r') as token_file:
    hf_token = token_file.read()

login(token=hf_token)
