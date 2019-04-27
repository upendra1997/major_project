from flask import Flask, redirect
from analyzer import analyze
import os

host = 'localhost'
if "IP" in os.environ.keys():
    host = os.environ["IP"]

port = 8080
if "PORT" in os.environ.keys():
    port = os.environ["PORT"]

app = Flask(__name__,static_folder="./client/",static_url_path='')

object = analyze()

@app.route('/',methods=["GET"])
def main_page():
    return redirect('index.html')

@app.route('/text/<text>',methods=["GET"])
def sentiment_analyze(text):
    print(text)
    if len(text)==0:
        return str(0)
    result = object.input(text)
    print(text,result)
    return str(result)

app.run(host=host,port=port,debug=True)