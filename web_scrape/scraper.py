import json
import requests
from bs4 import BeautifulSoup as bs

# dictionary object to store all companies' info, to be dumped into JSON
results = {}

# iterate from '/?page=1' through '?/page=10'
for x in range (1, 11):
	
	'''
	iterate through all links to individual company pages,
	as contained in the table on each '/?page=x'
	'''
	for link in bs(requests.get('http://data-interview.enigmalabs.org/companies/?page=%s' % x).text, 'html.parser').tbody('a'):
		
		# company info, as contained in the table on each individual company page
		company = bs(requests.get('http://data-interview.enigmalabs.org' + link.get('href')).text, 'html.parser').tbody
		
		# list to store raw company text data
		data = []
		
		'''
		iterate through CSS selectors for all necessary fields;
		append text to the 'data' list
		'''
		for field in ['#street_address', '#street_address_2', '#city', '#state', '#zipcode', '#phone_number', '#website', '#description']:
			
			# slice start index (will be variable based on len(id))
			start = len(field) + 9
			
			# append sliced field text to raw company data list
			data.append(str(company.select(field)[0])[start:-5])
		
		# dictionary object populated with company info
		info = {
			'Address Line 1': data[0],
			'Address Line 2': data[1],
			'City': data[2],
			'State': data[3],
			'Zipcode': data[4],
			'Phone': data[5],
			'Company Website': data[6],
			'Company Description': data[7]
		}
		
		# add each company's 'info' dictionary to the 'results' dictionary
		results[str(company.select('#name')[0])[14:-5]] = info

# dump 'results' dictionary to a new 'solution.json' file
with open('solution.json', 'w') as fp:
	json.dump(results, fp, sort_keys=True, indent=2)
	