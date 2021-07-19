import nltk
import re
import string
from tensorflow import keras
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
import pickle
import numpy as np

#Load Tokenizer
with open('properties/SentimentAnalysis/tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)
model=keras.models.load_model("properties/SentimentAnalysis/SentiModel")

#tokenizer=Tokenizer()
def clean_text(text):
    ps=nltk.PorterStemmer()
    stopwords=nltk.corpus.stopwords.words('english')
    text=''.join([char for char in text if char not in string.punctuation and not char.isdigit()])
    tokens=re.split('\W+',text)
    text=' '.join([ps.stem(word) for word in tokens if word not in stopwords])
    return text


def process_for_sentiment(sentences):
    sentences=[clean_text(sentence) for sentence in sentences]
    sequences=tokenizer.texts_to_sequences(sentences)#replaces the words with their indexes
    #Padding
    sequences_padded=pad_sequences(sequences,50)
    return sequences_padded



def get_sentiment(sentences):
    sequences=process_for_sentiment(sentences)
    #print(sequences)
    predictions=model.predict(sequences)
    #print(predictions)
    classes = (predictions>0.25)
    #print(classes)
    if sum(classes==True)>len(classes)/2:
        return 1
    else:
        return 0
