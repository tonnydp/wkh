# coding=utf-8
import sqlite3

con = sqlite3.connect("data\\num_wkh.db")
cur = con.cursor()
cur.execute("SELECT COUNT(*) FROM Round")
print(cur.fetchone()[0])
cur.execute("SELECT * FROM Round")
rlist = cur.fetchall()
for line in rlist:
	print(line) 
rnd = 1
count_obj = cur.execute("SELECT * FROM Owner WHERE rnd=?", (rnd,))
count = count_obj.fetchall()
print(count)

