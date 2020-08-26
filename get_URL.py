import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By

import time

def get_url(player_name, season):
    driver = webdriver.Chrome()
    driver.get("https://fbref.com/en")
    time.sleep(1)

    #team_names = driver.find_elements_by_xpath("//a[@name='Liverpool']")

    search_bar = driver.find_element_by_name("search")
    search_bar.send_keys(player_name)
    time.sleep(1)
    driver.find_element_by_class_name("ac-suggestion").click()
    time.sleep(1)
    url = driver.current_url
    return(get_summary(url, season))

def get_summary(url, season):
    split_url = url.split("/")
    player = split_url.pop()
    split_url.extend(["matchlogs", season, "summary", player + "-Match-Logs"])
    return("/".join(split_url))

def get_ID(player_name):
    driver = webdriver.Chrome()
    driver.get("https://fbref.com/en")
    time.sleep(1)

    #team_names = driver.find_elements_by_xpath("//a[@name='Liverpool']")

    search_bar = driver.find_element_by_name("search")
    search_bar.send_keys(player_name)
    time.sleep(1)
    driver.find_element_by_class_name("ac-suggestion").click()
    time.sleep(1)
    url = driver.current_url
    url_parts = url.split('/')
    id = url_parts[5]
    return id
