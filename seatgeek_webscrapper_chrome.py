from bs4 import BeautifulSoup
from selenium import webdriver
import csv
import time

""" Insert the SeatGeek URL you desire at the url variable below and the scrapper
    will load up the page in Chrome. Include the path to your chromedriver.exe 
    file or the scrapper won't run"""
url = 'https://seatgeek.com/parking-chicago-bears-at-los-angeles-rams-tickets/parking/2019-11-17-5-20-pm/4961784'
browser = webdriver.Chrome(executable_path=r'C:\Users\Kevin Chrzanowski\Downloads\sel_chrome\chromedriver.exe')
browser.get(url)
time.sleep(5)

""" x_path to page element that is responsible for scrolling"""
x_path = '//*[@id="react-map"]/div/div[2]/div[1]/div/div[2]/div/div/div/div/div'

""" Three functions that are need to write the scrolldown command and then execute it """
def element_getter(x_path):
	javascript_element = "document.evaluate(" + "'" + str(x_path) + "'" + ", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue"
	return javascript_element

def element_height(element):
	scroll_height_script = element + '.scrollHeight'
	last_height = browser.execute_script('return ' + scroll_height_script)
	return last_height

def element_scrolldown(x_path):
	while True:
		height = element_height(element_getter(x_path))
		scroll_to_bottom_command = element_getter(x_path) + ".scrollTo(0," + str(height) + ')'
		browser.execute_script(scroll_to_bottom_command)
		time.sleep(1)
		new_height = element_height(element_getter(x_path))
		if height == new_height:
			break
		else:
			height = new_height

""" Three functions that scrape the html off the page and then make a list of ticket prices,
    ticket quantity, and a description of the parking location"""
def pageSource_getter():
	pageSource = browser.page_source
	return pageSource

def BS_builder(raw_page_data):
	bs = BeautifulSoup(raw_page_data,'html.parser')
	return bs

def text_and_tickets_and_price(content):
	price_list = []
	text_list = []
	ticket_list = []
	for dweep in content.findAll('span', attrs={'class':'omnibox__listing__buy__price'}):
		price_list.append(dweep.text)
	for tweep in content.findAll('div',attrs={'class':'omnibox__listing__section'}):
		text_list.append(tweep.text)
	for seep in content.findAll('span'):
		if 'ticket' in seep.text:
			ticket_list.append(seep.text)
	combo = list(zip(text_list,price_list,ticket_list))
	return combo

"""Exports a list of parking locations, ticket prices, and ticket quantity to csv format.
    Change the name of the csv file by editing the first parameter in the 'open' method."""
def data_to_csv(data_list):
	header =['Description','Prices','Ticket Quantity']
	with open('rams_seatgeek_parking_prices.csv','w', newline = '') as f:
		write = csv.writer(f)
		write.writerow(header)
		write.writerows(data_list)

"""Function that is responsible for driving the program"""
def main_driver():
	parking_page_content = pageSource_getter()
	refined_parking_page_content = BS_builder(parking_page_content)
	clean_parking_and_ticket_and_prices_list = text_and_tickets_and_price(refined_parking_page_content)
	data_to_csv(clean_parking_and_ticket_and_prices_list)
	browser.quit()

element_scrolldown(x_path)

main_driver()