import requests

def translate(text, language = 'en'):
    url = "https://translate-service.scratch.mit.edu/translate"
    
    response = requests.get(url, params={
        'language': language,
        'text': text
    })
    if response.status_code != 200:
        return 'Translation error'
    return response.json()['result']


