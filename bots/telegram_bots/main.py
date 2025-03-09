"""Example of the telegram bot"""

import telebot
import g4f
from transformers import T5Tokenizer, T5ForConditionalGeneration
import requests
from bs4 import BeautifulSoup


BOT_KEY = "API_TOKEN"
HELP_TEXT_MSG = '''
This Bot is using the Artificial Intelegence techonology and could summarize any URL or 
send and answer for any your question. For summarizing of the URL at the beginning of 
the message type "URL:" or "url:" or start your url from "http://" or "https://".
For getting the answer to any of your question just send the text of your question.
'''


bot = telebot.TeleBot(BOT_KEY)


def get_responce_from_ai(msg):
    responce = g4f.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[{'role': 'user', 'content': msg}],
    )
    return responce


def extract_text_from_url(url: str) -> str:
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    paragraphs = soup.find_all("p")
    text = " ".join([p.get_text() for p in paragraphs])
    return text


def summerize_text(input_text: str) -> str:
    model_name = "t5-small"
    tokenizer = T5Tokenizer.from_pretrained(model_name)
    model = T5ForConditionalGeneration.from_pretrained(model_name)
    inputs = tokenizer.encode("summarize: " + input_text, return_tensors="pt", max_length=1024, truncation=True)
    summary_ids = model.generate(inputs, max_length=150, min_length=50, length_penalty=2.0, num_beams=4,
                                 early_stopping=True)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary

@bot.message_handler(commands=['help'])
def start_message(message):
    bot.send_message(message.from_user.id, HELP_TEXT_MSG)

@bot.message_handler(func=lambda message: True)
def responce_text_message(message):
    rec_text = message.text
    bot_massage = "Hi From AI..."
    if rec_text[:4] in ("URL:", "url:"):
        input_text = extract_text_from_url(rec_text[4:])
        bot_massage = summerize_text(input_text)
    elif rec_text[:7] == "http://" or rec_text[:8] == "https://":
        input_text = extract_text_from_url(rec_text)
        bot_massage = summerize_text(input_text)
    else:
        bot_massage = get_responce_from_ai(rec_text)
    bot.reply_to(message, bot_massage)


bot.polling(none_stop=True, interval=0)
