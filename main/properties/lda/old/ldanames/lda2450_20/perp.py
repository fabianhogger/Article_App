import gensim
import gensim.corpora as corpora
import pickle
from gensim import models
from gensim.models.coherencemodel import CoherenceModel

lda=gensim.models.ldamodel.LdaModel.load('model20')
corpus=0
with open('corpus20', 'rb') as f:
    corpus = pickle.load(f)
dict = corpora.Dictionary.load('model20.id2word')
#Calculate model Perplexity ,the lower the better
Perplexity=lda.log_perplexity(corpus)
#Calculate model u_mass Coherence
cm = CoherenceModel(model=lda, corpus=corpus, coherence='u_mass')
coherence = cm.get_coherence()  # get coherence value
print(Perplexity,coherence)
