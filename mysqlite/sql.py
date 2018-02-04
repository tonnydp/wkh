# coding=utf-8
import sqlite3
from time import sleep
import time
import random
import sys
from os import path

def init_db(db_path):
	con = sqlite3.connect(db_path)
	cur = con.cursor()

	#{"id": id_m, "gen": gen, "cz": cz, "sy": sy, "jj": jj, "kg": kg, "p_type": price_type, "price": price}
	create_mk_tb_cmd='''
        CREATE TABLE IF NOT EXISTS Monkey 
        (id INT, 
         gen INT, 
         cz REAL,
         sy REAL,
         jj REAL,
         kg REAL,
         price_type TEXT,
         price REAL,
         owner_addr TEXT,
         rnd INT,
         time TEXT); 
        '''  
	cur.execute(create_mk_tb_cmd)

	create_owner_tb_cmd='''
        CREATE TABLE IF NOT EXISTS Owner 
        (name TEXT, 
         addr TEXT,
         n0 INT,
         n1 INT,
         n2 INT,
         n3 INT,
         n4 INT,
         n5 INT,
         n6 INT,
         rnd INT,
         time TEXT);  
        '''  
	cur.execute(create_owner_tb_cmd)

	create_round_tb_cmd = '''
        CREATE TABLE IF NOT EXISTS Round 
        (id INT, 
         ok INT,
         cur_mk_id INT,
         time TEXT);  
        '''  
	cur.execute(create_round_tb_cmd)

	create_bad_owner_tb_cmd = '''
        CREATE TABLE IF NOT EXISTS BadOwner 
        (addr TEXT, 
         rnd INT,
         type TEXT,
         time TEXT);  
        '''  
	cur.execute(create_bad_owner_tb_cmd)

	create_bad_monkey_tb_cmd = '''
        CREATE TABLE IF NOT EXISTS BadMonkey 
        (id TEXT, 
         rnd INT,
         type TEXT,
         time TEXT);  
        '''  
	cur.execute(create_bad_monkey_tb_cmd)

	return (con, cur)

def get_mk_list(cur, rnd):
	print("Start!")
	t = time.time()
	count_obj = cur.execute("SELECT COUNT(id) FROM Monkey WHERE rnd=?", (rnd,))
	count = count_obj.fetchone()[0]
	mk_list = []
	print("SELECT MK COUNT %.3f." % (time.time() - t,))
	t = time.time()
	mk_max = 0
	if count > 0:
		cur.execute("SELECT id FROM Monkey WHERE rnd=?", (rnd,))
		print("SELECT MK ID * %.3f." % (time.time() - t,))
		t = time.time()
		id_list = cur.fetchall()
		print("FETCH ALL MK %.3f." % (time.time() - t,))
		t = time.time()
		mk_set = set()
		for id_tuple in id_list:
			# if id_tuple[0] not in mk_list:
			# 	mk_list.append(id_tuple[0])
			if id_tuple[0] > mk_max:
				mk_max = id_tuple[0]
			mk_set.add(id_tuple[0])
		mk_list = list(mk_set)
		print("ADD ALL MK %.3f." % (time.time() - t,))
		t = time.time()
	count_obj = cur.execute("SELECT COUNT(addr) FROM Owner WHERE rnd=?", (rnd,))
	count = count_obj.fetchone()[0]
	owner_list = []
	print("SELECT OW COUNT %.3f." % (time.time() - t,))
	t = time.time()
	if count > 0:
		cur.execute("SELECT addr FROM Owner WHERE rnd=?", (rnd,))
		print("SELECT OW ID * %.3f." % (time.time() - t,))
		t = time.time()
		id_list = cur.fetchall()
		print("FETCH ALL OW %.3f." % (time.time() - t,))
		t = time.time()
		for id_tuple in id_list:
			if id_tuple[0] not in owner_list:
				owner_list.append(id_tuple[0])
		print("ADD ALL OW %.3f." % (time.time() - t,))
	return (mk_max, mk_list, owner_list)

#(id INT,  ok INT,cur_mk_id INT,time TEXT); 
def get_cur_round(cur):
	count_obj = cur.execute("SELECT COUNT(id) FROM Round")
	count = count_obj.fetchone()[0]
	if count == 0:
		return (1, 1)
	cur.execute("SELECT id FROM Round WHERE ok=1")
	rnd_list = cur.fetchall()
	rnd = 0
	cur_mk_id = -1
	for rnd_tuple in rnd_list:
		if rnd_tuple[0] > rnd:
			rnd = rnd_tuple[0]
	cur.execute("SELECT cur_mk_id FROM Round WHERE id=?", (rnd + 1,))
	cur_mk_id_list = cur.fetchall()
	if cur_mk_id_list == []:
		return (rnd + 1, 1)
	else:
		cur_mk_id = -1
		for mid in cur_mk_id_list:
			if mid[0] > cur_mk_id:
				cur_mk_id = mid[0]
		return (rnd + 1, cur_mk_id)









