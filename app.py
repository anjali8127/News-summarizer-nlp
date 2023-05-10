from nltk.corpus import stopwords
import numpy as np
import networkx as nx
import regex
from flask import Flask, request, jsonify, render_template
import nltk
nltk.download('stopwords')
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
nltk.download('punkt')


def generate_summary(text):
    stopWords = set(stopwords.words("english"))
    words = word_tokenize(text)
   
# Creating a frequency table to keep the 
# score of each word
   
    freqTable = dict()
    for word in words:
        word = word.lower()
        if word in stopWords:
            continue
        if word in freqTable:
            freqTable[word] += 1
        else:
            freqTable[word] = 1
    sentences = sent_tokenize(text)
    sentenceValue = dict()
   
    for sentence in sentences:
        for word, freq in freqTable.items():
            if word in sentence.lower():
                if sentence in sentenceValue:
                    sentenceValue[sentence] += freq
                else:
                    sentenceValue[sentence] = freq
   
   
   
    sumValues = 0
    for sentence in sentenceValue:
        sumValues += sentenceValue[sentence]
   
# Average value of a sentence from the original text
   
    average = int(sumValues / len(sentenceValue))
    summary = ''
    for sentence in sentences:
        if (sentence in sentenceValue) and (sentenceValue[sentence] > (1.2 * average)):
            summary += " " + sentence
    return summary

#----------FLASK-----------------------------#

app = Flask(__name__)
@app.route('/templates', methods =['POST'])
def original_text_form():
		text = request.form['input_text']
# 		print("TEXT:\n",text)
		summary = generate_summary(text)
# 		print("*"*30)
# 		print(summary)
		return render_template('index.html', title = "Summarizer", original_text = text, output_summary = summary, num_sentences = 5)

@app.route('/')
def homepage():
	title = "TEXT summarizer"
	return render_template('index.html', title = title)

if __name__ == "__main__":
	app.debug = True
	app.run(port=8000)
