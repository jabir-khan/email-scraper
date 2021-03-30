from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import requests
import time
from bs4 import BeautifulSoup
import urllib
import os
import time
from time import sleep
from random import choice
from uuid import uuid4
import html2text
import pandas as pd
import re


bbb_org_name = []
bbb_website = []
bbb_website_links = []
org_links = []
bbb_emails = []


def scrapper(url):
    '''----------------------------options settings--------------------'''
    chrome_options = Options()
    proxy = "18.222.238.170:8888"  # tinyproxy
    print('Using Proxy Mode:{}'.format(proxy))
    chrome_options.add_argument('--proxy-server=%s' % proxy)
    '''if you dont want headless uncomment this'''
    # chrome_options.add_argument("--headless")
    # chrome_options.add_argument("--window-size=1400x800"    
    chrome_driver = 'C:\\chromedriver.exe'
    driver = webdriver.Chrome(options=chrome_options,
                              executable_path=chrome_driver)
    '''----------------------------end option settings--------------------'''

    driver.get(url)
    time.sleep(2)    

    # search_box = driver.find_element_by_id("findTypeaheadInput")
    # search_box.send_keys(Keys.CONTROL, 'a')
    # search_box.send_keys(Keys.CONTROL, 'x')   

    # ''' pass search keyword to search field '''
    # search_box.send_keys(search_keyword)

    # location = driver.find_element_by_id("nearTypeaheadInput")
    # location.send_keys(Keys.CONTROL, 'a')
    # location.send_keys(Keys.CONTROL, 'x')
    # ''' pass location to search field '''
    # location.send_keys("San Francisco, CA")
    
        
    # search_box.send_keys(Keys.ENTER)
    # time.sleep(1)

    ''' get all organization details '''
    html = driver.page_source   
    soup = BeautifulSoup(html, 'html.parser')
    org_names = soup.find_all('a', {'class': 'Name__Link-sc-12ndgzr-1 fsnukw'},href=True)
    
    # print(org_names)

          

    phones = soup.find_all('p', {'class': 'Phone-sc-1p1gq9f-0'})
    address = soup.find_all('p', {'class':'Address-sc-9uj8rv-0'})
  
    for x in range(len(org_names)):        
        bbb_org_name.append(org_names[x].text)
        # print('org name is:', bbb_org_name)
        # bbb_phone.append(phones[phone].a.text)
        ''' extract all the business links from org_names '''
        link = org_names[x]['href']
        print(org_names[x]['href'])

        ''' open links one by one and grab the website url '''
        driver.get(link)
        time.sleep(3)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        web_url = soup.find('a', {'class': 'styles__LinkStyled-sc-13wt55m-0 futKTq dtm-url'})
        
        if web_url is not None:
            print(web_url.text) 
            bbb_website.append(web_url.text)
            
        def Check_duplicate(x):
            new_url_list = []
            for i in x: 
                if i not in new_url_list: 
                    new_url_list.append(i)
            return new_url_list or "Searching url"    
        # This code is contributed by Sandeep_anand in GeeksforGeeks
        print (Check_duplicate(bbb_website))
        bbb_website_links = Check_duplicate(bbb_website)       

           

    print("All links are collected now opening the links...")

    def Check_duplicate_emails(x):
        new_emails_list = []
        for i in x: 
            if i not in new_emails_list: 
                new_emails_list.append(i)
        return new_emails_list

    
    for links in range(len(bbb_website_links)):

        ''' make a contact page url '''
        try:
            driver.get(bbb_website_links[links])        
            time.sleep(3)
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
        except:
            pass            
        
        try:
            contact = driver.find_element_by_xpath("//a[contains(text(),'contact')]")    
            driver.execute_script("arguments[0].click();", contact)      
            html = driver.page_source
            EMAIL_REGEX = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z.]+'
            emails = re.findall(EMAIL_REGEX, html)            
            filtered_email = Check_duplicate_emails(emails)
            # using list comprehension            
            email_listToString = ', '.join(map(str, filtered_email))   
            bbb_emails.append(email_listToString)
            print('Emails: ', email_listToString)             
                  
        except NoSuchElementException:
            pass
            # print("small contact not found")

        try:
            Contact = driver.find_element_by_xpath("//a[contains(text(),'Contact')]")   
            driver.execute_script("arguments[0].click();", Contact)         
            html = driver.page_source
            EMAIL_REGEX = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z.]+'
            emails = re.findall(EMAIL_REGEX, html)
            filtered_email = Check_duplicate_emails(emails)
            # using list comprehension            
            email_listToString = ', '.join(map(str, filtered_email))   
            bbb_emails.append(email_listToString)
            print('Emails: ', email_listToString)             
          

        except NoSuchElementException:
            pass
            # print("Big contact not found")


        try:
            CONTACT = driver.find_element_by_xpath("//a[contains(text(),'CONTACT')]")   
            # CONTACT.click()
            driver.execute_script("arguments[0].click();", CONTACT)         
            html = driver.page_source
            EMAIL_REGEX = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
            emails = re.findall(EMAIL_REGEX, html)
            filtered_email = Check_duplicate_emails(emails)
            # using list comprehension            
            email_listToString = ', '.join(map(str, filtered_email)) 
            bbb_emails.append(email_listToString)
            print('Emails: ', email_listToString)             
          

        except NoSuchElementException:
            pass
            # print("CAPS contact not found")   
            # print(match.groups()[0])
                        
            
                
            

search_keyword = str(input("What Business do you want to search ? =>"))
print("[+] Location is set to San Francisco, CA")
# page_no = int(input("How many page do you want to scrape ? =>"))


for i in range(0,1):
    page_no = i+1
    url = "https://www.bbb.org/search?find_country=USA&find_loc=San%20Francisco%2C%20CA&find_text="+search_keyword+"&page="+str(page_no)   
    scrapper(url)

    print("[+] Creating CSV file...")
    # print(bbb_website_links)
    # print("Total links:", len(bbb_org_name))
    # print("Total website:",len(bbb_website))



    data = {'Email': bbb_emails}
    df = pd.DataFrame(data=data, columns = ['Email'])
    df.to_csv('bbb_'+search_keyword+'_'+str(page_no)+'.csv') 


# data = {'Company Name': bbb_website_links, 'URL': bbb_website}
# df = pd.DataFrame(data=data, columns = ['Company Name', 'URL'])
# df.to_csv('bbb_'+search_keyword+'.csv') 

# site:linkedin.com "AI engineer" "Nepal" "@gmail.com"
# https://www.bbb.org/search?find_country=USA&find_loc=San%20Francisco%2C%20CA&find_text=school&page=1
