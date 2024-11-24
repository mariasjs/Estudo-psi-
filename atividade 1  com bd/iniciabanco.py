import sqlite3

conn = sqlite3.connect('database.db')

with open('database/banco.sql') as arquivo:
    conn.executescript(arquivo.read())