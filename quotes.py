import discord
import re
import sqlite3

def parse(message, quotes_file):
    content = message.content
    match = re.search('.+([A-Za-z0-9]:|\]:)+.+(\n[A-Za-z0-9].*)*', content)
    if(match is not None):
        if(match.group(0) == content):
            insert(content)
            return True 
    return False

def start():
    global conn
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS quotes (content TEXT)")
    conn.commit()

def insert(text):
    global conn
    c = conn.cursor()
    c.execute("INSERT INTO quotes (content) VALUES (?)", (text,))
    conn.commit()

def choose():
    global conn
    c = conn.cursor()
    c.execute("SELECT content FROM quotes ORDER BY RANDOM() LIMIT 1")
    return c.fetchone()[0]

def search(query):
    global conn
    c = conn.cursor()
    c.execute("SELECT content FROM quotes WHERE content LIKE ?", ('%' + query + '%',))
    results = []
    for result in c.fetchall():
        results.append(result[0])
    return results

conn = sqlite3.connect('quotes.db')
start()



