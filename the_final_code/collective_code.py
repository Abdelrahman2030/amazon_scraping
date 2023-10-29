# I will start by importing the main libraries

import time
import pandas as pd 
import sutra_function  #to import thr function of sutra
import jumia_function

start_time = time.time()
#i will need to upload the other python files for
#sutra 
#Jumia


keyword = input("Enter your keyword: ") #The search key words
keyword = keyword.replace(" ", "+")
print(keyword)

sutra_df = sutra_function.main_sutra(keyword)
#Now we have connected with sutra code, and have two things, first csv file
#second thing sutra_df



jumia_df = jumia_function.jumia_main(keyword)

end_time = time.time()

time_taken = (end_time - start_time) / 60
print("the total time taken of the collective code is {} minutes".format(time_taken))
