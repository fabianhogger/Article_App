from nltk.corpus import stopwords
import spacy
import re
import gensim
from gensim.utils import simple_preprocess
import gensim.corpora as corpora
import pickle
from gensim import models, similarities

stop_words = stopwords.words('english')
nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])
def sent_to_words(sentences):
    for sentence in sentences:
        yield(gensim.utils.simple_preprocess(str(sentence), deacc=True))
class clean():
    def clean_text(text):
        data = text
        data = [re.sub('\S*@\S*\s?', '', sent) for sent in data]
        data = [re.sub('\s+', ' ', sent) for sent in data]
        data = [re.sub("\'", "", sent) for sent in data]
        print('DATA AFTER FIRST PART  ',data)
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
        print('data_lemmatized',data_lemmatized)
        dict = corpora.Dictionary.load('properties/lda/lda_1835/lda_10_1835/modelall.id2word')
        converted = [dict.doc2bow(text) for text in data_lemmatized]
        print('data ready ',converted)
        return converted

    def get_similarity(lda, query_vector):
        corpus=0
        with open('properties/lda/lda_1835/lda_10_1835/corpusall', 'rb') as f:
            corpus = pickle.load(f)
        index = similarities.MatrixSimilarity(lda[corpus])
        sims = index[query_vector]
        return sims
