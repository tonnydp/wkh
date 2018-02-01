import sqlite3

def get_cur_round(cur):
	count_obj = cur.execute("SELECT COUNT(id) FROM Round")
	count = count_obj.fetchone()[0]
	if count == 0:
		return (1, 1)
	cur.execute("SELECT id FROM Round WHERE ok=1")
	rnd_list = cur.fetchall()
	print(rnd_list)
	rnd = 0
	cur_mk_id = -1
	for rnd_tuple in rnd_list:
		if rnd_tuple[0] > rnd:
			rnd = rnd_tuple[0]
	print(rnd)
	cur.execute("SELECT cur_mk_id FROM Round WHERE id=?", (rnd + 1,))
	cur_mk_id_list = cur.fetchall()
	print(cur_mk_id_list)
	if cur_mk_id_list == []:
		return (rnd + 1, 1)
	else:
		cur_mk_id = -1
		for mid in cur_mk_id_list:
			if mid[0] > cur_mk_id:
				cur_mk_id = mid[0]
		return (rnd + 1, cur_mk_id)


con = sqlite3.connect("data\\num_wkh.db")
cur = con.cursor()
get_cur_round(cur)

cur.execute("INSERT INTO Round VALUES(1,1,204884,'2018-02-01_09:35:00')")
rlist = cur.execute("SELECT * FROM Round").fetchall()
print(rlist)
con.commit()
cur.close()
con.close()