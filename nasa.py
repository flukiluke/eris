import requests
import discord
import util

api_key = "5f6aY0lmpr5JZP9yroHa78SgWyTDBhps96zMTqhw"

def get_astropod():
    url = "https://api.nasa.gov/planetary/apod?api_key=" + api_key

    result = requests.get(url)

    if result.status_code != 200:
        return ("SPAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACE isn't working right now. Please check your sky, and try again.", False)

    data = result.json()

    url = data['url']
    title = util.escape(data['title'])
    explanation = util.escape(data['explanation'])
    date = data['date']

    if 'youtube' in url:
        code = url.split("embed/")[1].split("?")[0]
        url = "https://www.youtube.com/watch?v=" + code
        return ("**" + title + "**" + "\n" + explanation + "\n" + url, False)

    img_url = url

    e = discord.Embed().set_image(url=img_url)
    e.title = title
    e.description = explanation
    e.url = "https://apod.nasa.gov/apod/astropix.html"
    return (e, True)

def get_spy(lat, long_):
    url = "https://api.nasa.gov/planetary/earth/imagery?api_key=" + api_key + "&lat=" + lat + "&long=" + long_

    result = requests.get(url)

    if result.status_code != 200:
        return ("SPAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACE isn't working right now. Please check your sky, and try again.", False)

    data = result.json()

    img_url = data['url']

    return discord.Embed().set_image(url=img_url)