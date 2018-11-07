import requests

def translate(text):
    url = "https://translate-service.scratch.mit.edu/translate"

    response = requests.get(url, params={
        'language': 'en',
        'text': text
    })
    if response.status_code != 200:
        return 'Translation error'
    return response.json()['result']


