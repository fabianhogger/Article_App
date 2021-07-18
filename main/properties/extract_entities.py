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
        if ent.label_ in ("GPE","ORG","PERSON"):
            entities.append((ent.text,ent.label_))
    #Remove Duplicates
    entities=list(set(entities))
    #print(entities)
    #Create a dictionary wuth entities as keys and a list of sentences as values
    ent_sentences={}
    #for each entity we calculate the Levensthein ratio with the other entities
    all_candidates=[]
    entity_types=[]
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
            entity_types.append(ent[1])
    for candidates in all_candidates:
        #here we gather all wikipedia links related to this page
        urls=[get_wikipedia_url(candidate) for candidate in candidates]
        #make list of lists of sentences for each candidate
        sentences=[find_sents(doc,candidate) for candidate in candidates]
        #turn it into regular list and remove duplicates
        all_sentences=list(set([item for sublist in sentences for item in sublist]))
        #Create a dictionary associating each final key with the sentences to be later used to get the sentiment score
        ent_sentences[candidates[0]]=all_sentences
    print(ent_sentences)

#for ent in ent_sentences.keys():
#    sentiment=get_sentiment(ent_sentences[ent])
#    new_Entity=Entity.objects.create(name=ent,type=type)
#    new_Sentiment=Sentiment.objects.create(article=article_id,entity=new_Entity,sentiment=sentiment)
"""
doc="The Bush administration has decided to repeal its 20-month-old tariffs on imported steel to head off a trade war that would have included foreign retaliation against products from politically crucial US states.Quoting administration and industry sources, The Washington Post said in its Monday editions that President George Bush is\xa0 likely to announce the decision this week.The officials said they had to allow for the possibility that Bush would make some change in the plan, but a source close to the White House said it was “all but set in stone”, the Post reported.A spokesman for the White House denied a decision had been made to repeal the tariffs.“The matter is still under review and we’ll make announcements when there are announcements to make,” the spokesman said.Ending the tariffs 16 months before schedule could spark a political backlash against Bush in next year’s presidential election in the pivotal steel-producing states of Ohio, Pennsylvania and West Virginia.The Washington Post sources said Bush’s aides concluded they could not run the risk that the European Union would carry out its threat to impose sanctions on citrus fruit from Florida, farm machinery, textiles and other products.A source involved in the negotiations said White House aides looked for some step short of a full repeal that would satisfy the European Union, but concluded that it was “technically possible but practically impossible”, according to the Post.Speculation had mounted that Washington would scrap or roll back the controversial tariffs after it last week sought and obtained an effective delay in retaliatory sanctions by countries opposed to them.The European Union, one of a number of trade partners to take action at the WTO over the levies, had warned it was ready to hit Washington with sanctions on up to $2.2 billion of goods within five days of the WTO approving the court ruling.The Bush administration imposed the duties, initially for up to 30%, in 2002 to help defend the country’s struggling steel industry against cheap imports"
process_for_ner(doc)
"""
"""
αρθρο --> οντόντητες
|
\____---> Sentiment

οντότητα--> αριθμός θετικών άρθρων  | αριθμός αρνητικών άρθρων
|
\____--> άρθρα με αυτή την οντότητα

Οντότητα many to many Αρθρα
Οπότε κάθε οντότητα θα έχει ενα κλειδί

Πράγματα που θα μπορώ να δω έτσι:
    Για ποια θέματα μιλάει κάθε κανάλι
    τα αρθρα με τα περισσοτερα views και την οντότητα
το χ καναλι έχει 59 θετικα αρθρα για το y

Χρησιμοποίησε Phrase Matcher για να βρίσκει χώρες?
Free Map για άρθρα.
https://www.datawrapper.de/maps/symbol-map
Ψαξε για κάθε entity αν έχει wikipedia entry και αν ναι πρόσθεσε την στον πίνακα με τα entities εφόσον δεν υπάρχει.

https://ashutoshtripathi.com/2020/05/04/how-to-perform-sentence-segmentation-or-sentence-tokenization-using-spacy-nlp-series-part-5/
https://www.datacamp.com/community/tutorials/fuzzy-string-python
fuzzy string matching
https://machinelearningmastery.com/choose-an-activation-function-for-deep-learning/
activation functions


1 βρές entities
2 βρες Levensthein distance για το καθένα
3 βάση ενός οριού πές ότι είναι το ίδιο
4.φτιαξε λίστες ίδιων
πχ. George Bush,Bush,Bus
    European Union,Union,European

6. Υπόθεσε ότι όλες οι προτάσεις της λίστας του αναφέρονται σε αυτό
7. μάζεψε σε dictionary για κάθε entity της προτάσεις που το αναφέρουν

8. κάνε sentiment analysis στις προτάσεις και βγάλε score για το entity
9. Εισχώρησε το στον πίνακα με τα entities



views
Πίνακας με άρθρα,
Πίνακας για βιβλιοθήκες
Most viewed story
1 Σελίδα με entities και sentiment (Ταξινομημένα βάση πλήθους άρθρων)
    Κάτω απο τα entities θα έχει Summary που θα λεεί top 3 covered entities για κάθε source με το sentiment
1 Σελίδα που δείχνει μερικά άρθρα για το κάθε entity (εφόσον πατηθεί στη προηγούμενη σελίδα)


"""
"""

"""
