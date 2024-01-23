from transformers import T5Tokenizer, T5ForConditionalGeneration
import requests
from bs4 import BeautifulSoup


def extract_text_from_url(url: str) -> str:
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    paragraphs = soup.find_all("p")
    text = " ".join([p.get_text() for p in paragraphs])
    return text


def summerize_text(input_text: str) -> str:
    # Load pre-trained T5 model and tokenizer
    # google/pegasus-cnn_dailymail
    # t5-small
    model_name = "t5-small"
    tokenizer = T5Tokenizer.from_pretrained(model_name)
    model = T5ForConditionalGeneration.from_pretrained(model_name)
    # Tokenize and summarize the input text using T5
    inputs = tokenizer.encode("summarize: " + input_text, return_tensors="pt", max_length=1024, truncation=True)
    summary_ids = model.generate(inputs, max_length=150, min_length=50, length_penalty=2.0, num_beams=4,
                                 early_stopping=True)

    # Decode and output the summary
    summary = tokenizer.decode(summary_ids [0], skip_special_tokens=True)
    return summary
