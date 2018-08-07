# -*- coding: utf-8 -*-
import psycopg2

try:
    conn = psycopg2.connect("dbname='question' user='user' host='localhost' password='secret'")
    cur = conn.cursor()
    cur.execute("""SELECT * from users""")
    rows = cur.fetchall()
    print("Show the users")
    for i in range(len(rows)):
        row = rows[i]
        print(f"[{i}]: {row[0]}")
except:
    print("Unable to connect to the database")