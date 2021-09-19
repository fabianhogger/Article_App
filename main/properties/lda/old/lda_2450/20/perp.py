import gensim
import gensim.corpora as corpora
import pickle
from gensim import models
from gensim.models.coherencemodel import CoherenceModel

lda=gensim.models.ldamodel.LdaModel.load('model5_2450')
corpus=0
with open('corpus5_2450', 'rb') as f:
    corpus = pickle.load(f)
dict = corpora.Dictionary.load('model5_2450.id2word')
#Calculate model Perplexity ,the lower the better
Perplexity=lda.log_perplexity(corpus)
#Calculate model u_mass Coherence
cm = CoherenceModel(model=lda, corpus=corpus, coherence='u_mass')
coherence = cm.get_coherence()  # get coherence value
print(Perplexity,coherence)

def jensen_shannon_divergence(repr1, repr2):
    """Calculates Jensen-Shannon divergence (https://en.wikipedia.org/wiki/Jensen%E2%80%93Shannon_divergence)."""
    avg_repr = 0.5 * (repr1 + repr2)
    sim = 1 - 0.5 * (scipy.stats.entropy(repr1, avg_repr) + scipy.stats.entropy(repr2, avg_repr))
    if np.isinf(sim):
        # the similarity is -inf if no term in the document is in the vocabulary
        return 0
    return sim
