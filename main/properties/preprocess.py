from nltk.corpus import stopwords
import spacy
import re
import gensim
from gensim.utils import simple_preprocess
import gensim.corpora as corpora
import pickle
from gensim import models, similarities
import numpy as np
import scipy
stop_words = stopwords.words('english')
nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])
def jensen_shannon_distance(p, q):
    """
    method to compute the Jenson-Shannon Distance
    between two probability distributions
    """
    #print('REACHED')
    # convert the vectors into numpy arrays in case that they aren't
    p = np.array(p)
    q = np.array(q)
    if len(p)>len(q):
        dif=len(p)-len(q)
        arr=np.zeros(dif)
        q=np.append(q,arr)
    elif len(p)<len(q):
        dif=len(q)-len(p)
        arr=np.zeros(dif)
        p=np.append(p,arr)
    # calculate m
    m = (p + q) / 2
    #print('REACHED2')
    # compute Jensen Shannon Divergence
    divergence = (scipy.stats.entropy(p, m) + scipy.stats.entropy(q, m)) / 2
    # compute the Jensen Shannon Distance
    distance = np.sqrt(divergence)
    return distance
def sent_to_words(sentences):
    for sentence in sentences:
        yield(gensim.utils.simple_preprocess(str(sentence), deacc=True))
class clean():
    def clean_text(text):
        data = text
        data = [re.sub('\S*@\S*\s?', '', sent) for sent in data]
        data = [re.sub('\s+', ' ', sent) for sent in data]
        data = [re.sub("\'", "", sent) for sent in data]
        #print('DATA AFTER FIRST PART  ',data)
        data_words = list(sent_to_words(data))
        def remove_stopwords(texts):
            return [[word for word in simple_preprocess(str(doc)) if word not in stop_words] for doc in texts]
        def lemmatization(texts, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV']):
            texts_out = []
            for sent in texts:
                doc = nlp(" ".join(sent))
                texts_out.append([token.lemma_ for token in doc if token.pos_ in allowed_postags])
            return texts_out
        data_words_nostops =remove_stopwords(data_words)
        data_lemmatized = lemmatization(data_words_nostops, allowed_postags=[
           'NOUN', 'ADJ', 'VERB', 'ADV'
        ])
        #print('data_lemmatized',data_lemmatized)
        dict = corpora.Dictionary.load('properties/lda/lda_50_articles/model50bodies.id2word')
        converted = [dict.doc2bow(text) for text in data_lemmatized]
        #print('data ready ',converted)
        return converted

    def get_similarity(lda, query_vector):
        corpus=0
        with open('properties/lda/lda_15_articles_wlist/corpus15bodies', 'rb') as f:
            corpus = pickle.load(f)
        index = similarities.MatrixSimilarity(lda[corpus])
        sims = index[query_vector]
        return sims

    def get_jensen_shannon(lda,vector):
        corpus=0
        with open('properties/lda/lda_50_articles/corpus50bodies', 'rb') as f:
            corpus = pickle.load(f)
        vector=[item[1] for item in vector]
        print("VECTOR AFTER PROCESS")
        print(vector)
        vectors=lda[corpus]
        dists=[]
        for i in range(len(corpus)):
            next=[item[1] for item in vectors[i]]
            dists.append(jensen_shannon_distance(vector,next))
        #print(dists)
        return dists
