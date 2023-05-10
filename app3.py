from nltk.corpus import stopwords
import numpy as np
import networkx as nx
import regex
from flask import Flask, request, jsonify, render_template
import nltk
nltk.download('stopwords')
from transformers import PegasusForConditionalGeneration
from transformers import PegasusTokenizer
from transformers import pipeline

# Load pretrained tokenizer
pegasus_tokenizer = PegasusTokenizer.from_pretrained("google/pegasus-xsum")

model_name="google/pegasus-xsum"
# Define PEGASUS model
pegasus_model = PegasusForConditionalGeneration.from_pretrained(model_name)



def generate_summary(text, top_n=10):
   # pegasus_model = PegasusForConditionalGeneration.from_pretrained(model_name)
    
# Create tokens
    tokens = pegasus_tokenizer(text, truncation=True, padding="longest", return_tensors="pt")
    encoded_summary = pegasus_model.generate(**tokens)

# Decode summarized text
    decode_summary = pegasus_tokenizer.decode(
        encoded_summary[0],
        skip_special_tokens=True
      )
    summarizer = pipeline(
        "summarization", 
        model=model_name, 
        tokenizer=pegasus_tokenizer, 
        framework="pt"
      )
    summ = summarizer(text_ds[:2000],max_length=210)
    summary=summ[0]["summary_text"]

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
		return render_template('index1.html', title = "Summarizer", original_text = text, output_summary = summary, num_sentences = 5)

@app.route('/')
def homepage():
	title = "TEXT summarizer"
	return render_template('index1.html', title = title)

if __name__ == "__main__":
	app.debug = True
	app.run(port=5000)
