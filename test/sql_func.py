import sqlite3


def get_con_cur(db_path):
	con = sqlite3.connect(db_path)
	cur = con.cursor()
	return(con, cur)

def db2dict(cur, rnd):
	cur.execute("SELECT * FROM Monkey WHERE rnd=?", (rnd,))
	mlist = cur.fetchall()
	mdict_list = []
	for m in mlist:
		md = {}
		md["id"] = m[0]
		md["gen"] = m[1]
		md["cz"] = m[2]
		md["sy"] = m[3]
		md["jj"] = m[4]
		md["kg"] = m[5]
		md["price_type"] = m[6]
		md["price"] = m[7]
		md["owner_addr"] = m[8]
		md["rnd"] = m[9]
		md["time"] = m[10]
		mdict_list.append(md)

	cur.execute("SELECT * FROM Owner WHERE rnd=?", (rnd,))
	olist = cur.fetchall()
	odict_list = []
	for o in olist:
		od = {}
		od["name"] = o[0]
		od["addr"] = o[1]
		od["n0"] = o[2]
		od["n1"] = o[3]
		od["n2"] = o[4]
		od["n3"] = o[5]
		od["n4"] = o[6]
		od["n5"] = o[7]
		od["n6"] = o[8]
		od["rnd"] = o[9]
		od["time"] = o[10]
		odict_list.append(od)
	return (mdict_list, odict_list)

def close(con, cur):
	cur.close()
	con.close()

