# -*- coding: utf-8 -*-
"""
Created on Sat Oct 26 00:28:34 2019

@author: PRECIOUS
"""
from flask import Flask, render_template, url_for, request
from model import *

app = Flask(__name__)

@app.route('/',methods=['POST','GET'])
def home():
    startload = 1
    if request.method == 'POST':
        votes = str(request.form['votes']) 
        comp = str(request.form['comp'])
        mail = str(request.form['mail'])
        report = confidence_check(mail, comp, votes)        
        startload = 0
        return render_template('index.html', starter = startload, report=report)
    return render_template('index.html', starter = startload)
  

def confidence_check(mail, comp, votes):
    if mail and comp and votes:
        correction = check(mail)
        positive, negative, neutral = (analysis(comp)) 
        if negative < 20:
            n = 10
        elif negative >=20 and negative < 30:
                n = 5
        elif negative >= 30:
            n = 0
        if correction > 4 :
            c = 0
        else:
            c = 1
        if votes == "yes":
            confidence = ((c + n + 5) / 30) * 10
        else:
            confidence = 0
        if confidence > 6:
            return "There's a high possibility that this job is not real"
        if confidence >= 4 and confidence <= 6:
            return "You could attend but, there's a slight element of it being a scam"
        if confidence < 4:
            return "Job is a confirm scam, don't try it"       


if __name__ == '__main__':
    app.run()
