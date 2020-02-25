#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   Nexus_cookies.py
@Time    :   2020/02/24 15:52:31
@Author  :   Recluse Xu
@Version :   1.0
@Contact :   444640050@qq.com
@License :   (C)Copyright 2017-2022, Recluse
@Desc    :   None
'''

# here put the import lib

import json
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver


def get_cookies_by_selenium_login(user_name, user_password):
    driver = webdriver.Firefox()
    # 登录界面
    driver.get('https://users.nexusmods.com/auth/sign_in')
    try:
        username_inputer = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "user_login")))
        userpassword_inputer = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "user_password")))
    finally:
        username_inputer.send_keys(user_name)
        userpassword_inputer.send_keys(user_password)
        commit_button = driver.find_element_by_xpath('//input[@type="submit"]')
        commit_button.click()
    
    while driver.current_url == "https://users.nexusmods.com/auth/sign_in":
        time.sleep(0.5)

    nexus_cookies_list = driver.get_cookies()
    while len(nexus_cookies_list) < 9:
        nexus_cookies_list = driver.get_cookies()
        time.sleep(2)

    print(nexus_cookies_list)
    nexus_cookies = ''
    for cookie in nexus_cookies_list:
        nexus_cookies = nexus_cookies + cookie['name'] + "=" + cookie['value']+"; "
    nexus_cookies = nexus_cookies[:-2]
    print(nexus_cookies)

    # driver.close()

    with open('Nexus_Cookies.json', 'w', encoding="utf-8")as f:
        json.dump(nexus_cookies, f)
    driver.close()
    return nexus_cookies


def get_cookies_from_file():
    with open("Nexus_Cookies.json", "r", encoding="utf-8")as f:
        nexus_cookies = json.load(f)
    return nexus_cookies


if __name__ == "__main__":
    # host = ".baidu.com"
    # a = get_cookie_from_chrome(host)
    # b = get_cookies_by_selenium_login("", "")
    b = get_cookies_by_selenium_login("444640050@qq.com", "")

    print(b)