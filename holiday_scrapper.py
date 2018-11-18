import requests

from bs4 import BeautifulSoup
import datetime
import csv
import time


headers = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5)",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "accept-charset": "cp1254,ISO-8859-9,utf-8;q=0.7,*;q=0.3",
    "accept-encoding": "gzip,deflate,sdch",
    "accept-language": "tr,tr-TR,en-US,en;q=0.8",
}

##Countries to be iterated upon
Country_name = ['uk','ireland','australia','new-zealand','malaysia','thailand','india','china','us','canada','brazil']

#Main Loop
def main():
	for y in range(0,1):
		Year = 2016
		for x in range(0,1):
			dataset = getHolidayDatesetByCountryAndYear(Country_name[x],str(Year))
			writeDatasetToCSV(dataset)
			Year = Year + 1
			time.sleep(2)

#write dataset to csv file
def writeDatasetToCSV(dataset):
	with open('holiday_file.csv', mode='a') as holiday_file:
		holiday_file = csv.writer(holiday_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		for val in dataset:
			holiday_file.writerow(val)


#Method to get holiday json datalist by country and year
def getHolidayDatesetByCountryAndYear(country,year):
	dataset = []
	with requests.Session() as session:
		session.headers = headers
		item_tr = []
		item_val = []
		item_td = []
	
		r = session.get('https://www.timeanddate.com/holidays/'+country+'/'+year, headers=headers)
		if r.status_code != 200:
			print("request denied")
		else:
			print("ok")
			soup = BeautifulSoup(r.text, "html.parser")
			items = soup.find_all(class_="zebra fw tb-cl tb-hover")
			#print(items[0].prettify())
			item_tr = items[0].find_all('tr')
			for val in item_tr:
				item_val = val.find_all(class_="nw")
				item_td = val.find_all('td')
				if len(item_val) > 0 and len(item_td) > 0:
					typeOfDay = item_td[2].text
					dateOfHoliday = datetime.datetime.strptime(str(item_val[0].text+" "+year), '%d %b %Y')
					dayOfHoliday = item_val[1].text
					nameOfHoliday = item_td[1].text
					data = [dateOfHoliday.isoformat(),dayOfHoliday,nameOfHoliday,typeOfDay]
					dataset.append(data)
	return dataset

if __name__ == '__main__':
	main()