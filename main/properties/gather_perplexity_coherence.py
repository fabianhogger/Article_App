
"""
import gensim
import gensim.corpora as corpora
import pickle
from gensim import models
from gensim.models.coherencemodel import CoherenceModel

models=['lda/1st_lda/model2','lda/lda10/model10','lda/lda20/model20','lda/lda_1835/lda_10_1835/modelall','lda/lda_1835/lda_20_1835/modelall20','lda/lda_1835/lda_5_2000/modelall5','lda/lda_2450/model5_2450']
dictio=['lda/1st_lda/model2.id2word','lda/lda10/model10.id2word','lda/lda20/model20.id2word','lda/lda_1835/lda_10_1835/modelall.id2word','lda/lda_1835/lda_20_1835/modelall20.id2word','lda/lda_1835/lda_5_2000/modelall5.id2word','lda/lda_2450/model5_2450.id2word']
corpi=['lda/1st_lda/corpus2','lda/lda10/corpus10','lda/lda20/corpus20','lda/lda_1835/lda_10_1835/corpusall','lda/lda_1835/lda_20_1835/corpusall20','lda/lda_1835/lda_5_2000/corpusall5','lda/lda_2450/corpus5_2450']

values=[]
for i in range(len(models)):
    lda=gensim.models.ldamodel.LdaModel.load(models[i])
    corpus=0
    with open(corpi[i], 'rb') as f:
        corpus = pickle.load(f)
    dict = corpora.Dictionary.load(dictio[i])
    #Calculate model Perplexity ,the lower the better
    Perplexity=lda.log_perplexity(corpus)
    #Calculate model u_mass Coherence
    cm = CoherenceModel(model=lda, corpus=corpus, coherence='u_mass')
    coherence = cm.get_coherence()  # get coherence value
    values.append((Perplexity,coherence))
    print("{} perplexity ,{} ,Coherence {}".format(models[i],Perplexity,coherence))

lda/1st_lda/model2 perplexity ,-8.10540112664753 ,Coherence -7.8969053885736855
lda/lda10/model10 perplexity ,-8.276172619100972 ,Coherence -9.365727403698168
lda/lda20/model20 perplexity ,-13.65181483862402 ,Coherence -8.04937166522311
lda/lda_1835/lda_10_1835/modelall perplexity ,-8.488547369183433 ,Coherence -5.99887252300144
lda/lda_1835/lda_20_1835/modelall20 perplexity ,-12.778878108732613 ,Coherence -8.67890479799749
lda/lda_1835/lda_5_2000/modelall5 perplexity ,-8.133472207050898 ,Coherence -20.23439969614912
model10_2450 perplexity ,-8.78581448964732 ,Coherence -19.537120724942845
model20_2450 -24.22308505078068 -17.72768807373683
"""
