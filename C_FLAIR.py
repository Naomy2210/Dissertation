from flair.models import TextClassifier
from flair.data import Sentence
import numpy as np

def run_FLAIR(df):
    # Load the pre-trained sentiment classifier
    classifier = TextClassifier.load('en-sentiment')

    eng_snt_score=[]

    # Iterate over each tweet in the dataframe
    for content in df.msg.to_list():
        sentence = Sentence(content)

        # Predict the sentiment of the tweet
        classifier.predict(sentence)
        #sentiment_label = sentence.labels[0].value

        eng_snt_score.append(sentence.labels[0].value)

        # Add the sentiment label to the dataframe
        #df[index, 'flair_sentiment_labels'] = sentiment_label

    df['sentiment_score'] = np.array(eng_snt_score)


    i = 0

    flair_sentiment = [ ]

    while(i<len(df)):
        if ((df.iloc[i]['sentiment_score'] == 'POSITIVE')):
            flair_sentiment.append('POS')
            i = i+1
        elif ((df.iloc[i]['sentiment_score'] == 'NEGATIVE')):
            flair_sentiment.append('NEG')
            i = i+1
    df['flair_sentiment_labels'] = flair_sentiment

    # Remove the 'sentiment_score' column
    df = df.drop('sentiment_score', axis=1)

    return df