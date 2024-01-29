from transformers import T5Tokenizer, T5ForConditionalGeneration
import requests
from bs4 import BeautifulSoup
from diffusers import StableDiffusionPipeline
import torch

URL = "https://en.wikipedia.org/wiki/Natural_language_processing"
IMAGE_NAME = "img_from_nlp"
DEVICE = 'mps'
MAX_NEWS_LENGTH = 4096
MAX_SUMMAR_LEN = 150
TRANSFORMERS_MODEL = "t5-small"
DIFFUSERS_MODEL = "runwayml/stable-diffusion-v1-5"


def extract_text_from_url(url: str) -> str:
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    paragraphs = soup.find_all("p")
    text = " ".join([p.get_text() for p in paragraphs])
    return text


def summarize_text(input_text: str) -> str:
    model_name = TRANSFORMERS_MODEL
    tokenizer = T5Tokenizer.from_pretrained(model_name)
    model = T5ForConditionalGeneration.from_pretrained(model_name)
    inputs = tokenizer.encode("summarize: " + input_text, return_tensors="pt", max_length=MAX_NEWS_LENGTH, truncation=True)
    summary_ids = model.generate(inputs, max_length=MAX_SUMMAR_LEN, min_length=50, length_penalty=2.0, num_beams=4,
                                 early_stopping=True)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary


def image_creator(prompt: str, neg_prompt: str, img_name: str) -> None:
    model_id = DIFFUSERS_MODEL
    pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
    pipe = pipe.to(DEVICE)

    image = pipe(prompt, negative_prompt=neg_prompt).images[0]
    image.save(f"{img_name}.png")


text_from_url = extract_text_from_url(URL)
summary = summarize_text(text_from_url)
neg_prompt = "nsfw, bad quality, bad anatomy, worst quality, low quality, low resolutions, extra fingers, " \
             "blur, blurry, ugly, wrongs proportions, watermark, image artifacts, lowres, ugly, jpeg artifacts, " \
             "deformed, noisy image"

image_creator(summary, neg_prompt, IMAGE_NAME)
