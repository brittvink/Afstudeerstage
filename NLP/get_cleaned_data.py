#!/usr/bin/env python
import pandas as pd
import nltk
from nltk.corpus import stopwords
import re
import string
import logging


def preprocess_text(text: str, remove_stopwords: bool) -> str:
    """This utility function sanitizes a string by:
    - removing links
    - removing special characters
    - removing numbers
    - removing stopwords
    - transforming in lowercase
    - removing excessive whitespaces
    Args:
        text (str): the input text you want to clean
        remove_stopwords (bool): whether or not to remove stopwords
    Returns:
        str: the cleaned text
    """

    # remove links
    text = re.sub(r"http\S+", "", text)
    # remove special chars and numbers
    text = re.sub('\[.*?\]', '', text)
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\w*\d\w*', '', text)
    text = re.sub('[‘’“”…]', '', text)
    text = re.sub('\n', '', text)
    
    # remove stopwords
    if remove_stopwords:
        # 1. tokenize
        tokens = nltk.word_tokenize(text)
        # 2. check if stopword
        tokens = [w for w in tokens if not w.lower() in stopwords.words("english")]
        # 3. join back together
        text = " ".join(tokens)
    # return text in lower case and stripped of whitespaces
    text = text.lower().strip()
    return text


df = pd.read_pickle("Information_joined.pkl")

logging.basicConfig(filename= "logfile_get_cleaned_data.log",
                            filemode='w',
                            format='%(asctime)s,%(msecs)d %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.DEBUG)

logging.info("df: " + str(df.shape) + "with columns" + df.columns)
logging.info("Column text has an avarage length of: " + str(df["text"].str.len().mean()))
logging.info("Column text has " + str(df["text"].str.len().sum()) + " words")
logging.info("Column text has quantiles " + str(df["text"].str.len().quantile([0.25, 0.5, 0.75])) + " words")
logging.info("Column text has minimal " + str(df["text"].str.len().min()) + " words")
logging.info("Column text has maximal " + str(df["text"].str.len().max()) + " words")

df['cleaned'] = df['text'].apply(lambda x: preprocess_text(x, remove_stopwords=True))

logging.info("df: " + str(df.shape) + "with columns" + df.columns)
logging.info("Column cleaned has an avarage length of: " + str(df["cleaned"].str.len().mean()))
logging.info("Column cleaned has " + str(df["cleaned"].str.len().sum()) + " words")
logging.info("Column cleaned has quantiles " + str(df["cleaned"].str.len().quantile([0.25, 0.5, 0.75])) + " words")
logging.info("Column cleaned has minimal " + str(df["cleaned"].str.len().min()) + " words")
logging.info("Column cleaned has maximal " + str(df["cleaned"].str.len().max()) + " words")

df.to_pickle("df_cleaned.pkl")