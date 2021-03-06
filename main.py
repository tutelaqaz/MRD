# -*- coding: utf-8 -*-

DEFAULT_PORT = 5000
ADDITIVE_FOR_UID = 1000

try:
    from os import getuid

except ImportError:
    def getuid():
        return DEFAULT_PORT - ADDITIVE_FOR_UID

import re
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def main_page():
    return render_template('main_page.html')
@app.route('/bts.html')
def bts():
    return render_template('bts.html') 
@app.route('/contacts.html')
def contacts():
    return render_template('contacts.html') 
@app.route('/dmitr.html')
def dmitr():
    return render_template('dmitr.html') 
@app.route('/download_page.html')
def download_page():
    return render_template('download_page.html') 
@app.route('/reference.html')
def reference():
    return render_template('reference.html') 
@app.route('/tutorial.html')
def tutorial():
    return render_template('tutorial.html') 
@app.route('/index.html')
def index():
    return render_template('index.html')
    
def open_dict(path):
    f = open(path,'r',encoding = 'utf-8')
    _dict = f.read().split('<superEntry>')
    return _dict
    
def tag_cleaner(art):
    fine_elements = []
    elements = art.split('\n')
    for element in elements:
        if element != '':
            m = re.match('<.+>',element)
            if m != None:
                element = element.strip(m.group())
        fine_elements.append(element)
    fine_art = '\n'.join(fine_elements)
    return fine_art
    
def fine_dict():
    _dict = open_dict('bts+tei.txt')
    all_words = []
    for art in _dict:        
        if art == '':
            _dict.remove(art)
        else:
            art = tag_cleaner(art)
            elements = art.split('\n')
            word = elements[1].strip('<orth>, ').lower()
            all_words.append({word:art})
    return all_words

@app.route('/index.html', methods=['POST'])
def search():
    all_words = fine_dict()
    key = request.form["key_word"]
    key = key.lower()
    i = 0
    for word in all_words:  
        if key == list(word.keys())[0]:
            result = list(word.values())[0].strip('"')
        else:
            i += 1        
    if i >= len(all_words):
        result = 'Not found'    
    return render_template('/index.html', key=key, result=result)

if __name__ == '__main__':
    app.run(port=getuid() + ADDITIVE_FOR_UID, debug=True)
