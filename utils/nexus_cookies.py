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
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import json
import os
from utils.util import Util
# from util import Util


cookies_json_location = Util.get_resources_folder()+'Nexus_Cookies.txt'


def init_selenium_chrome_driver():
    '''
    @summary: 配置selenium.webdriver   chrome
    '''
    chromedriver = Util.get_lib_folder() + "chromedriver.exe"
    drivePath = os.path.join(os.path.dirname(__file__), chromedriver)
    options = webdriver.ChromeOptions()
    # 禁止图片加载
    prefs = {"profile.managed_default_content_settings.images": 2}
    options.add_experimental_option("prefs", prefs)
    # 不显示图片
    options.add_argument('--blink-settings=imagesEnabled=false')
    # 非沙盒模式
    options.add_argument('no-sandbox')
    driver = webdriver.Chrome(executable_path=drivePath, chrome_options=options)
    return driver


def init_selenium_ie_driver():
    '''
    @summary: 配置selenium.webdriver   IE
    '''
    iedriver = Util.get_lib_folder() + "IEDriverServer_x32.exe"
    drivePath = os.path.join(os.path.dirname(__file__), iedriver)

    capabilities = DesiredCapabilities.INTERNETEXPLORER
    capabilities["ignoreProtectedModeSettings"] = True  # 无视保护模式
    capabilities["ignoreZoomSetting"] = True  # 不检查界面缩放
    driver = webdriver.Ie(executable_path=drivePath, capabilities=capabilities)
    return driver


def init_selenium_driver():
    try:
        Util.info_print('尝试初始化chrome浏览器', 3)
        return init_selenium_chrome_driver()
    except Exception as e:
        print(e)
    
    try:
        Util.info_print('尝试初始化IE浏览器', 3)
        return init_selenium_ie_driver()
    except Exception as e:
        print(e)
    
    print("初始化浏览器失败")
    Util.warning_and_exit(1)


def get_cookies_by_selenium_login(user_name, user_password):
    '''
    @summary: 通过selenium获取cookies信息，并记录下来，返回
    @return: cookies:dict
    '''
    driver = init_selenium_driver()

    # 登录界面
    driver.get('https://users.nexusmods.com/auth/sign_in')
    Util.info_print('请在页面中登录N网账户', 3)
    Util.info_print('如果设置在conf.ini的账户密码正确，这个过程会自动完成。', 3)
    Util.info_print('如果不正确，请手动输入账户密码', 3)
    Util.info_print('每一步操作都设置了30s的可行时间，超过时间程序就会退出', 3)

    # 登录界面
    username_inputer = driver.find_element_by_id("user_login")
    username_inputer.send_keys(user_name)
    userpassword_inputer = driver.find_element_by_id("password")
    userpassword_inputer.send_keys(user_password)

    commit_button = driver.find_element_by_xpath('//input[@type="submit"]')
    commit_button.click()

    while driver.current_url == "https://users.nexusmods.com/auth/sign_in":
        time.sleep(1)

    # 欢迎界面
    try:
        index_a = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//div[@class="links"]/div[@class="left-link"]/a[1]')))
        index_a.click()
    finally:
        Util.info_print('等待进入首页，请勿操作', 3)

    # 返回首页后
    while driver.current_url != "https://www.nexusmods.com/":
        time.sleep(1)
    Util.info_print('等待从首页中获取cookies', 3)
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
    # init_selenium_driver()
    # a = get_cookie_from_chrome(host)
    # b = get_cookies_by_selenium_login("", "")
    # b = get_cookies_by_selenium_login("444640050@qq.com", "Recluse444640050")
    # init_webbrowser_driver()
    # print(b)
    pass
