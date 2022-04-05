#!/usr/bin/env python


from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import WordNetLemmatizer
 
lemmatizer = WordNetLemmatizer()

ps = PorterStemmer()

example_text = """"Driving a self driving car might not be fun for a professional driver, but for a lazy driver, a self driving car saves a lot of driving"""

words = word_tokenize(example_text)
for word in words:
    print(ps.stem(word))
    print(lemmatizer.lemmatize(word))
