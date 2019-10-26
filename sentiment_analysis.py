"""importing libraries"""
import requests
from bs4 import BeautifulSoup
from textblob import TextBlob
import urllib


WordList = []


def percentage(part, whole):
    """function to calculate percentage"""
    return round((100 * float(part)/float(whole)),2)


def word_count(string):
    """function to return count of comments"""
    counts = dict()
    words = string.split()

    for word in words:
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1

    return len(counts)


def search_item(search_term, next=False, page=0,  board=0):
    """function to search and return comments"""
    if next == False:
        page = requests.get("https://www.nairaland.com/search?q=" + urllib.parse.quote_plus(str(search_term)) + "&board="+str(board))
    else:
        page = requests.get("https://www.nairaland.com/search/"
                            + str(search_term) + "/0/"+str(board)+"/0/1" + str(page))
    soup = BeautifulSoup(page.content, 'html.parser')

    comments = soup.findAll("div", {"class": "narrow"})

    return comments


def add_to_word_list(strings):
    """function to add all comments to Wordlist"""
    global WordList
    k = 0
    while k < len(strings):
        if word_count(strings[k].text) > 1:
            WordList.append(strings[k].text)
        k += 1


searchTerm = input("Enter search term: ")
board = 29

j = 0

while j < 20:
    if j == 0:
        nextItem = False
    else:
        nextItem = True
    commentsCurrent = search_item(searchTerm, nextItem, j,  board)
    add_to_word_list(commentsCurrent)
    j += 1

polarity = 0
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
    polarity += analysis.sentiment.polarity

    if (analysis.sentiment.polarity == 0):
        neutral += 1
    elif (analysis.sentiment.polarity < 0.00):
        negative += 1
    elif (analysis.sentiment.polarity > 0.0):
        positive += 1

noOfSearchTerms = positive + negative + neutral

positive = percentage(positive, noOfSearchTerms)
negative = percentage(negative, noOfSearchTerms)
neutral = percentage(neutral, noOfSearchTerms)


print("From people's reaction to " + searchTerm + ", there were " + str(noOfSearchTerms) + " comments "
      "on nairaland")

if (negative> 30):
    print("Dear Employee, there is a high percentage of negative comments regarding this job.\n It is only 30% likely. We are afraid it is not real.")
elif(negative>20):
    print("There is a slight chance that this is a real job. It is 50% likely. It's worth a try though." )
elif (negative<20):
    print("Dear Employee, this job has high possibilities of being true. It is 75% likely. Let's give it a try.")


