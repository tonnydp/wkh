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
	
	(con, cur) = sql.init_db_goods("..\\data\\goods_wkh.db")
	driver = webdriver.Chrome()
	driver.get('http://monkey.plus/')
	driver.implicitly_wait(10)
	mk_num = login(driver, SERVER_ID, phone)
	if MODE == "PROD":
		driver.get('chrome://settings/content/images')
		sleep(10)

	click_tabbar(driver, "items")
	goods_tabbar_list = ["猴毛", "蟠桃"]
	tabbar_list_index = 0
	last_state = ("", 0, 0.0)
	while True:
		if tabbar_list_index >= len(goods_tabbar_list):
			tabbar_list_index = 0
		click_goods_tabbar(driver, goods_tabbar_list[tabbar_list_index])
		if is_goods_tabbar_active(driver, goods_tabbar_list[tabbar_list_index]):
			(goods_data, last_state) = parse_goods_price(driver, goods_tabbar_list[tabbar_list_index], last_state)
			for g in goods_data:
				print(g)
			print("************************************")
			sql.insert_goods_data(cur, goods_data)
			con.commit()
			sleep(1)
		else:
			continue


		tabbar_list_index = tabbar_list_index + 1


	
finally:
	
	con.commit()
	driver.quit()
	cur.close()
	con.close()

