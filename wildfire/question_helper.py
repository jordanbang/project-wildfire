import requests
import urllib
from wildfire.models import Question

BASE_URL = 'https://api.datamarket.azure.com/Bing/Search/News?$format=json&Query='

def get_news_for_question(question):
	requests.packages.urllib3.disable_warnings()
	headers = {'Authorization': 'Basic QjV4cmw3Wmt3SlVJMWEvQ1BnWU1XWVpoSERBb0hLNEhVeTRIVldLaGlVdz06QjV4cmw3Wmt3SlVJMWEvQ1BnWU1XWVpoSERBb0hLNEhVeTRIVldLaGlVdz0='}
	encoded = urllib.quote(question.text)
	r = requests.get(BASE_URL + "%27" + encoded + "%27", headers=headers, verify=False)

	if (r.status_code == 200):
		json = r.json()
		question.related_link = json['d']['results'][0]["Url"]
		question.save()

	return
