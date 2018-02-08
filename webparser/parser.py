from selenium import webdriver
from time import sleep
import time
import random
import sys
from os import path

from webaction.actions import *
import utils.timeutils as tu

def parse_owner_info(driver):
	if "/profile/" in driver.current_url:
		owner_name = driver.find_element_by_css_selector("div#app > div.page > div.head > h1").get_attribute("innerHTML")
		owner_addr = driver.find_element_by_css_selector("div#app > div.page > div.head > div.address").get_attribute("innerHTML")
		if owner_name == "" or owner_addr == "":
			raise Exception("Bad Owner Parse.")

		return {"name": owner_name, "addr": owner_addr}
	else:
		raise Exception("Bad Owner Page.")

def parse_owner_monkeys(driver):
	if "/profile/" in driver.current_url:
		m_list = list()
		prev_len = 0
		items = driver.find_elements_by_css_selector('div#app > div.page > div.panel > div.item')
		if len(items) > 19:
			while True:
				last_item = items[-1]
				driver.execute_script("arguments[0].scrollIntoView();", last_item)
				wait_for_infin_bar_dispear(driver)
				items = driver.find_elements_by_css_selector('div#app > div.page > div.panel > div.item')
				if len(items) == prev_len:	
					break
				prev_len = len(items)
		tu.log_time_elps(1, "SCROLL ALL MK")
		for item in items:
			m_info = parse_monkey_info_in_owner_page(driver, item)
			m_list.append(m_info)
		return m_list

	else:
		raise Exception("Bad Owner Page.")


def parse_monkey_info_in_owner_page(driver, item):
	id_m = parse_id(item)
	sy = 0.0
	price_type = "-"
	price = 0
	ps = item.find_elements_by_css_selector('div.img > div.info > p')
	info_p = None
	if len(ps) == 2:
		price_type = parse_price_type(ps[0].find_element_by_css_selector("i").get_attribute("class"))
		price = parse_price(ps[0].find_element_by_css_selector("span").get_attribute("innerHTML"))
		info_p = ps[1]
	if len(ps) == 1:
		info_p = ps[0]
	spans = info_p.find_elements_by_css_selector("span")
	cz = parse_attr_str(spans[0].get_attribute("innerHTML"))
	if len(spans) == 2:
		(jj, kg) = parse_attr_kg_str(spans[1].get_attribute("innerHTML"))
	elif len(spans) == 3:
		sy = parse_attr_str(spans[1].get_attribute("innerHTML"))
		(jj, kg) = parse_attr_kg_str(spans[2].get_attribute("innerHTML"))
	gen = parse_gen(item.find_element_by_css_selector("div.price").get_attribute("innerHTML"))
	return {"id": id_m, "gen": gen, "cz": cz, "sy": sy, "jj": jj, "kg": kg, "price_type": price_type, "price": price}

def parse_id(item):
	id_str = item.find_element_by_css_selector('div.img > div.id').get_attribute("innerHTML")
	id_list = id_str.split(" ")
	id_m = id_list[1]
	return int(id_m)

def parse_price(price_str):
	price_list = price_str.split(" ")
	return float(price_list[0])

def parse_price_type(class_str):
	if "love" in class_str:
		price_type = "love"
	elif "sell" in class_str:
		price_type = "sell"
	else:
		raise Exception("Wrong Price Type.")
	return price_type

def parse_attr_str(attr_str):
	return float(attr_str[:-1])
#1.10 · 0kg
def parse_attr_kg_str(attr_kg_str):
	akglist = attr_kg_str.split(" · ")
	attr = akglist[0]
	kg = akglist[1][:-2]
	return (float(attr), float(kg))
def parse_gen(gen_str):
	gen_list = gen_str.split(" ")
	return int(gen_list[0])

def parse_cur_monkey_id(driver):
	if "/monkey/" in driver.current_url:
		l = driver.current_url.split("/")
		return l[2]
	else:
		raise Exception("Not A Monkey Page To Parse Id.")
def parse_monkeys_of_zupu(driver):
	cur_id = parse_cur_monkey_id(driver)
	monkey_list = []
	parsed_monkey_items = driver.find_elements_by_css_selector("a[href^='/monkey/']")
	for m in parsed_monkey_items:
		url = m.get_attribute("href")
		
		l = url.split("/")
		print(l)
		m_id = l[4]
		if m_id != cur_id:
			print(m_id)
			img = m.find_element_by_css_selector("img")
			monkey_list.append((m_id, img))
	return monkey_list

###############################################################
#Goods Parser
###############################################################

def parse_goods_price(driver, goods_type, last_state):
	price_trs = driver.find_elements_by_css_selector("div.panel> table > tbody > tr")
	if len(price_trs) != 11:
		raise "Wrong Price Table! Len of Trs is %d" % (len(price_trs),)
	price_data_list = []
	while True:
		price_data_list = []
		t_str = str_time()
		for i in range(11):
			if i != 5:
				tds = price_trs[i].find_elements_by_css_selector("td")
				if len(tds) != 4:
					raise "Wrong Price Table Len of TDS is %d" % (len(tds),)
				name = tds[0].get_attribute("innerHTML")
				mount = int(tds[1].get_attribute("innerHTML"))
				price_str = tds[2].get_attribute("innerHTML")
				price_type = price_str.split(" ")[1]
				price = float(price_str.split(" ")[0])
				if i in range(5):
					bid_type = "SELL"
				else:
					bid_type = "BUY"
				price_data_list.append((t_str, name, mount, price, price_type, bid_type, goods_type))
		(n,m,last_p) = last_state
		if len(price_data_list) != 10 or (last_p > price*0.5 and last_p < price*1.5):
			print("*****ONCE AGAIN!*******")
			sleep(1)
		else:
			last_state = (name, mount, price)
			break
	return (price_data_list, last_state)
