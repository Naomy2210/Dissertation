import tokenize

import pandas as pd
import re

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from langdetect import detect


def preprocessing_msg(df):
    # Remove '@' mentions
    df["msg"] = df["msg"].str.replace(r'@[A-Za-z0-9_]+', 'mention', regex=True)

    # Remove URLs
    df["msg"] = df["msg"].str.replace(r'http\S+|www\S+|https\S+', 'URL', regex=True)

    # Remove duplicates
    df.drop_duplicates(subset='msg', inplace=True)

    # Remove tweets not in English
    # Apply language detection to filter out non-English tweets
    df['language'] = df['msg'].apply(detect_language)
    df = df[df['language'] == 'en'].reset_index(drop=True)
    df = df.drop('language', axis=1)

    # Tokenize tweets using word_tokenize()
    df['Tokenized Tweet'] = df['msg'].apply(word_tokenize)

    # Remove stop words + lower
    stop_words = set(stopwords.words('english'))
    df['Filtered Tweet'] = df['Tokenized Tweet'].apply(
        lambda tokens: [token for token in tokens if token.lower() not in stop_words])

    # lemmatizer = WordNetLemmatizer()
    #df["msg2"] = ' '.join([lemmatizer.lemmatize(w) for w in df["Filtered Tweet"].split() if len(lemmatizer.lemmatize(w)) > 3])
    #df["msg2"] = df["Filtered Tweet"].str.replace(r'{\S+|}\S+', ' ', regex=True)
    df['msg2'] = [','.join(map(str, l)) for l in df['Filtered Tweet']]

    return df

def detect_language(text):
    try:
        lang = detect(text)
        return lang
    except:
        return None





'''
# Initialize tokenizer, lemmatizer, and stopwords

lemmatizer = WordNetLemmatizer()
stopwords = set(stopwords.words('english'))


def preprocess_tweet(tweet):
        # Tokenization
    tokens = tokenize.tokenize(tweet)

        # Handling Mentions and Hashtags
    tokens = [token if token[0] not in ['@', '#'] else token[1:] for token in tokens]

        # Removing URLs
    tokens = [token for token in tokens if not token.startswith('http')]

        # Removing Special Characters and Punctuation
    tokens = [token for token in tokens if token.isalpha()]

        # Removing Stop Words
    tokens = [token for token in tokens if token not in stopwords]

        # Lemmatization
    tokens = [lemmatizer.lemmatize(token) for token in tokens]

        # Join tokens back to form preprocessed tweet
    preprocessed_tweet = ' '.join(tokens)

    return preprocessed_tweet

    # Example DataFrame
df = pd.DataFrame({'msg': ["Great #weekend! Just chilling with @friend1 and @friend2. #RelaxationTime",
                               "Having a fantastic time at the beach! #Sunshine",
                               "Can't wait for the party tonight! #Excited"]})

    # Apply preprocessing to 'msg' column and store the result back into 'msg' column
#df['msg'] = df['msg'].apply(lambda x: preprocess_tweet(x))

df1 = preprocessing_msg(df)
    # Display the updated DataFrame
print(df1['msg2'])
'''


