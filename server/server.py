from flask import Flask, redirect
# from analyzer import analyze
import os, json
from dummy import output

host = '0.0.0.0'
if "IP" in os.environ.keys():
	host = os.environ["IP"]

port = 80
if "PORT" in os.environ.keys():
	port = os.environ["PORT"]

app = Flask(__name__,static_folder="./client/",static_url_path='')

# object = analyze()

@app.route('/',methods=["GET"])
def main_page():
        return 	"hello"
        return redirect('index.html')

@app.route('/text/<text>',methods=["GET","POST"])
def sentiment_analyze(text):
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
	return json.dumps(ret)

app.run(host=host,port=port,debug=True)
