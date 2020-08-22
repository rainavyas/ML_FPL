import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By

import time

def get_url(player_name):
    driver = webdriver.Chrome(executable_path=r'/Users/adian/Documents/PROJECTS/BOT/chromedriver')
    driver.get("https://fbref.com/en")
    time.sleep(1)

    #team_names = driver.find_elements_by_xpath("//a[@name='Liverpool']")

    search_bar = driver.find_element_by_name("search")
    search_bar.send_keys(player_name)
    time.sleep(1)
    driver.find_element_by_class_name("ac-suggestion").click()
    time.sleep(1)
    url = driver.current_url
    return(get_summary(url))

def get_summary(url):
    split_url = url.split("/")
    player = split_url.pop()
    split_url.extend(["matchlogs","2019-2020","summary", player + "-Match-Logs"])
    return("/".join(split_url))


def get_link_list(name_list):
    output_list = []
    for i in name_list:
        output_list.append(get_url(i))

liverpool = ["Virgil Van Dijk", "Sadio Mane", "Andrew Robertson", "Xedan Shaqiri"]
test = ["Bob"]
get_link_list(test)


#url = get_url("Virgil Van Dijk")
#url = get_summary(url)
