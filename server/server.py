from flask import Flask, redirect
# from analyzer import analyze
import os, json
from dummy import output
from flask_cors import CORS



host = 'localhost'
if "IP" in os.environ.keys():
	host = os.environ["IP"]

port = 80
if "PORT" in os.environ.keys():
	port = os.environ["PORT"]

app = Flask(__name__,static_folder="./client/",static_url_path='')
CORS(app)
# object = analyze()

@app.route('/',methods=["GET"])
def main_page():
        return 	"hello"
        return redirect('index.html')

@app.route('/text/<text>',methods=["GET"])
def sentiment_analyze(text):
	# print("HERE")
	#text = 'toilets are so bad that they stink like anything and basin is leaking'
	res = output(text)
 #    res = json.loads("""{'resultid': 'c5d38c59-46b7-4600-a7ab-a4b746432e26',                                                             
	#  'sentimentanalysis': [{'sentence': 'toilets are so bad that they stink like anything and basin is leaking',     
	#    'topic': 'toilets',                                                                                           
	#    'topic_norm': 'toilet',                                                                                       
	#    'text': 'so,bad',                                                                                             
	#    'text_norm': 'so,bad',                                                                                        
	#    'score': '-5.000000'},                                                                                        
	#   {'sentence': 'toilets are so bad that they stink like anything and basin is leaking',                          
	#    'topic': 'toilets,toilets',                                                                                   
	#    'topic_norm': 'toilet,toilet',                                                                                
	#    'text': 'stink',                                                                                              
	#    'text_norm': 'stink',                                                                                         
	#    'score': '-2.000000'},                                                                                        
	#   {'sentence': 'toilets are so bad that they stink like anything and basin is leaking',                          
	#    'topic': 'basin',                                                                                             
	#    'topic_norm': 'basin',                                                                                        
	#    'text': 'is,leaking',                                                                                         
	#    'text_norm': 'be,leak',                                                                                       
	#    'score': '-1.000000'}]}                                                                                                                                                                                            
	# """)
	print(text)
	obj = {}
	for i in res['sentimentanalysis']:
		topics = i['topic'].split(',')
		rel = i['text'].split(',')
		for t in topics:
			obj[t] = {'targets': [], 'score': 0}
			for r in rel:
				obj[t]['targets'].append(r)
				obj[t]['score'] = i['score']
	ret = {}
	ret['sentence'] = text
	ret['result'] = obj
	print(ret)
	response = app.response_class(
        response=json.dumps(ret),
        mimetype='application/json',
		status=200,
    )
	# response.headers['Access-Control-Allow-Origin'] = "*"
	return response

app.run(host=host,port=port,debug=True)
