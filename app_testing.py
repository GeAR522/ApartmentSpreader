#!python3
import os
import pprint
import urllib.request
import webbrowser

import requests
from bs4 import BeautifulSoup as bs
import re
import pandas as pd


def propDets(link):
    PropURL = link
    page = urllib.request.urlopen(PropURL)
    propSoup = bs(page, features='lxml') # the base website we are searching on being made into a soup object
    roomPage = propSoup.body.findAll('span') # searches for all 'span' tags which include the details
    roomCounts = re.findall('>\d<|>-<', str(roomPage)) # this searches specifically for digits inbetween the tags
    del roomCounts[4:] # delete all the numbers after the first 3, as they are other apartments
    for Num in roomCounts:
        Ix = roomCounts.index(Num) # gets the index of the entry
        En = str(Num).strip('<').strip('>')   # strips the entry, and creates as separate strong
        roomCounts[Ix] = En    # replaces previous list entry with striped string
    return roomCounts


#
#
#
#propDets('https://www.places.je/property/20863')
#
#print(roomCounts)
#



