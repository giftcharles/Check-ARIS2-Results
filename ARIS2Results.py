#!/usr/bin/env python

"""
Check ARIS2 Results
Periodically check for results update published on the 
ARIS website for any given account/student

How to use
1 Create credentials.py file.

2 Add three variables, __username__, __password__ and __waittime__.
The __username__ variable takes your ARIS2 ID as a value,
 the __password__ variable obviously takes your password and the 
__waittime__ variable takes an integer that defines the amount of time
 to wait between each check, specified in seconds.

3 Use 0 as a value for __waittime__ to make the script wait at a random 
interval between 12 and 24 hours until the next check.

4 Run ARIS2Results.py to start the checks.

When the script finds your results they will be automatically
 downloaded into full_results.html.

Requirements
1 Python 3.x
2 Chromedriver
3 Chrome Browser
"""

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
from selenium.webdriver.chrome.options import Options 

try:
	import credentials # local modules
except:
    print("\n>> You did not create a credentials.py file, Read the instructions on the Github page again\n\n")
    raise

def compare_last_table(htmlString):
    if not os.path.isfile("result_table.html"):
        with open("result_table.html", "w", encoding="utf8") as f:
            f.write(htmlString)

        print("First time seeing the results page, the table has been saved...")
        return True

    try:
        with open("result_table.html", "r", encoding="utf8") as f:
            old_html = f.read()
        
        if len(old_html)==len(htmlString):
            return True
    except Exception as e:
        print(f"{e}")
    
    return False    
    

def navigate_aris_user(USERNAME, PASSWORD, headless=True):
    start_time= time.time()
    aris_url = r"https://aris2.udsm.ac.tz/index.php"
    chrome_options = Options()

    if headless == True:
        chrome_options.add_argument("--headless")

    driver = webdriver.Chrome(chrome_options=chrome_options)
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

        driver.find_element_by_css_selector("table td ul li:last-child a").click()
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
    username=credentials.__username__
    password=credentials.__password__
    wait_time=credentials.__waittime__
    headless=credentials.__headless__

    print(f">> ID Number: {username}\n>> password: {'*' * len(password)}")
    
    while navigate_aris_user(username, password, headless):
        if wait_time==0:
            sleep_time = randint(43200, 86400)
            print(f"Sleeping for {int(sleep_time)}s")
            time.sleep(sleep_time)
        else:
            print(f"Sleeping for {int(wait_time)}s")
            time.sleep(wait_time)

        


    
        
