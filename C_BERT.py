# Install and import packages
import numpy as np
import time
from transformers import pipeline
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification, DistilBertTokenizer, \
    DistilBertForSequenceClassification


def run_BERT(df):
    start = time.time()
    # Set up the inference pipeline using a model from the 🤗 Hub
    sentiment_analysis = pipeline(model="finiteautomata/bertweet-base-sentiment-analysis")
    # Let's run the sentiment analysis on each tweet
    sentence = []
    score = []
    for content in df.msg.to_list():
        sentiment = sentiment_analysis(content)
        sentence.append(sentiment[0]['label'])
        score.append(sentiment[0]['score'])

    df['sentiment_score'] = np.array(score)
    df['bert_sentiment_labels'] = np.array(sentence)

    end = time.time()
    # total time taken
    time_waited = f"Runtime of the program is {(end - start) / 60} minutes or {(end - start)} seconds"

    return df


# Set device (CPU or GPU)
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


# Sentiment analysis using RoBERTa-base-sentiment model
def run_ROBERTA(df):
    tokenizer = AutoTokenizer.from_pretrained("roberta-base")
    model = AutoModelForSequenceClassification.from_pretrained("textattack/roberta-base-SST-2")

    tweets = df['msg2'].tolist()
    sentiments = []

    for tweet in tweets:
        inputs = tokenizer.encode_plus(tweet, add_special_tokens=True, return_tensors="pt", padding=True,
                                       truncation=True)
        input_ids = inputs["input_ids"].to(device)
        attention_mask = inputs["attention_mask"].to(device)

        with torch.no_grad():
            outputs = model(input_ids, attention_mask=attention_mask)

        logits = outputs.logits
        _, predicted_class = torch.max(logits, dim=1)
        sentiment_label = "POS" if predicted_class.item() == 1 else "NEG"
        sentiments.append(sentiment_label)

    df['roberta_sentiment_labels'] = sentiments

    return df


# Sentiment analysis using DistilBERT-base-uncased-finetuned-sst-2-english model
def run_DISTILBERT(df):
    model_name = "distilbert-base-uncased-finetuned-sst-2-english"
    tokenizer = DistilBertTokenizer.from_pretrained(model_name)
    model = DistilBertForSequenceClassification.from_pretrained(model_name)

    tweets = df['msg'].tolist()
    sentiments = []

    for tweet in tweets:
        inputs = tokenizer.encode_plus(tweet, add_special_tokens=True, return_tensors="pt", padding=True,
                                       truncation=True)
        input_ids = inputs["input_ids"].to(device)
        attention_mask = inputs["attention_mask"].to(device)

        with torch.no_grad():
            outputs = model(input_ids, attention_mask=attention_mask)

        logits = outputs.logits
        _, predicted_class = torch.max(logits, dim=1)
        sentiment_label = "POS" if predicted_class.item() == 1 else "NEG"
        sentiments.append(sentiment_label)

    df['distilbert_sentiment_labels'] = sentiments

    return df
