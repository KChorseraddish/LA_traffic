from selenium import webdriver
from bs4 import BeautifulSoup
import csv
import time

"""Insert the Stubhub parking page url to the url variable below and the scrapper will start up Google Chrome. 
   Include the path to your chromedriver.exe file or else the scrapper won't run"""
url = 'https://www.stubhub.com/los-angeles-rams-tickets-los-angeles-rams-los-angeles-los-angeles-coliseum-parking-lots-11-17-2019/event/104119463/'
browser = webdriver.Chrome(executable_path=r<YOUR_PATH_TO_CHROMEDRIVER.EXE>)
browser.get(url)
time.sleep(10)

"""The next three functions select the scrolling element on the page and scroll to its bottom."""
def javascript_element_getter(element_name):
	javascript_table = "document.getElementById(" + "'" + element_name + "'" + ")"
	return javascript_table

def javascript_element_height(element_name):
	scroll_height_script = javascript_element_getter(element_name) + '.scrollHeight'
	last_height = browser.execute_script('return ' + scroll_height_script)
	return last_height

def javascript_element_scrolldown(element_name):
	while True:
		height = javascript_element_height(element_name)
		scroll_to_bottom_command = javascript_element_getter(element_name) + ".scrollTo(0," + str(height) + ')'
		browser.execute_script(scroll_to_bottom_command)
		time.sleep(1)
		new_height = javascript_element_height(element_name)
		if height == new_height:
			break
		else:
			height = new_height

"""The next three functions scrape the webpages HTML code and return the desired information"""
def bottom_pagesource(element_name):
	javascript_element_scrolldown(element_name)
	pageSource = browser.page_source
	return pageSource

def BeautifulSoup_Page_Bottom_HTML_Scrape(element_name):
	element_bottom = bottom_pagesource(element_name)
	bs = BeautifulSoup(element_bottom,'html.parser')
	return bs

def raw_HTML_element_filter(raw_list):
	new_list = []
	for i in raw_list:
		new_list.append(i.text)
	return new_list

""" Function that drives the script. It uses the above functions to process the webpage and outputs
    a CSV file with ticket price, ticket quantity, and parking location description."""
def main_driver(element_name):
	str_element_name = str(element_name)
	total_page_content = BeautifulSoup_Page_Bottom_HTML_Scrape(str_element_name)
	
	pricelist_raw= total_page_content.findAll('div',attrs={'class':'dollar-value partials'})
	ticketlist_raw = total_page_content.findAll('div', attrs={'class':'ticketsText'})
	parking_location_raw = total_page_content.findAll('div', attrs={'class':'sectioncell'})

	ticketlist = raw_HTML_element_filter(ticketlist_raw)
	parking_location_list = raw_HTML_element_filter(parking_location_raw)
	pricelist = raw_HTML_element_filter(pricelist_raw)

	combo = list(zip(pricelist,ticketlist,parking_location_list))
	header= ['Prices','Tickets','Parking Location']
	with open('rams_stubhub_parking_prices.csv','w', newline ='') as f:
		write = csv.writer(f)
		write.writerow(header)
		write.writerows(combo)
	browser.quit()

main_driver('ticketlist_container')