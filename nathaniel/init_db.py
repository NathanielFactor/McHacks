import sqlite3

connection = sqlite3.connect('Conversations.db')

cur = connection.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS Conversations(\
    Userid INTEGER PRIMARY KEY AUTOINCREMENT,\
    UserName TEXT NOT NULL,\
    Created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,\
    Messages TEXT NOT NULL)\
    ")

connection.commit()
connection.close()
    