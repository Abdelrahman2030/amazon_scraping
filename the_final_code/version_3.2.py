'''
In this version i added the brand, and made in egypt column
'''
first_start_time = time.time() # This to calculate the time take for the program to run

import pandas as pd
from bs4 import BeautifulSoup
import requests
import time
import numpy as np


#Empty lists for the values
names_list = []
old_prices_list = []
new_prices_list = []
discount_list = []
rating_list = []
number_of_ratings_list = []
official_store_list = []
brand_list = []
made_in_egypt_list = []


'''
This program is the final product all of the web scraping process 
is in jupyter notebook
'''

# create a list with all of <div> tags that has the data of the 
# product inside of it
def products_in_page(url):

    '''
    This function is the main function of the program, it takes the url
    then it creates a soup then a list of all 40 products in the page
    then extracts these names, prices, etc
    '''

    content = requests.get(url).content
    soup = BeautifulSoup(content, "lxml")
    div_list = soup.find_all("div", class_ = "info") 
    # this creates a list with all 40 proucts

    for div in div_list:
        # this for loop extracts the names, prices, etc
        product_name = div.find("h3", class_ = "name").contents[0] # the name of the product

        if len(div.find_all(text = "Official Store")) != 0:
            '''
            This if statment identifes wither the product is a brand or not
            if it's a brand it will identify the brand becouse it's the first word in 
            the broduct name, and if the brand is american it will add eagle to it
            '''
            official_store_list.append("Official Store")
            brand_name = product_name.split()[0].lower()
            brand_list.append(brand_name)
        else:
            brand_name = "Not a brand"
            brand_list.append(brand_name)
            official_store_list.append("Non")
        

        price = div.find("div", class_ = "prc").contents[0]
        #I want to remove the EGP and "," to make it float
        price = price.split()[1]
        price = float(price.replace(",",""))


        try:
            old_price = div.find("div", class_ = "old").contents[0]
            old_price = old_price.split()[1]
            old_price = float(old_price.replace(",",""))
        except:
            old_price = price
    

        try:
            discount = div.find("div", class_ = "bdg _dsct _sm").contents[0]
            discount = int(discount.replace("%", ""))
        except:
            discount = 0
        

        try:
            rating = div.find("div", class_ = "stars _s").contents[0]
            rating = float(rating.split()[0])
        except:
            rating = np.nan


        try:
            rating_div_parent = str(div.find_all("div", class_ = "rev")[0]) # finds the div of the reviews
            rating_place = rating_div_parent.split()[8] # removed all the noise in the div
            number_of_ratings = rating_place.split("(")[1].split(")")[0] # splits the string many times
            # until we finish with the number of ratings
        except:
            number_of_ratings = 0
        
        #Now i will append these values into new lists
        names_list.append(product_name)
        old_prices_list.append(old_price)
        new_prices_list.append(price)
        discount_list.append(discount)
        rating_list.append(rating)
        number_of_ratings_list.append(number_of_ratings)


# Now this is the first part that will be exuted
# the url for jumia is the same excpet for the search key word
# so this part adjust the url and adds the key word to it
key_word = input("Please write your search key word: ")
url_key_word = key_word.replace(" ", "+")
url = "https://www.jumia.com.eg/catalog/?q={}".format(url_key_word)

products_in_page(url) # This runs the function for the first page
print("the total number of pages is 50")
print("first page done")

for index in range(2, 51):
    start_time = time.time() # to diplay the time taken by each page
    new_url = url + "&page={}#catalog-listing".format(index) # the url for each page

    products_in_page(new_url) # preform the function for the page

    end_time = time.time()
    time_taken = round(end_time - start_time, 2)
    print("{} page done, this took {} seconds".format(index, time_taken)) # display the time taken


search_rank = np.arange(1, len(names_list) + 1) # creates a search rank column

#Now i will create the data frame
dict_ = {"search_rank" : search_rank,
         "product_name": names_list,
         "old_price": old_prices_list,
         "discount": discount_list, 
         "current_price": new_prices_list,
         "rating": rating_list,
         "number_of_ratings" : number_of_ratings_list,
         "official_store" : official_store_list,
         "brand_name" : brand_list}
df = pd.DataFrame(dict_)
df.to_csv("{} data set.csv".format(key_word), index = False)


last_end_time = time.time()
total_time = round(last_end_time - first_start_time, 3)

print("total of {} produts".format(len(df)))
print("total time is {} seconds".format(total_time))

