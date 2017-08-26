import sys
import string
import random
import wolframalpha
import discord
import asyncio
import re

# Fun strings for invalid queries
invalidQueryStrings = ["Nobody knows.", "It's a mystery.", "I have no idea.", "No clue, sorry!", "I'm afraid I can't let you do that.", "Maybe another time.", "Ask someone else.", "That is anybody's guess.", "Beats me.", "I haven't the faintest idea."]
markupChars = ['*', '_', '~', '\\', '`']

def startWA(app_id):
    global waclient
    waclient = wolframalpha.Client(app_id)
    
# Prints a single result pod
def print_pod(text, title):
    return "**" + escape(title) + ":** " + escape(text).replace('\n', '')

# Prints a single image pod
def printImgPod(img, title):
    return "__**" + title + ":**__\n" + img

def escape(text):
    r = ''
    for c in bytes(text.replace('\\:', '\\u'), 'utf-8').decode('unicode_escape'):
        if c in markupChars:
            r += '\\' + c
        else:
            r += c
    return r
                            
def do_wolfram(query, extra):
    try:
        pods = list(waclient.query(query).pods)
    except AttributeError:
        pods = []
    results = extract(pods, extra)
    if len(results) == 0 and not extra:
        results = extract(pods, True)
    if len(results) == 0:
        results = [random.choice(invalidQueryStrings)]
    return results
    
def extract(pods, extra):
    results = []
    for pod in pods:
        if pod.text and (extra or pod.primary):
            results.append(print_pod(pod.text, pod.title))
    return results
