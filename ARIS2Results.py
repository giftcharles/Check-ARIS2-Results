#!/usr/bin/env python

__author__ = "Gift C. Nakembetwa"
__copyright__ = "Copyright 2019"
__credits__ = ["Gift C. Nakembetwa"]
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "Gift C. Nakembetwa"
__email__ = "giftnakembetwa@gmail.com"
__status__ = "Development"


import time # Standard Library
from random import randint
import os

from selenium import webdriver # 3rd party modules
from selenium.webdriver.common.keys import Keys

try:
	import credentials # local modules
except:
    print("\n>> You did not create a credentials.py file, Read the instructions on the Github page again\n\n")
    raise

def compare_last_table(htmlString):
    try:
        with open(f"result_table.html", "r", encoding="utf8") as f:
            old_html = f.read()

        #print(f"old_html: {len(old_html)}")
        #print(f"htmlString: {len(htmlString)}")
        
        if len(old_html)==len(htmlString):
            return True
    except Exception as e:
        print(f"{e}")
    
    return False    
    

def navigate_aris_user(USERNAME, PASSWORD):
    """
    This function takes a user's aris account details,
    logs into their account and checks if new results
    are published by comparing the length of the old
    saved table Html and the length of the current result 
    table html. 
    
    """
    start_time= time.time()
    aris_url = r"https://aris2.udsm.ac.tz/index.php"
    driver = webdriver.Chrome()
    try:
        driver.get(aris_url)

        if "ARIS" not in driver.title:
            print("could not reach the website, sleeping...")
            driver.close()
            return True
    

        username_input = driver.find_element_by_name("username")
        time.sleep(randint(1,3))
        password_input = driver.find_element_by_name("password")
        time.sleep(randint(1,3))
        login_button = driver.find_element_by_css_selector("input[type=\"submit\"]")
        time.sleep(randint(1,4))

        username_input.send_keys(USERNAME)
        password_input.send_keys(PASSWORD)
        login_button.click()
        time.sleep(randint(1,4))

        driver.find_element_by_link_text('Course Results').click()
        time.sleep(randint(1,4))

        driver.find_element_by_css_selector("table td ul li a:last-child").click()
        time.sleep(randint(1,4))

        table_results = driver.find_element_by_css_selector("table:nth-child(2) td:nth-child(2)")

        htmlString = table_results.get_attribute('innerHTML')
    
    except Exception as e:
        print(f">> {e} -> A problem has occured while navigating with selenium")
        driver.close()
        return True

    if compare_last_table(htmlString):

        with open("result_table.html", "w", encoding="utf8") as f:
            f.write(htmlString)

        print("No change in the results table")
        driver.close()
        return True

    else:

        with open("full_results.html", "w", encoding="utf8") as f:
            f.write(driver.page_source)

        print(">> Change was detected in the results table")
        print(f"saved html in {os.path.join('file://', os.getcwd(), 'full_results.html')}")
        driver.close()
        return False

    print(f"The script ran for {int(time.time()-start_time)}s")    
 
if __name__ == "__main__":
    # Do not touch anything from this point
    username=credentials.__username__
    password=credentials.__password__
    wait_time=credentials.__waittime__

    print(f">> ID Number: {username}\n>> password: {'*' * len(password)}")
    
    while navigate_aris_user(username, password):
        if wait_time==0:
            sleep_time = randint(43200, 86400)
            print(f"Sleeping for {int(sleep_time)}s")
            time.sleep(sleep_time)
        else:
            print(f"Sleeping for {int(wait_time)}s")
            time.sleep(wait_time)

        


    
        
