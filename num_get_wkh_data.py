# coding=utf-8
from selenium import webdriver
from time import sleep
import time
import random
import sys
from os import path



from webaction.actions import *
from webparser.parser import *
import mysqlite.sql as sql
import utils.timeutils as tu


if len(sys.argv) >= 2:
	if sys.argv[1] == "prod":
		MODE = "PROD"
	elif sys.argv[1] == "debug":
		MODE = "DEBUG"
	else:
		raise Exception("Bad Cmd Param!")
	if sys.argv[2] == "0":
		SERVER_ID = 0
	elif sys.argv[2] == "1":
		SERVER_ID = 1
	else:
		raise Exception("Bad Cmd Param!")
	if len(sys.argv) == 4 and MODE == "DEBUG":
		start_id = int(sys.argv[3])
	else:
		start_id = 0

else:
	raise Exception("Bad Cmd Param!")

if MODE == "PROD":
	phone = "17896007887"
if MODE == "DEBUG":
	phone = "17896025920"
if SERVER_ID == 0:
	mk_url = "http://0.monkey.plus/monkey/"
if SERVER_ID == 1:
	mk_url = "http://wkc.monkey.plus/monkey/"
final_mk_id = 0
try:
	
	(con, cur) = sql.init_db("..\\data\\num_wkh.db")
	driver = webdriver.Chrome()
	driver.get('http://monkey.plus/')
	driver.implicitly_wait(10)
	mk_num = login(driver, SERVER_ID, phone)
	print(str(mk_num) + " We got!")
	if MODE == "PROD":
		print("请设置为无图模式。")
		sleep(40)
	while True:
		(rnd, cur_mk_id) = sql.get_cur_round(cur)
		if start_id > 0:
			cur_mk_id = start_id
		print(str(rnd) + " " + str(cur_mk_id))
		
		(count, monkey_list, owner_list) = sql.get_mk_list(cur, rnd)
		# print(monkey_list)
		# print(owner_list)
		bad_owner_list = []
		bad_monkey_list = []		

		for i in range(cur_mk_id, mk_num + 1):
			if i in monkey_list:
				continue
			t0 = time.time()
			tu.restart_time_elps(1)
			driver.get(mk_url + str(i))
			driver.implicitly_wait(10)
			tu.log_time_elps(1, "OPEN WEB PAGE")
			try:
				svg404 = driver.find_element_by_css_selector('html > body > div.app > div.page > svg.me404')
				print("Not get data from " + str(i))
				cur.execute("INSERT INTO BadMonkey VALUES(?,?,?,?)",(i, rnd, "404_FAILURE", str_time()))
				con.commit()
				continue
			except:
				pass
			try:
				
				tu.log_time_elps(1, "SEARCH FOR 404")
				owner = get_owner_in_monkey_page(driver)
				owner.click()
				#change to sleep 2 sec 2018-01-29
				wait_for_infin_bar_dispear(driver)
				owner_info = parse_owner_info(driver)
				owner_info["time"] = str_time()
				for ii in range(7):
					owner_info["n" + str(ii)] = 0
				tu.log_time_elps(1, "PARSE ONWER INFO")
			except Exception as e:
				owner_info = {"name": "NONE", "addr": "NONE"}
				print(e)
				print("BAD OWNER PAGE BUT CONTINUED! " + str(i))
			if owner_info["addr"] not in owner_list and owner_info["addr"] != "NONE":
				monkeys_of_owner = parse_owner_monkeys(driver)
				mk_data = []
				tu.log_time_elps(1, "PARSE MK")
				for m in monkeys_of_owner:
					int_id = int(m["id"])
					if int_id > mk_num:
						mk_num = int_id
					monkey_list.append(int_id)
					m["owner_addr"] = owner_info["addr"]
					m["rnd"] = rnd
					m["time"] = str_time()
					mk_data.append((m["id"], m["gen"], m["cz"], m["sy"], m["jj"], m["kg"], m["price_type"], m["price"], m["owner_addr"],m["rnd"], m["time"]))			
					owner_info["n" + str(m["gen"])] = owner_info["n" + str(m["gen"])] + 1
				tu.log_time_elps(1, "INSERT MK")
				cur.executemany("insert into Monkey (id, gen, cz, sy, jj, kg, price_type, price, owner_addr, rnd, time)values(?,?,?,?,?,?,?,?,?,?,?)", mk_data)
				owner_info["rnd"] = rnd

				cur.execute("insert into Owner values(:name, :addr, :n0, :n1, :n2, :n3, :n4, :n5, :n6, :rnd, :time)", owner_info)
				con.commit()
				owner_list.append(owner_info["addr"])
				owner_info_p = owner_info
				del owner_info_p["addr"]
				del owner_info_p["time"]
				print(str(i) + "\t" + str(len(monkeys_of_owner)) + "\t" + str(owner_info_p))
				print("Mk: " + str(len(monkey_list)) + "\tOwner: " + str(len(owner_list)))
				final_mk_id = i
				tu.log_time_elps(1, "INSERT OWNER")
			else:
				
				if owner_info["addr"] in owner_list:
					if owner_info["addr"] not in bad_owner_list:
						bad_owner_list.append(owner_info["addr"])
						cur.execute("INSERT INTO BadOwner VALUES(?, ?, ?, ?)", (owner_info["addr"], rnd, "NOT_COMPLETE", str_time()))
						
				else:
					cur.execute("INSERT INTO BadOwner VALUES(?, ?, ?, ?)", (owner_info["addr"], rnd, "BAD_OWNER_PAGE", str_time()))
			total_t = time.time() - t0
			print("Time for this Owner is %.2f. Avg time is %.4f." % (total_t, total_t/len(monkeys_of_owner)))
		
		print("%d round finished at %s. Got %d Monkeys." % (rnd, str_time(), mk_num))
		cur.execute("INSERT INTO Round values(?, ?, ?, ?)", (rnd, 1, final_mk_id, str_time()))
finally:
	if final_mk_id != 0:
		if final_mk_id != mk_num:
			state = 0
		else:
			state = 1
		cur.execute("INSERT INTO Round values(?, ?, ?, ?)", (rnd, state, final_mk_id, str_time()))
	con.commit()
	driver.quit()
	cur.close()
	con.close()

