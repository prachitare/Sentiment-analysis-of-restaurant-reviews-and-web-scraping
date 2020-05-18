
from bs4 import BeautifulSoup
import requests
import re
import csv
import pandas as pd

base_url_1 = "https://www.tripadvisor.in/Restaurant_Review-g304551-d13388460-Reviews-or"
i = 00
base_url_2 = "-Kitchen_With_A_Cause-New_Delhi_National_Capital_Territory_of_Delhi.html"

#demo_url = base_url_1 + str(i) + base_url_2

url_list = []
for i in range(0, 220, 10):
	url = base_url_1 + str(i) + base_url_2
	url_list.append(url)

#####################################
# MAIN LOOP
#####################################
for k in url_list:
	print k
	r = requests.get(k)
	soup = BeautifulSoup(r.content, 'html5lib')

	#### REVIEW TEXT
	site_name = "Trip Advisor"
	site_name_list = []
	s_txt = soup.findAll("div", {"class": "entry"})
	s_txt_new = []
	for i in s_txt:
		new_txt = str(i).replace("""<div class="entry">""", '')
		new_txt = new_txt.replace("</div>", '')
		new_txt = new_txt.replace("\n", '')
		new_txt = new_txt.replace("""<p class="partial_entry">""", '')
		new_txt = new_txt.replace("</p>", '')
		s_txt_new.append(new_txt)
		site_name_list.append(site_name)
	#print len(s_txt_new)

	#### REVIEW TITLE
	s_title = soup.findAll('span', {"class": "noQuotes"}, text = True)
	s_title_new = []
	for i in s_title:
		new_title = str(i).replace("""<span class="noQuotes">""", '')
		new_title = new_title.replace("</span>", '')
		s_title_new.append(new_title)
	#print len(s_title_new)

	#### REVIEW DATE
	s_date = soup.findAll('span', {"class" : "ratingDate"}, text = True)
	s_date_new = []
	for i in s_date:
		new_date = str(i).split("Reviewed ",1)[1]
		new_date = new_date.replace("</span>", '')
		s_date_new.append(new_date)
	#print len(s_date_new)

	#### REVIEW RATING
	rating = ''
	bigbox = soup.find("div", {"id": "REVIEWS"})
	s_rvw = bigbox.findAll('span', {"class" : "ui_bubble_rating"})
	s_rvw_new = []
	for i in s_rvw:
		new_rvw = str(i).replace("</span>", '')
		if 'bubble_50' in new_rvw:
			rating = 'Excellent'
		elif 'bubble_40' in new_rvw or 'bubble_35' in new_rvw:
			rating = 'Very Good'
		elif 'bubble_30' in new_rvw or 'bubble_25' in new_rvw:
			rating = 'Average'
		elif 'bubble_20' in  new_rvw or 'bubble_15' in new_rvw:
			rating = 'Poor'
		elif 'bubble_10' in new_rvw or 'bubble_05' in new_rvw:
			rating = 'Terrible'
		s_rvw_new.append(rating)
	#print s_rvw_new

	### INSERT INTO CSV
	with open('data.csv', 'a') as f:
	    writer = csv.writer(f)
	    writer.writerows(zip(site_name_list, s_rvw_new, s_title_new, s_date_new, s_txt_new))

colnames=['Site', 'Rating', 'Review Title', 'Review Date', 'Review Paragraph'] 
modified = pd.read_csv('data.csv', names=colnames, header=None)
