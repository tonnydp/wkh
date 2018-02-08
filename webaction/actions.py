# coding=utf-8
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
import time
import random
import sys
from os import path


tab_bar_dict = {"home" : 0, "market": 1, "find": 2,"items" : 3,"mine" : 4}
goods_bar_dict = {"猴毛": 0, "蟠桃":1, "官方": 2}
order_dict = {"价格": 0, "代数":1, "体重":2, "生育":3}

def str_date():
	return time.strftime('%Y-%m-%d',time.localtime(time.time()))

def str_time():
	return time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

def login(driver, server_id, phone):
	
	pick_server_span = driver.find_element_by_css_selector('#app > div > div.section-1 > div > div.links > span.pickServer')
	pick_server_span.click()
	sleep(2)

	server_list_div = driver.find_element_by_css_selector('#app > div > div.server > div.server-list')
	server_a_list = server_list_div.find_elements_by_css_selector('a')
	if int(server_id) >= len(server_a_list):
		raise Exception("Wrong Server_Id Param of Login.")
	if server_a_list[server_id].get_attribute("class") != "green":
		raise Exception("The Server of" + server_id + " is not available.")

	#当前小猴数量：209591只
	mk_num_str_list = server_a_list[server_id].find_element_by_css_selector("span").get_attribute("innerHTML").split("：")
	if len(mk_num_str_list) == 2:
		mk_num = int(mk_num_str_list[1][:-1])
		print(mk_num)
	else:
		raise Exception("Error when get monkey number of server.")
	server_a_list[server_id].click()
	sleep(2)

	driver.execute_script("var elems=document.getElementsByClassName(\"weui-mask_transparent\");for(var i = 0; i < elems.length; i++){p=elems[i].parentNode;p.removeChild(elems[i]);}")

	driver.execute_script("var elems=document.getElementsByClassName(\"weui-mask_transparent\");for(var i = 0; i < elems.length; i++){p=elems[i].parentNode;p.removeChild(elems[i]);}")

	driver.execute_script("var elems=document.getElementsByClassName(\"weui-mask_transparent\");for(var i = 0; i < elems.length; i++){p=elems[i].parentNode;p.removeChild(elems[i]);}")

	checkboxes = driver.find_elements_by_css_selector('label') #label
	for checkbox in checkboxes:
		checkbox.click()
		sleep(1.3)

	button = driver.find_element_by_css_selector('button')
	print("DONE")	
	button.click()
	driver.implicitly_wait(10)

	next_button = driver.find_element_by_css_selector('#next')
	phone_input = driver.find_element_by_css_selector('#login div:nth-child(2) div div:nth-child(1) div:nth-child(2) input')
	phone_input.clear()
	phone_input.send_keys(phone)
	while next_button.get_attribute("disabled") == "true":
		sleep(1)
	sleep(1)
	next_button.click()

	while True:
		try:
			psw_input = driver.find_element_by_css_selector('#login div:nth-child(2) div div:nth-child(3) div:nth-child(2) input')
			break
		except:
			sleep(1)
			continue
	psw_input.send_keys("Aa19851201")
	login_button_parent = driver.find_element_by_css_selector('#login')
	buttons = login_button_parent.find_elements_by_css_selector('button')
	for button in buttons:
		if "登录" in button.get_attribute("innerHTML"):
			button.click()

	driver.implicitly_wait(10)

	#sleep(100)
	tabbars = driver.find_elements_by_css_selector("body > div#app > div.container > div[class='weui-tabbar tab'] > a[class^='weui-tabbar__item']")
	print(len(tabbars))
	if len(tabbars) == 5:
		return mk_num
	else:
		raise Exception("Login Failed.")

def click_tabbar(driver, tab_name):
	
	if tab_name not in tab_bar_dict.keys():
		raise Exception("Bad Tabbar Name.")
	tabbars = driver.find_elements_by_css_selector("body > div#app > div.container > div[class='weui-tabbar tab'] > a[class^='weui-tabbar__item']")
	if tabbars[tab_bar_dict[tab_name]].get_attribute("class") != "weui-tabbar__item weui-bar__item_on" :
		tabbars[tab_bar_dict[tab_name]].click()
		sleep(1)
def click_goods_tabbar(driver, tab_name):
	if tab_name not in goods_bar_dict.keys():
		raise Exception("Bad Goods Tabbar Name.")
	tabbars = driver.find_elements_by_css_selector("div.goods > div")
	tabbars[goods_bar_dict[tab_name]].click()
	sleep(1)

def is_goods_tabbar_active(driver, tab_name):
	if tab_name not in goods_bar_dict.keys():
		raise Exception("Bad Goods Tabbar Name.")
	tabbars = driver.find_elements_by_css_selector("div.goods > div")
	active_str = tabbars[goods_bar_dict[tab_name]].get_attribute("class")
	if active_str == "active":
		return True
	else:
		return False

def get_cur_tabbar(driver):
	tabbars = driver.find_elements_by_css_selector("body > div#app > div.container > div[class='weui-tabbar tab'] > a[class^='weui-tabbar__item']")
	if len(tabbars) != 4:
		raise Exception("Bad Tabbar State.")
	for index in range(len(tabbars)):
		if tabbars[index].get_attribute("class") == "weui-tabbar__item weui-bar__item_on" :
			return index
	return None

def set_market_order(driver, param, up=True):
	if get_cur_tabbar(driver) != 1:
		raise Exception("Wrong Tab to Get Order.")
	
	order_lis = driver.find_elements_by_css_selector("div#app > div.container > div.page > div.vux-sticky-box > div.filter > ul.order > li")
	if len(order_lis) != 4:
		raise Exception("Bad Market Order .")
	if param in order_dict.keys():
		if up == True:
			target_attr = "active up"
		else:
			target_attr = "active"
		while order_lis[order_dict[param]].get_attribute("class") != target_attr:
			order_lis[order_dict[param]].click()
			sleep(1)
	else:
		raise Exception("Bad Market Order Param")

def scroll_down(driver, x, y):
	driver.execute_script("window.scrollBy(0,document.body.scrollHeight);")

def find_items_in_market(driver):
	return driver.find_elements_by_css_selector("div#app > div.container > div.page > div.panel > div.item")

def get_owner_in_monkey_page(driver):
	if "/monkey/" in driver.current_url:
		return driver.find_element_by_css_selector('#app > div.page > div.panel > div.owner')
	else:
		raise Exception("Wrong Monkey Page.")
def click_zupu(driver):
	lis = driver.find_elements_by_css_selector("div#app > div.page > div.panel > div.category > div.filter > ul.status > li")
	if len(lis) == 4:
		lis[3].click()
	else:
		raise Exception("Wrong Zu pu tab.")

def wait_for_infin_bar_dispear(driver):
	while True:
		sleep(0.2)
		waiting_bar_divs = driver.find_elements_by_css_selector("div#app > div.page > div.panel > div.infinite-loading-container > div") 
		#print("%s" %(waiting_bar_divs[0].get_attribute("style"),))
		if waiting_bar_divs[0].get_attribute("style").endswith("display: none;"):
			break