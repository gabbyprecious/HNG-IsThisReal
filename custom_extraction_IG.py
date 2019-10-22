# -*- coding: utf-8 -*-
"""
Created on Sun May 19 11:44:36 2019

@author: Katie
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pandas
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains


class AccountScraper():
    def __init__(self,email,password,pagename):
        self.browserProfile = webdriver.ChromeOptions()
        self.browserProfile.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
        self.browserProfile.add_argument("--disable-notifications")
        self.browserProfile.add_argument("--headless")
        self.browserProfile.add_argument("window-size=1200,1100")
        self.email = email
        self.password = password
        self.pagename = pagename
        self.driver = webdriver.Chrome(executable_path ='C:/Users/USER/Downloads/Compressed/chromedriver_win32/chromedriver.exe',chrome_options=self.browserProfile)
        
    def login(self):
        self.driver.get("https://www.instagram.com/accounts/login/")
        emailInput = self.driver.find_elements_by_css_selector('form input')[0]
        passwordInput = self.driver.find_elements_by_css_selector('form input')[1]

        emailInput.send_keys(self.email)
        passwordInput.send_keys(self.password)
        passwordInput.send_keys(Keys.ENTER)
        time.sleep(2)
        print("Login Successful")
        
    
    def getUserLikes(self,Login):
        self.driver.get('https://www.instagram.com/'+ self.pagename)
        self.user_posts = []
        for posts in self.driver.find_elements_by_xpath("//div[@class= 'v1Nh3 kIKUG  _bz0w']"):
            self.post_links = posts.find_element_by_css_selector('a').get_attribute('href')
            self.user_posts.append(self.post_links)
        
        time.sleep(2)
        # here, you can see user list you want.
        # you have to scroll down to download more data from instagram server.
        # loop until last element with users table view height value.
        
        self.user_list = []
        self.extract_comment =[]
        for post in self.user_posts:
            self.driver.get(post)
            self.get_comments = []
            try:
                self.comments = self.driver.find_element_by_css_selector('div.EtaWk')
                self.nested_comments = self.comments.find_elements_by_css_selector('div.C4VMK')
                for comment in self.nested_comments:
                    self.comment_links = comment.find_element_by_css_selector('a').get_attribute("href")
                    self.get_comments.append(self.comment_links)
                self.extract_comment += self.get_comments
                
                
            except NoSuchElementException:
                pass
            
            actions = ActionChains(self.driver)
            self.userid_element = self.driver.find_elements_by_xpath('//*[@id="react-root"]/section/main/div/div/article/div[2]/section[2]/div/div[@class="Nm9Fw"]/a[@class="zV_Nj"]')[0]
            actions.move_to_element(self.userid_element).click().perform()
            time.sleep(2)
            self.height = self.driver.find_element_by_xpath("//html/body/div[3]/div/div[2]/div/div").value_of_css_property("padding-top")
            self.users = []
            match = False
            while match==False:
                self.lastHeight = self.height
                # step 1
                self.elements = self.driver.find_elements_by_xpath("//*[@id]/div/a")
                # step 2
                for element in self.elements:
                    if element.get_attribute('title') not in self.users:
                        self.users.append(element.get_attribute('title'))
                        #print(self.users)
            
                        
                # step 3
                self.driver.execute_script("return arguments[0].scrollIntoView();", self.elements[-1])
                time.sleep(1)
                # step 4
                self.height = self.driver.find_element_by_xpath("//html/body/div[3]/div/div[2]/div/div").value_of_css_property("padding-top")
                if self.lastHeight==self.height:
                    match = True
            self.user_list += self.users
            
        self.user_likes = list(set(self.user_list + self.extract_comment))
        print("Likes and Comments Extracted.Check the custom_extraction_IG.csv file")
        self.driver.close()
        return self.user_likes
    
    
    def save_likes(self,user_list):
        self.likes = user_list
        print(self.likes)
        self.df = pandas.DataFrame({"Users that Liked/Commented":self.likes})
        self.df.to_csv("custom_extraction_IG.csv")
    
    
    
username = input("le__x__ie")
password = input("Leke039.") 
pagename = input("Enter the IG page name\n")     
instagram = AccountScraper(username,password,pagename)
Login = instagram.login()
Likes = instagram.getUserLikes(Login)
instagram.save_likes(Likes)
