import os,sys
from flask import Flask,request
from utils import wit_response,get_news_elements
from pymessenger import Bot

app= Flask(__name__)

PAGE_ACCESS_TOKEN= "EAACUMYp8Hq4BAJjy00nQfIxciTlWmt5s9PV54Q98PinshUGes4WPfrzlw6dQJ1RYjH8y1umLkTriKLbZBZBJiZC64vvRaiOvJxjrPsS48ZCL2hg3ltBRolIUbpOZCDSztq4dMuEDmfRmpn9etqoZCgwlbOuboKPMQqhHMUlCNLC1wZBSoVS4qDZB"


bot=Bot(PAGE_ACCESS_TOKEN)
@app.route('/',methods=['GET'])
def verify():
	if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
		if not request.args.get("hub.verify_token") == "hello":
			return "Verification token mismatch",403
		return request.args["hub.challenge"],200
	return "hello World",200


@app.route('/',methods=['POST'])

def webhook():
	data = request.get_json()
	log(data)

	if data['object']=='page':
		for entry in data['entry']:
			for messaging_event in entry['messaging']:

				#IDs
				sender_id=messaging_event['sender']['id']
				recipient_id=messaging_event['recipient']['id']

				if messaging_event.get('message'):
					if 'text' in messaging_event['message']:
						messaging_text=messaging_event['message']['text']
					else:
						messaging_text='no text'

					#Echo		
					# response=None

					# entity,value=wit_response(messaging_text)
					# if entity=='newstypes':
					# 	response="Ok,I will send you {} news".format(str(value))
					# elif entity=='location':
					# 	response="Ok.So you live in {0}.I will send you top headlines from {0}".format(str(value))

					# if response==None:
					# 	response="Sorry,I am not getting what you want to know"
						

					categories=wit_response(messaging_text)
					elements=get_news_elements(categories)

					bot.send_text_message(sender_id,elements)
	return "ok",200

def log(message):
	print(message)
	sys.stdout.flush()

if __name__ == "__main__":
	app.run(debug=True,port=5000)

