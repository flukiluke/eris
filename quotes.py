import discord
import re
import db

def parse(message, quotes_file):
    content = message.content
    match = re.search('.+([A-Za-z0-9]:|\]:)+.+(\n[A-Za-z0-9].*)*', content)
    if(match is not None):
        if(match.group(0) == content):
            db.insert('quotes', {'content': content})
            return True
    return False

def choose():
    c = db.cursor()
    c.execute("SELECT content FROM quotes ORDER BY RANDOM() LIMIT 1")
    return c.fetchone()[0]

def search(query):
    c = db.cursor()
    c.execute("SELECT content FROM quotes WHERE content LIKE ?", ('%' + query + '%',))
    results = []
    for result in c.fetchall():
        results.append(result[0])
    return results
