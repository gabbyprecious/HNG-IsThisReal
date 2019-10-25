from flask import Flask, render_template, url_for, request
import requests
from bs4 import BeautifulSoup
from textblob import TextBlob
import matplotlib.pyplot as plt
import urllib
import nltk
# import spacy
# import en_core_web_sm
import pytesseract as pt
from PIL import Image
from gingerit.gingerit import GingerIt
# import googlemaps

# nltk.download("stopwords") # downloading nltk stop words
# nltk.download("punkt")
# assigning variables
# nlp = en_core_web_sm.load()
# stop_words = stopwords.words("english")
# gmaps = googlemaps.Client(key='AIzaSyAlvT9QoXecXq_WFfd4_slajtCnMJBXB6Y')
pt.pytesseract.tesseract_cmd = '/app/.apt/usr/bin/tesseract'
WordList = []

# ldefine a folder to store and later serve the images
UPLOAD_FOLDER = '/static/uploads/'

# allow files of a specific type
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])



app = Flask(__name__)

@app.route('/',methods=['POST','GET'])
def home():
    startload = 1
    if request.method == 'POST':
        searchTerm = str(request.form['message'])
        board = 29

        try:
            j = 0
            while j < 20:
                if j == 0:
                    nextItem = False
                else:
                    nextItem = True
                commentsCurrent = search_item(searchTerm, nextItem, j,  board)
                add_to_word_list(commentsCurrent)
                j += 1
        except:
            titlee = "Search failed"
            common = "Try again"
            startload = 0
            return render_template('home.html', starter = startload, searcht= titlee, poip=common)            

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


        titl = "From people's reaction to " + searchTerm + ", there were " + str(noOfSearchTerms) + " comments on nairaland"

        if (negative> 30):
            comm = "Dear Employee, there is a high percentage of negative comments regarding this job.\n It is only 30% likely. We are afraid it is not real."
        elif(negative>20):
            comm = "There is a slight chance that this is a real job. It is 50% likely. It's worth a try though." 
        elif (negative<20):
            comm = "Dear Employee, this job has high possibilities of being true. It is 80% likely. Let's give it a try."

        startload = 0
        return render_template('home.html', starter = startload, searcht= titl, poip=comm)
    return render_template('home.html', starter = startload, searcht= "",poip="")

# route and function to handle the upload page
@app.route('/upload', methods=['GET', 'POST'])
def upload_page():
    if request.method == 'POST':
        # check if there is a file in the request
        if 'file' not in request.files:
            return render_template('upload.html', msg='No file selected')
        file = request.files['file']
        # if no file is selected
        if file.filename == '':
            return render_template('upload.html', msg='No file selected')

        if file and allowed_file(file.filename):

            # call the OCR function on it
            extracted_text = file_type(file)

            if extracted_text == '':
                replyy = 'Sorry Character could not be clearly recognized'
                return render_template('upload.html',
                                   msg=replyy)
            # extract the text and display it
            return render_template('upload.html',
                                   msg='Successfully processed',
                                   extracted_text=extracted_text)
    
    return render_template('upload.html')

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

# function to check the file extension
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# defining useful functions
def file_type(filename):# function for character optical recognition
    s = Image.open(filename)
    text = pt.image_to_string(s)
    return text
        
if __name__ == '__main__':
    app.run()
