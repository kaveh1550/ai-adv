# utils/text_processing.py
from hazm import Normalizer, WordTokenizer
from transformers import pipeline

# استفاده از Hazm برای پاکسازی متون
normalizer = Normalizer()
tokenizer = WordTokenizer()

# ParsBERT
nlp_parser = pipeline(task="fill-mask", model="persianbert/bert-base")

def clean_text(text):
    text = normalizer.normalize(text)  # پاکسازی نویز‌ها
    return text

def analyze_text_with_parsbert(text):
    response = nlp_parser(text)
    return response
