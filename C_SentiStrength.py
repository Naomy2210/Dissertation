# Install and import packages
import numpy as np
from sentistrength import PySentiStr


def run_SentiStrength(df):
    # Initialize SentiStrength
    senti = PySentiStr()
    senti.setSentiStrengthPath('C:/Users/naomy/Downloads/SentiStrength.jar')
    senti.setSentiStrengthLanguageFolderPath('C:/Users/naomy/Downloads/SentStrength_Data')

    eng_snt_score = senti.getSentiment(df['msg'].to_list(), score='scale')
    df['sentiment_score'] = np.array(eng_snt_score)

    i = 0
    sentistrength_sentiment = []
    while i < len(df):
        if df.iloc[i]['sentiment_score'] > 0:
            sentistrength_sentiment.append('POS')
            i = i + 1
        elif df.iloc[i]['sentiment_score'] == 0:
            sentistrength_sentiment.append('NEU')
            i = i + 1
        elif df.iloc[i]['sentiment_score'] < 0.0:
            sentistrength_sentiment.append('NEG')
            i = i + 1
    df['sentistrength_sentiment_labels'] = np.array(sentistrength_sentiment)

    return df