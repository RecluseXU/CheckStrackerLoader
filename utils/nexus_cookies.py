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

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from utils.util import Util
import json
# from util import Util

cookies_json_location = Util.get_resources_folder()+'Nexus_Cookies.txt'

def get_cookies_by_selenium_login(user_name, user_password):
    '''
    @summary: 通过selenium获取cookies信息，并记录下来，返回
    @return: cookies:dict
    '''
    driver = webdriver.Firefox()
    # 登录界面
    driver.get('https://users.nexusmods.com/auth/sign_in')
    Util.info_print('请在页面中登录N网账户', 3)
    Util.info_print('如果设置在conf.ini的账户密码正确，这个过程会自动完成。', 3)
    Util.info_print('如果不正确，请手动输入账户密码', 3)

    # 登录界面
    try:
        username_inputer = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "user_login")))
    finally:
        username_inputer.send_keys(user_name)
    try:
        userpassword_inputer = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "user_password")))
    finally:
        userpassword_inputer.send_keys(user_password)

    commit_button = driver.find_element_by_xpath('//input[@type="submit"]')
    commit_button.click()

    while driver.current_url == "https://users.nexusmods.com/auth/sign_i":
        time.sleep(1)

    # 欢迎界面
    try:
        index_a = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//div[@class="left-link"]/a[@class="d-none d-md-block"]')))
        index_a.click()
    finally:
        Util.info_print('等待进入首页，请勿操作', 3)

    # 返回首页后
    while driver.current_url != "https://www.nexusmods.com/":
        time.sleep(1)
    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/header[1]/div[1]/div[2]/div/div/div[3]/div[2]')))
    finally:
        nexus_cookies_list = driver.get_cookies()

    nexus_cookies = dict()
    for cookie in nexus_cookies_list:
        nexus_cookies[cookie['name']] = cookie['value']

    with open(cookies_json_location, 'w', encoding="utf-8")as f:
        json.dump(nexus_cookies, f)
    driver.close()
    return nexus_cookies


def get_cookies_from_file():
    '''
    @summary: 从文件中读取cookies信息
    @return: cookies:dict
    '''
    with open(cookies_json_location, "r", encoding="utf-8")as f:
        nexus_cookies = json.load(f)
    return nexus_cookies


if __name__ == "__main__":
    # host = ".baidu.com"
    # a = get_cookie_from_chrome(host)
    # b = get_cookies_by_selenium_login("", "")
    b = get_cookies_by_selenium_login("444640050@qq.com", "")

    print(b)