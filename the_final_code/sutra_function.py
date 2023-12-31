#I will customize this code to work as a function that i can call in my main code

def main_sutra(keyword):


    import pandas as pd
    import numpy as np
    import requests
    from bs4 import BeautifulSoup
    import random
    import time

    user_agents_df = pd.read_csv('user_agents_list.csv')
    #This is the Fake user agent data set
    sutra_url = "https://sutrastores.com/en/search?type=product&options%5Bunavailable_products%5D=hide&options%5Bprefix%5D=last&q={}".format(keyword)

    titles_list = []
    old_prices_list = []
    new_prices_list = []
    discount_list = []
    sources_list = []
    searc_rank_list = []

    #The following list will be null just to merge this data set with jumia, as jumia set has the columns
    rating_list = []
    numer_of_ratings = []
    official_store_list =[]
    brand_name = []

    def response(url):
        #This function creates the request and it takes the url as input and returns the soup
        
        #user_agent = random.choice(user_agents_df["user_agent"]) #Fake user agent
        '''
        headers = {"User-Agent": user_agent,
               "Accept-Encoding":"gzip, deflate",
               "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
               "DNT":"1","Connection":"close",
               "Upgrade-Insecure-Requests":"1",
               "Accept-Language": "en-US,en;q=0.9"}
        '''
        page = requests.get(url) # the request is made here
        content = page.content
        
        soup = BeautifulSoup(content, "html.parser")
        
        return soup

    main_soup = response(sutra_url) #The main soup is the soup of page one


    def sutra(soup):
        '''
        This function takes the parameter soup then gives me all the desired results 
        from sutra
        '''


        #The next section is for the titles
        unc_titles_list = soup.find_all("h3", class_ = "t4s-product-title")
        search_rank = 1
        for index in unc_titles_list:

            titles_list.append(index.text)
        
            searc_rank_list.append(search_rank)
            search_rank = search_rank + 1
            # This for loop exctracts the product names

            #The next appends are to add null values to merge with jumia
            rating_list.append(np.nan)
            numer_of_ratings.append(np.nan)
            official_store_list.append("official_store")
            brand_name.append("sutra")
        
        #The next section is for prices
        unc_prices = soup.find_all("div", class_ = "t4s-product-price")
        
        for index in unc_prices:
            old_price = index.contents[0].text
            try:
            	old_price = float(old_price.split(" ")[1]) #This will reomve the LE from the price
            except:
            	old_price = (old_price.split(" ")[1])#some times there are values with commas. like 1,000
            	old_price = float(old_price.replace(",", ""))
            	
            old_prices_list.append(old_price)
            
            try:
                new_price = index.contents[1].text
                new_price = float(new_price.split(" ")[1]) #This will reomve the LE from the price
                new_prices_list.append(new_price)
            except:
                new_price = old_price
                new_prices_list.append(new_price)

            discount = round(((old_price - new_price) / old_price) * 100)
            discount_list.append(discount)
            
            sources_list.append("sutra") #This will help us later when we merge datasets, to know wich market this came from
     




    # now i will make this function works for all of the pages
    try:
        number_of_pages = int(main_soup.find_all("a", class_ = "t4s-pagination__item link")[-1].contents[0])
        print("the total number of pages in sutra is {}".format(number_of_pages))
        for index in range(2, number_of_pages + 1):
            #This loop will repeate the response and sutra function for all pages
            next_page_url = sutra_url + "&page={}".format(index) #This will create the link
           
            soup = response(next_page_url) #creates the soup
           
            sutra(soup) #To exctract the values
            print("Page: {}".format(index))

    except:
       print("number of pages is one")
       sutra(main_soup) 


        
    # This code will create the final data frame
    sutra_dict = {"search_rank" : searc_rank_list,
                "product_name" : titles_list,
                 "old_price" : old_prices_list,
                 "discount" : discount_list,
                 "new_price" : new_prices_list,
                 "rating" : rating_list,
                 "number_of_ratings" : numer_of_ratings,
                 "official_store" : official_store_list,
                 "brand_name" : brand_name,
                 "source" : sources_list}

    sutra_df = pd.DataFrame(sutra_dict)

    #sutra_df.to_csv("sutra_{}.csv".format(keyword), index = False)
    
    print("The total number of products in sutra is {}".format(len(searc_rank_list)))
    return sutra_df