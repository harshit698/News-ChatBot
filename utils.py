from wit import Wit
from gnewsclient import gnewsclient

access_token="HE2BO5SNACMG5XMRZREM3TUXEHMBBLIB"

client=Wit(access_token=access_token)

def wit_response(message_text):
	resp=client.message(message_text)
	# entity=None
	# value=None
	categories={'newstypes':None,'location':None}

	entities=list(resp['entities'])

	# try:
	# 	entity=list(resp['entities'])[0]
	# 	value=resp['entities'][entity][0]['value']
	# except:
	# 	pass
	# return (entity,value)

	for entity in entities:
		categories[entity]=resp['entities'][entity][0]['value']

	return categories

def get_news_elements(categories):
	news_client=gnewsclient()
	news_client.query=''

	if categories['newstypes'] != None:
		news_client.query += categories['newstypes']+' '
	if categories['location'] != None:
		news_client.query += categories['location'] 

	return news_client.query		

	news_items=news_client.get_news()
	elements=[]

	for item in news_items:
		element={
			'title':item['title']
			'buttons':[{
					'type':'web_url',
					'title':'Read more',
					'url':item['link'],
			}],
			'image_url':item['img']

			elements.append(element)
			
		}

print(get_news_elements(wit_response("I want sports news from india")))