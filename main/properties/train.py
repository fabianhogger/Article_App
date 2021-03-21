import gensim
from nltk.corpus import stopwords
from sklearn.datasets import fetch_20newsgroups
import pickle
import re
from gensim.utils import simple_preprocess
import spacy
import gensim.corpora as corpora
#data cleaning
stop_words = stopwords.words('english')
nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])
def sent_to_words(sentences):
    for sentence in sentences:
        yield(gensim.utils.simple_preprocess(str(sentence), deacc=True))
class train_defs():

    def start(django_data):

        stop_words.extend(['from', 'subject', 're', 'edu', 'use'])
        #newsgroups_train = fetch_20newsgroups(subset='train')
        def check_latin(text):
            pattern = re.compile("^[a-zA-Z]+$")
            check=[]
            for i in range(len(text)):
                check=[]
                for char in text[i]:
                    if pattern.match(char):
                        check.append(1)
                    else:
                        check.append(0)
                print('Article number {} has {} percent latin characters'.format(i,(sum(check)/len(check))*100))
                if ((sum(check)/len(check))*100)<=3:
                    print(text[i])
        check_latin(django_data)
        data = django_data
        """
        data = [re.sub('\S*@\S*\s?', '', sent) for sent in data]
        data = [re.sub('\s+', ' ', sent) for sent in data]
        data = [re.sub("\'", "", sent) for sent in data]
        print('DATA AFTER FIRST PART  ',data)
        data_words = list(sent_to_words(data))
        #bigrams,trigrams
        bigram = gensim.models.Phrases(data_words, min_count=5, threshold=100)
        trigram = gensim.models.Phrases(bigram[data_words], threshold=100)
        bigram_mod = gensim.models.phrases.Phraser(bigram)
        trigram_mod = gensim.models.phrases.Phraser(trigram)
        def remove_stopwords(texts):
            return [[word for word in simple_preprocess(str(doc)) if word not in stop_words] for doc in texts]
        def make_bigrams(texts):
           return [bigram_mod[doc] for doc in texts]
        def make_trigrams(texts):
           [trigram_mod[bigram_mod[doc]] for doc in texts]
        def lemmatization(texts, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV']):
            texts_out = []
            for sent in texts:
                doc = nlp(" ".join(sent))
                texts_out.append([token.lemma_ for token in doc if token.pos_ in allowed_postags])
            return texts_out
        data_words_nostops =remove_stopwords(data_words)
        data_words_bigrams =make_bigrams(data_words_nostops)

        data_lemmatized = lemmatization(data_words_bigrams, allowed_postags=[
           'NOUN', 'ADJ', 'VERB', 'ADV'
        ])
        print('DATA AFTER lemmatization  ',data_lemmatized)
        diction = corpora.Dictionary(data_lemmatized)

        corpus = [diction.doc2bow(text) for text in data_lemmatized]
        #Create a model
        lda_model = gensim.models.ldamodel.LdaModel(
           corpus=corpus, id2word=diction, num_topics=1x`0, random_state=100,
           update_every=1, chunksize=100, passes=10, alpha='auto'
        )
        lda_model.save('model10')
        open_file = open('corpus10', "wb")
        pickle.dump(corpus, open_file)
        import pyLDAvis.gensim
        vis = pyLDAvis.gensim.prepare(lda_model, corpus, dictionary=diction)
        pyLDAvis.save_html(vis,'ldavis10.html')
        """
