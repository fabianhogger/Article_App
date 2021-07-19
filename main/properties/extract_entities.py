import spacy
from spacy import displacy
from fuzzywuzzy import fuzz,process
import wikipedia
#wikipedia.set_rate_limiting(rate_limit=True, min_wait=datetime.timedelta(0, 0, 50000))
spacy.prefer_gpu()
nlp=spacy.load("en_core_web_sm")
def find_sents(doc,word):
    sentences=[]
    for sent in doc.sents:
        if word in str(sent):
            sentences.append(str(sent))
    return sentences
def get_wikipedia_url(candidate):
    try:
        article=wikipedia.page(title=candidate,redirect=True,auto_suggest=True,preload=False)
        print(article.url)
        url=article.url
    except:
        url=None
    return url
def levensthein(word1,word2):
    return fuzz.token_set_ratio(word1.lower(),word2.lower())
#Store entities in a list of tuples
def process_for_ner(doc):
    doc=nlp(doc)
    entities=[]
    for ent in doc.ents:
        if ent.label_ in ("GEO","GPE","ORG","PERSON"):
            entities.append((ent.text,ent.label_))
    #Remove Duplicates
    entities=list(set(entities))
    #print(entities)
    #Create a dictionary wuth entities as keys and a list of sentences as values
    ent_sentences={}
    #for each entity we calculate the Levensthein ratio with the other entities
    all_candidates=[]
    entity_types={}
    for ent in entities:
        ratio=[]
        #print(ent[0])
        for i in range(len(entities)):
            #check only entities with the same type
            if ent[1] == entities[i][1]:
                ratio.append((levensthein(ent[0],entities[i][0]),entities[i][0]))
        #keep entities with score higher than 80(assuming the differences between 80-100 are meaningless)
        #also sorting the resulting list to later get the first entity as the final one
        candidates=sorted([element[1] for element in ratio if element[0]>80 ],reverse=True)
        print(candidates)
        #add candidates in a list of lists to keep each list only once
        if candidates not in all_candidates:
            all_candidates.append(candidates)
            entity_types[candidates[0]]=ent[1]
    for candidates in all_candidates:
        #here we gather all wikipedia links related to this page
        #urls=[get_wikipedia_url(candidate) for candidate in candidates]
        #make list of lists of sentences for each candidate
        sentences=[find_sents(doc,candidate) for candidate in candidates]
        #turn it into regular list and remove duplicates
        all_sentences=list(set([item for sublist in sentences for item in sublist]))
        #Create a dictionary associating each final key with the sentences to be later used to get the sentiment score
        ent_sentences[candidates[0]]=all_sentences
    return ent_sentences,entity_types

#for ent in ent_sentences.keys():
#    sentiment=get_sentiment(ent_sentences[ent])
#    new_Entity=Entity.objects.create(name=ent,type=type)
#    new_Sentiment=Sentiment.objects.create(article=article_id,entity=new_Entity,sentiment=sentiment)
