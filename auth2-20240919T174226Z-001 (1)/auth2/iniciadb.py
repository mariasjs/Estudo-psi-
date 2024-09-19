#Este arquivo serve apenas para iniciar banco de dados 

import sqlite3

database = "database.db"
conn = sqlite3.connect(database)

with open('banco.sql') as f:
    conn.executescript(f.read())