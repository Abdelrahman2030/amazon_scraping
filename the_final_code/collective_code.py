# I will start by importing the main libraries

import pandas as pd 
import requests
import time
from bs4 import BeautifulSoup

#i will need to upload the other python files for
#sutra 
#Jumia

import sutra_function

keyword = input("Enter your keyword: ") #The search key words
keyword = keyword.replace(" ", "+")

sutra_df = sutra_function.main_sutra(keyword)
#No we have connected with sutra code, and have two things, first csv file
#seconde thinf sutra_df