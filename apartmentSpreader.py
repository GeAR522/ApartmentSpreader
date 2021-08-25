#!python3
import os
import pprint
import urllib.request
import webbrowser

import requests
from bs4 import BeautifulSoup as bs
import re
import pandas as pd
import app_testing as at
import openpyxl as px


URL = 'https://www.places.je/propertysearch/residential-rent?propertyCategoryId=2&type=2&type=5&type=3&type=4&parish=4&sortBy=price-asc'
page = urllib.request.urlopen(URL)

soup = bs(page, features='lxml')  # the base website we are searching on being made into a soup object

strongPage = soup.body.findAll('strong')  # searching the bold items as the prices are bold
function_Page = re.findall('£\d.\d+', str(strongPage))  # within the bold, searching for a price using regex

linkPage = soup.body.findAll('a')  # searching base page for all tags with 'a'
hrefPage = re.findall('property/.....', str(linkPage))  # finding the property tag, which is also link ending

linkList = []  # create empty list for the links of properties
for props in hrefPage:  # this runs through the collected property ids and makes them into full HREF links
    fulLink = f'https://www.places.je/{props}'
    linkList.append(fulLink)  # and then adds them to the empty list

PropTails = []  # empty list for bedrooms, bathrooms, receptions, parking of each property
for link in linkList:
    tbE = at.propDets(link)  # using app_testing file to store the function for info
    PropTails.append(tbE)  # appending list entries to main list, in order. for dataframe

bedrooms = []  # empty lists for ease of df creation
bathrooms = []
receptions = []
parking = []

for ro in PropTails:
    bedrooms.append(PropTails[PropTails.index(ro)][0]) #cycling each list entry to add the entries to the appropriate list
    bathrooms.append(PropTails[PropTails.index(ro)][1])
    receptions.append(PropTails[PropTails.index(ro)][2])
    parking.append(PropTails[PropTails.index(ro)][3])

propsData = pd.DataFrame(
    {'Property Price': function_Page, 'Bedrooms': bedrooms, 'Bathrooms': bathrooms,
     'Receptions': receptions, 'Parking': parking, 'Property Link': linkList})
propsData = propsData.drop([0], axis=0)  # removes row 0 as it is the bonus property shown on every page

propsData.to_excel('Cheapest Rentals in St. Helier.xlsx')


#pprint.pprint(propsData)

'''was trying to get auto column fit to work'''

#writer = pd.ExcelWriter('Cheapest Rentals in St. Helier.xlsx')
#propsData.to_excel(writer, sheet_name='Rentals', index=False, na_rep='NaN')
#
## Auto-adjust columns' width
#for column in propsData:
#    column_width = max(propsData[column].astype(str).map(len).max(), len(column))
#    col_idx = propsData.columns.get_loc(column)
#    writer.sheets['Rentals'].set_column(col_idx, col_idx, column_width)
#
#writer.save()
#
#print(parking)