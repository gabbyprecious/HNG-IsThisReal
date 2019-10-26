import nltk #download the tokenizer english by python -m nltk.downloader punkt in the cmdimport spacy
import requests
from bs4 import BeautifulSoup
from textblob import TextBlob
import urllib
from gingerit.gingerit import GingerIt
from nltk.corpus import stopwords #download by python -m nltk.downloader stopwords in the cmd
stop_words = stopwords.words("english") 

def percentage(part, whole): # calculate percentage
    if whole != 0:
        return round((100 * float(part)) / float(whole), 2)
    else:
        return "Error calculating percentage"

def word_count(string):
    """function to return count of comments"""
    try:
        counts = dict()
        words = string.split()
        for word in words:
            if word in counts:
                counts[word] += 1
            else:
                counts[word] = 1
        return len(counts)
    except:
        print("Word count failed")
  

def add_to_word_list(strings):
    """function to add all comments to Wordlist"""
    global WordList
    try:
        k = 0
        while k < len(strings):
            if word_count(strings[k].text) > 1:
                WordList.append(strings[k].text)
            k += 1
    except:
        print("Add to WordList failed")


def check(mail):
    f = word(mail, 'sentence')
    corrections = 0
    for s in f:
        g = GingerIt()
        h = g.parse(s)
        corrections += len(h['corrections'])
    return corrections


def word(mail, final_type): # function to tokenize text 
        tok_sent = nltk.sent_tokenize(mail)
        tok_word = []
        for s in tok_sent:
            tok_word.append(nltk.word_tokenize(s))
        final_text = []
        for w in tok_word:
            if w not in stop_words:
                final_text.append(w)
        if final_type == 'sentence':
            return tok_sent
        elif final_type == 'word':
            return final_text


def search(search_term, next=False, page=0,  board=0):
    """function to search and return comments"""
    if next == False:
        page = requests.get("https://www.nairaland.com/search?q=" + urllib.parse.quote_plus(str(search_term)) + "&board="+str(board))
    else:
        page = requests.get("https://www.nairaland.com/search/"
                            + str(search_term) + "/0/"+str(board)+"/0/1" + str(page))
    soup = BeautifulSoup(page.content, 'html.parser')

    comments = soup.findAll("div", {"class": "narrow"})

    return comments
    


WordList = []
def analysis(comp):
    """function to evaluate sentiment"""
    try:
        j = 0
        board = 29
        while j < 10:
            if j == 0:
                nextItem = False
            else:
                nextItem = True
            commentsCurrent = search(comp, nextItem, j,  board)
            add_to_word_list(commentsCurrent)
            j += 1
    except:
        print("Search failed")
        
    positive = 0
    negative = 0
    neutral = 0
    
    previous = []
    for tweet in WordList:
        if tweet in previous:
            continue
        previous.append(tweet)
        analysis = TextBlob(tweet)
        """evaluating polarity of comments"""
        polarity = analysis.sentiment.polarity

        if (analysis.sentiment.polarity == 0):
            neutral += 1
        elif (analysis.sentiment.polarity < 0.00):
            negative += 1
        elif (analysis.sentiment.polarity > 0.0):
            positive += 1
    
    noOfSearchTerms = positive + negative + neutral

    positive = percentage(positive,  noOfSearchTerms)
    negative = percentage(negative,  noOfSearchTerms)
    neutral = percentage(neutral,  noOfSearchTerms)
    
    return positive, negative, neutral


#def confidence_check(mail, comp, votes):
#    if mail and comp:
#        correction = check(mail)
#        positive, negative, neutral = (analysis(mail) + analysis(comp)) / 2 
#        
 #       if negative < 20:
  #          n = 10
   #     elif negative >=20 and negative < 30:
#            n = 5
#        elif negative >= 30:
#            n = 0
#            
#        if corrections > 4 :
#            c = 0
#        else:
#            c = 1
#            
#        if votes == "yes":
#            confidence = ((c + n + 5) / 30) * 10
#        else:
#            confidence = 0
        
#        if confidence > 6:
#            return "There's a high possibility that this job is not real"
#        if confidence >= 4 and confidence <= 6:
#            return "You could attend but, there's a slight element of it being a scam"
#        if confidence < 4:
#            return "Job is a confirm scam, don't attend"

