import re
import random
import string
import requests
import pandas as pd
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup, NavigableString

def response(user_response):
    robo_response=''
    comp_name = user_response
    url="https://www.nairaland.com/search?q="+comp_name+"&board=29"
    request=requests.get(url)
    soup = BeautifulSoup(request.text, features="lxml")
    body = soup.find('div', {'class': 'body'})
    page_num = body.p.b.find_next_sibling('b').text
    arr = []
    for i in range(0, int(page_num)):
        text = soup.find_all('div', {'class': 'narrow'})
        for tags in text:
            if tags.find('blockquote'):
                newarr= []
                newtext = ""
                for i in tags.blockquote.next_siblings:
                    if not isinstance(i,NavigableString):
                        if i.text != "" or i.text != " ":
                            newtext+=i.text
                    else:
                        if i != "" or i != " ":
                            newtext+=i
                if len(newtext) != 0:
                    newarr.append(newtext)
                    arr.append(newarr)
        body = soup.find('div', {'class': 'body'})
        link = body.p.b.find_next_sibling('a')
        if link:
            url=link['href']
            request=requests.get(url)
            soup = BeautifulSoup(request.text, features="lxml")
        else:
            break

    # initialize list of lists
    data = arr 
    
    # Create the pandas DataFrame 
    df = pd.DataFrame(data, columns = ['Comments']) 
    
    # print dataframe. 
    df.to_csv("comments.csv", index=False)

    
name = input("enter company name: ")
response(name)