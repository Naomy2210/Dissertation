# Install and import packages
import numpy as np
from nltk.sentiment.vader import SentimentIntensityAnalyzer

def run_VADER(df):
    eng_snt_score =[]

    for comment in df.msg.to_list():
        snts_score = calculate_sentiment_scores_VADER(comment)
        eng_snt_score.append(snts_score)

    df['sentiment_score'] = np.array(eng_snt_score)

    i = 0

    vader_sentiment = [ ]

    while(i<len(df)):
        if ((df.iloc[i]['sentiment_score'] >= 0.05)):
            vader_sentiment.append('POS')
            i = i+1
        elif ((df.iloc[i]['sentiment_score'] > -0.05) & (df.iloc[i]['sentiment_score'] < 0.05)):
            vader_sentiment.append('NEU')
            i = i+1
        elif ((df.iloc[i]['sentiment_score'] <= -0.05)):
            vader_sentiment.append('NEG')
            i = i+1
    df['vader_sentiment_labels'] = vader_sentiment

    return(df)


def calculate_sentiment_scores_VADER(sentence):
    analyzer = SentimentIntensityAnalyzer()
    sntmnt = analyzer.polarity_scores(sentence)['compound']
    return (sntmnt)