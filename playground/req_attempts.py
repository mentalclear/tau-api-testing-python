import requests
import json

# Requesting: 
#  - same user: ?seed=best
#  - nationality: ?nat=us 
#  - results amount: ?results=3

BASE_URI = 'https://randomuser.me/api/?seed=best&nat=us&results=3'

def read_all():
    response = requests.get(BASE_URI)    
    # response_text = response.json()
    # Alternative way
    response_text = json.loads(response.text)


    print(json.dumps(response_text['results'], indent=4))
   

    # Getting to the last name: 
    # print(json.dumps(response_text['results'][0]['name']['last'], indent=4))

read_all()