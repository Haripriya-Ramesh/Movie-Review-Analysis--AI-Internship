from flask import Flask, request, render_template
import numpy as np
import re
import requests
import json
from gevent.pywsgi import WSGIServer
import os

app = Flask(__name__)

def check(output):
    url =  "https://japerk-text-processing.p.rapidapi.com/sentiment/"
    payload = {"text": output}
    print(payload)
    headers = {
    'content-type': "application/x-www-form-urlencoded",
    'x-rapidapi-key': "537649ff73msh477f6855911bb13p129cf4jsnd5cb001617b2",
    'x-rapidapi-host': "japerk-text-processing.p.rapidapi.com"
    }
    response = requests.request("POST", url, data=payload, headers=headers)
    print(response.text)
    value = response.text
    output=json.loads(value)
    return response.json()
#home page
@app.route('/')
def summarizer():
    return render_template('summarizer.html')

#summarizer page
@app.route('/summarize',  methods=['POST'])
def summarize():
    output = request.form['output']
    output=re.sub("[^a-zA-Z.,]"," ",output)
    print(output)
    essay = check(output)
    print(type(essay['label']))
    if essay['label'] == "pos":
        output="Positive review"
    elif essay['label'] == "neg":
        output="Negative review"
    else:
        output="Neutral Review"
    #print(max(essay['probability'], key=essay.get))
    return render_template('summary.html',essay=essay,prediction_text='{}'.format(output))

port=os.getenv('VCAP_APP_PORT', '8080')


if __name__ == "__main__":

    app.secret_key=os.urandom(12)
    app.run(debug=True, host='0.0.0.0', port=port)
