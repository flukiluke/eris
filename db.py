import sqlite3

def cursor():
    global conn
    return conn.cursor()

def commit():
    global conn
    conn.commit()

def insert(table, data):
    global conn
    c = conn.cursor()
    keys = [*data]
    template_list = ','.join(['?'] * len(data))
    query = "INSERT INTO {} ({}) VALUES ({})".format(table, ','.join(keys), template_list)
    c.execute(query, tuple(data[k] for k in keys))
    conn.commit()

def start():
    global conn
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS quotes (content TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS alerts (target TEXT, time INTEGER, message TEXT)")
    conn.commit()

conn = sqlite3.connect('persist.db')
start()
