# Article App

Example Article app using django.
Scraped Articles from BBC and Aljazeera using a crawler with the help of the library scrapy.
Trained a LDA model on around 2000 articles for the  purpose of topic modelling using the gensim module.

## Latent Dirichlet Allocation (LDA)

In natural language processing, the latent Dirichlet allocation (LDA) is a generative statistical model that allows sets of observations to be explained by unobserved groups that explain why some parts of the data are similar. For example, if observations are words collected into documents, it posits that each document is a mixture of a small number of topics and that each word's presence is attributable to one of the document's topics. LDA is an example of a topic model and belongs to the machine learning toolbox and in wider sense to the artificial intelligence toolbox.[1]

Plainly explained LDA is an algorithm used for topic modelling that takes as input separate bodies of texts and than categorizes them in a given number of topics based on word appearances. The model creates a vector for each document that than can be used to find similar documents.

The Documents used to train the model are really important and should be close to the application domain in order for the model to have a meaningful result on unseen bodies of text.
### Training

The algorithm should be trained on text without special characters and commonly used words.The model has various parameters to experiment with, the most important one being the number of topics.

### Evaluation

LDA can't be evaluated like using common metrics like accuracy so we would have to test the model ourselves and also use some other metrics unique to the model itself.  Below we are going to be using perplexity and topic coherence to evaluate our models.
There is actually more than one topic coherence kind.
- U-mass
- C_v
- C_p
- C_uci
- C_umass
- C_npmi
- C_a
### Similarity

For Finding similar documents gensim has a similarity class that uses cosine similarity but we will have to see what kind of results it produces.Many people also recommend Jensen-Shannon distance metric.
Some of the possible  similarity metrics are
- Jensen-Shannon
- Hellinger distance
- Kullback–Leibler
- Jaccard

## Visualization

As mentioned above for the creation of the lda model I used the gensim library. For the visualization of the resulting model there is a great library called pyLDAvis.This tool creates an interactive html page with various important data about the model.

### Results

Initially I used 500 articles for my first model and as parameters I set it to num_topics=20, random_state=100,update_every=1, chunksize=100, passes=10, alpha='auto'
![lda10](images/lda10.jpg)
Download the html file [here]( https://github.com/fabianhoegger/Article_App/blob/main/main/properties/lda/lda10/ldavis10.html)

After removing some non english documents I retrained the model on about 350 documents with the same parameters.Here I selected one of the topics to show how the html file works
![lda10clean](images/lda10cleaned.jpg)
Download the html file [here]( https://github.com/fabianhoegger/Article_App/blob/main/main/properties/lda/lda10/lda10_cleaned/ldavis10clean.html)

Below is the result of the model with the same 500 articles but 20 topics
![lda20](images/lda20.png)
Download the html file [here](https://github.com/fabianhoegger/Article_App/blob/main/main/properties/lda/lda20/ldavis20.html)

Finally I tried training on all the english files I had Scraped
first dividing them in 10 topics and then 20.
![lda20](images/lda10_1835.png)
Download the html file [here](hhttps://github.com/fabianhoegger/Article_App/blob/main/main/properties/lda/lda_1835/lda_10_1835/ldavisall.html)
![lda20](images/lda20_1835.png)
Download the html file [here](https://github.com/fabianhoegger/Article_App/blob/main/main/properties/lda/lda_1835/lda_20_1835/ldavisall20.html)

### Results
>On the first table there are various models with different number of articles and their corresponding perplexity, U-mass coherence and number of topics.
U-mass coherence is better when close to zero and perplexity is optimal at its lowest.

|Model | Perplexity |  U-mass Coherence| Articles |Topics
| -----| ----------  | ----------------|----------|------|
| LDA10 | -8.270   | -9.366|         500|10|
| LDA20 | -13.652  |  -8.049|      500|20|
|lda_10_1835|-8.488| -5.999|      1835|10|
|lda_20_1835 | -12.778| -8.678|   1835|20|

#### Models based on Articles names.
> Because  using U-mass coherence didn't help to distinguish the perfomance of the models for 2450 articles I started using  CV coherence which immediately made things clearer.The higher the cv coherence the better.

|Model | Perplexity |  U-mass Coherence| CV Coherence|Topics
| -----| ----------  | ----------------|----------|----|
|lda_2450|-8.128     | -19.412|0.694| 5|
|lda10_2450|-8.785   |-19.537|0.672|10|
|lda15_2450|-15.156 |-18|0.555|15|
|lda_20_2450|-24.223 |-17.727| 0.556|20|
|lda30_2450|-33.610| -18.760| 0.639 |30|
|lda40_2450|-50.990| -19.720| **0.735**|40|



![c-v_graph](images/c_v_coherence1to50.png)

>Coherence along with perplexity

![c-v_graph](images/cv_coherence_perplexity1to50names.png)
#### Models trained with all the Articles

|Model | Perplexity | CV Coherence|Topics
| -----| ---------- | ------------|------|
|lda_2450|-7.921   |0.352| 5|
|lda10_2450|-8.337 |0.401|10|
|lda15_2450|-11.174 |**0.479**|15|
|lda_20_2450|-12.674|0.467|20|
|lda30_2450|-15.047 |0.401|30|
|lda40_2450|-17.387 |0.418|40|
|lda50_2450|-19.784 |0.420|50|
|lda55_2450|-21.022|0.406|55|
|lda60_2450| -22.208|0.396|60|
|lda70_2450|-24.631|0.349|70|
|lda100_2450|-31.802|0.352|100|
>As we see model coherence maximizes at 15 topics
but the difference is quite minimal. In general we see that the
value of **Perplexity** is not as low as in the models trained only on the article names and **Coherence** is also lower. That might be explained by the fact that now the models are trained on a much bigger corpus.


![c-v_graph](images/c_v_coherence1to50correct.png)

>Coherence along with perplexity shows that perplexity keeps decreasing so we have to try an increased number of topics to see if it ever bottoms out.

![c-v_graph](images/cv_coherence_perplexity1to50.png)


#### Examples

Below I ran some similarity tests using the same Articles for 2 different models.
I classified the articles as **irrelevant** ,**slightly relevant** and **relevant**
The first model was trained  with 15 number of topics (the one from the table above) .
The 2nd was trained with 50 topics for the same articles as the first.

Article given: **Covid-19 in the UK: How many coronavirus cases are there in your area? - BBC News**

**MODEL 1**
1. Newcastle city centre £50m revamp plan - BBC News **irrelevant**
2. Covid: Guernsey leaves second pandemic lockdown - BBC News' **relevant**
3. Gold rush threat to Amazon jungle | News News | Al Jazeera **irrelevant**
4. Machine finds tantalising hints of new physics - BBC News **irrelevant**
5. Seen from the sky: Polluted waters around the world | Gallery News | Al Jazeera **irrelevant**
6. COVID jabs bring relief for vulnerable California farmworkers | Agriculture News | Al Jazeera **relevant**
7. Dating agencies boom in China | Arts and Culture News | Al Jazeera **irrelevant**
8. Jinxed Japanese space programme | News News | Al Jazeera **irrelevant**
9. Munching your way through the afternoon | News News | Al Jazeera **irrelevant**
10. Hot tub accidents triple in lockdown, says insurer - BBC News **slightly relevant**




**MODEL 2**

1. Canada quarantines 500 suspected SARS cases | News News | Al Jazeera  **slightly relevant**
2. Covid: Five more in hospital on Isle of Man as 45 new cases confirmed - BBC News **relevant**
3. How the COVID-19 pandemic is affecting mental health | News News | Al Jazeera **relevant**
4. Japan is greying fast | News News | Al Jazeera **irrelevant**
5. Covid: 17 patients treated after Ysbyty Gwynedd outbreak - BBC News' **relevant**
6. 'Covid-19: Brazil to get fourth health minister since pandemic began - BBC News **relevant**
7. Why is India staring at a ‘second peak’ of COVID cases? | Coronavirus pandemic News | Al Jazeera  **relevant**
8. Covid-19: India reports record daily rise in new infections - BBC News **relevant**
9. Russia identifies two cases of South African COVID variant | Coronavirus pandemic News | Al Jazeera **relevant**
10. COVID jabs bring relief for vulnerable California farmworkers | Agriculture News | Al Jazeera **relevant**






>MODEL 1 had  7 **irrelevant**, 1 **slightly relevant**, 2 **relevant**

>MODEL 2 had  1  **irrelevant**, 2 **slightly relevant**, 7 **relevant**


Article given: **School attendance back at high levels in England - BBC News**



**MODEL 1**
1. We were the only people there to support them" - BBC News **irrelevant**
2. Over 50 and overlooked for work' - BBC News **irrelevant**
3. "Covid and cancer: 'It felt like the universe was out to get me' - BBC News **slightly relevant**
4. Nurseries sent first official cyber-attack warning - BBC News  **irrelevant**
5.  "Coronavirus: 'We got through lockdown by dancing' - BBC News"  **relevant**
6. Online privacy: digitally exposed | Science and Technology News | Al Jazeera **irrelevant**
7. Covid in Wales: More face-to-face university teaching after Easter - BBC News  **relevant**
8. Covid-19: Lateral flow testing for years 12-14 pupils - BBC News **relevant**
9. Watch: Freestyle Ski and Snowboarding World Championships - Snowboard Big Air finals - BBC Sport **irrelevant**
10. Covid: Wales' school pupils 'excited and nervous' about return - BBC News  **relevant**



**MODEL 2**
1. Coronavirus: 'Everyone is excited to be back at school' - BBC News **relevant**
2. Nurseries sent first official cyber-attack warning - BBC News **irrelevant**
3. LIVE: Scottish Conservative Party conference speech by Douglas Ross - BBC News **irrelevant**
4. Covid in Wales: More face-to-face university teaching after Easter - BBC News **relevant**
5. Censors hold back Chinese cinema | News News | Al Jazeera **irrelevant**
6. Guernsey's autism centre to move schools over space issue - BBC News **irrelevant**
7. Covid: Outdoor education centres 'may not survive' - BBC News **relevant**
8. Covid-19: Lateral flow testing for years 12-14 pupils - BBC News **relevant**
9. Ipswich aims to become 'UK's first 15-minute' town - BBC News **irrelevant**
10.  Cross-border workers call for home-working tax law - BBC News **irrelevant**






>MODEL 1 had  5 **irrelevant**, 1 **slightly relevant**, 4 **relevant**

>MODEL 2 had  6 **irrelevant**, 0 **slightly relevant**, 4 **relevant**


## Scraping

To scrap bbc and aljazeera I used scrapy's SitemapSpider class that automatically crawls a websites sitemap which is really usefull.
Currently For each article the scraper downloads the page url,title and text body.
[Click here to view the scripts](https://github.com/fabianhoegger/Article_App/tree/main/main/scraper/scraper/spiders).
The scrapy project is connected to my django app and the
Data is stored to a Django postgresql database.
## Website

After gathering the articles I created a small website where you can view some article titles and click a button that starts training an lda model.
![website](images/website.png)

## Links



https://www.analyticsvidhya.com/blog/2016/08/beginners-guide-to-topic-modeling-in-python/
https://datascience.aero/topic-modelling/
http://qpleple.com/perplexity-to-evaluate-topic-models/


https://www.machinelearningplus.com/nlp/topic-modeling-gensim-python/#17howtofindtheoptimalnumberoftopicsforlda


https://www.machinelearningplus.com/nlp/topic-modeling-gensim-python/
https://towardsdatascience.com/lets-build-an-article-recommender-using-lda-f22d71b7143e
https://radimrehurek.com/gensim/similarities/docsim.html
https://radimrehurek.com/gensim/auto_examples/core/run_similarity_queries.html

https://radimrehurek.com/gensim/auto_examples/core/run_corpora_and_vector_spaces.html#sphx-glr-auto-examples-core-run-corpora-and-vector-spaces-py

https://towardsdatascience.com/topic-modelling-in-python-with-nltk-and-gensim-4ef03213cd21

https://medium.com/analytics-vidhya/gensim-lda-topic-modeling-for-article-discovery-9707237e4f0d

https://medium.com/analytics-vidhya/web-scraping-with-scrapy-and-django-94a77386ac1b


https://www.machinelearningplus.com/nlp/topic-modeling-visualization-how-to-present-results-lda-models/

https://miningthedetails.com/blog/python/lda/GensimLDA/
https://groups.google.com/g/gensim
https://rare-technologies.com/what-is-topic-coherence/
