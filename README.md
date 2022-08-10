## Project Overview

The BreakingEven api is a tool to be used in newsrooms to speed up headline writing and tweet generation, detect potential bias in copy and guide social media content to maximise interactions. <br>

. <br>


<img src="images/shutterstock_2131280571.jpg" style="width: 700px;"/>

<br>
<br>

### Business Problem

Trust in print media is at an all-time low, according to . <br>

Much of the focus in the industry has been on so-called 'fake news', with fact-checking now a booming sector. <br>

But less attention has been paid to sloppy journalism brought about by the increasing need for speedy copy, and to the blurring of the lines between the news pages and opinion section <br>

BreakingEven harnesses the power of the latest generation of machine learning language models, similar to those used by Google's search function, to make a start in tackling these problems <br>

The api can be used by journalists to generate accurate headlines on the fly, by subeditors to flag up when opinion is creeping into news stories, and by social media teams to quickly curate output. <br>

<img src="images/shutterstock_1730598724.jpg" style="width: 700px;"/>
<br>
<br>

### Layout of code

Given memory considerations, GitHub file size restrictions and the processing power of Google Colab, the code is split up between GitHub and Colab. The Colab folder can be shared on request.<br>

Data collection duties were shared across these platforms, as detailed below, while the rest of the code is on Colab.<br>


### The Data

The models were trained on 1.3 million news articles and 1.8 million tweets from five outlets: CNN, Fox News, The Gaurdian, Reuters and the BBC.<br>

Free-to-use python library [snscrape](https://github.com/JustAnotherArchivist/snscrape), was used to scrape the tweets. It returns the tweet text, URL links within the tweet and metrics such as likes and retweets for tweets between specified dates for specified accounts.

For those able to afford $1500, the articles can all be retrieved from the [News Api](https://newsapi.org) module.<br>

This example instead used the Internet [Wayback Machine](https://archive.org/web/) to retrieve the links to articles hosted on the outlet's homepage, going back to 2013.<br>

These URLs were then used to scrape the actual article and retreive the text, headline, category, and date.<br>

Guardian articles were scraped using its free api.<br>

The two datasets were then linked as below...

<img src="Viz/BreakingEven (2).jpg" style="width: 700px;"/>


### Methods

## Headline and tweet summarizers

The aim was to create an inferential model, as the headline and tweet summarizers are seen as merely a first step towards developing an array of tools to analyse journalistic language. To do this, we need models that learn the DNA of language, in order that we can then put them to use building various types of language tools, in the same way the human body uses the genetic code to build differnt parts. 

The first attempt was 'lstm' model, which uses cells that store the state of model so that relationships of words that appear close together and far apart can be encoded, allowing us to feed in long articles. The encoded article was trained against the articles headline. In production, the article text is fed into an encoder, which then generates a predicted headline, one line at a time.



<br>

<img src="Viz/music_wc.png" style="width: 700px;"/>
<br>
<br>

### Headline Results
<br>

**The two best performing models, out of the 24 created, predicted the correct labels almost 80 percent of the time.** <br>
<br>
<br>

**The best-performing model struggled most with stories  in the world-news, business and lifestyle categories as these tend to be more loosely defined and overlap with other categories.** <br>
<br>
<br>
<img src="Viz/log_res.png" style="width: 700px;"/>
<br>

**The model's internal decision making process can analyzed to reveal which words are the most important in predicting category labels, whether across the whole corpus, each category or individual articles. providing potentially valuable hidden insights.**
<br>

<br>
<br>
<img src="Viz/us-politics.png" style="width: 700px;"/>

### Conclusion

* The model is definitely accurate enough to suggest it could become a viable product, both internally and commercially, with more resources.

* It also generates useful insights, potentially revealing hidden threads that run through categories and generating story angles. It can also help in analysing reporting standards in our own copy.

<img src="Viz/le_tensor_google.jpg" style="width: 700px;"/>

### Next steps

* Provide funds for more storage space and processing power to enable the models to be better 'tuned' and to enable more advanced processing techniques on the article to help it discern between overlapping categories

* Channel more resources into analyzing the workings of the model to find hidden insights. The model can easily be linked to Twitter analytics, or to other metadata tags such as byline to glean distinctive features of successful writers or stories that play well on social media
 

<br>
<br>
