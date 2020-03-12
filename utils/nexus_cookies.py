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


from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium import webdriver
import json
# import time
import os
from utils.util import Util
# from util import Util


cookies_json_location = None
lib_location = None


def set_cookies_json_location(location: str):
    global cookies_json_location
    cookies_json_location = location


def set_lib_location_location(location: str):
    global lib_location
    lib_location = location


def _init_selenium_chrome_driver():
    '''
    @summary: 配置selenium.webdriver   chrome
    @return: selenium.webdriver chrome
    '''
    chromedriver = lib_location + "chromedriver.exe"
    drivePath = os.path.join(os.path.dirname(__file__), chromedriver)
    options = webdriver.ChromeOptions()
    # 禁止图片加载
    # prefs = {"profile.managed_default_content_settings.images": 2}
    # options.add_experimental_option("prefs", prefs)
    # 不显示图片
    # options.add_argument('--blink-settings=imagesEnabled=false')
    # 非沙盒模式
    options.add_argument('no-sandbox')
    driver = webdriver.Chrome(executable_path=drivePath, chrome_options=options)
    return driver


def _init_selenium_firefox_driver():
    '''
    @summary: 配置selenium.webdriver   firefoxdriver
    @return: selenium.webdriver firefoxdriver
    '''
    firefoxdriver = lib_location + "geckodriver.exe"
    drivePath = os.path.join(os.path.dirname(__file__), firefoxdriver)
    driver = webdriver.Firefox(executable_path=drivePath)
    return driver


def _init_selenium_ie_driver():
    '''
    @summary: 配置selenium.webdriver   IE
    @return: selenium.webdriver IE
    '''
    iedriver = lib_location + "IEDriverServer_x32.exe"
    drivePath = os.path.join(os.path.dirname(__file__), iedriver)

    capabilities = DesiredCapabilities.INTERNETEXPLORER
    capabilities["ignoreProtectedModeSettings"] = True  # 无视保护模式
    capabilities["ignoreZoomSetting"] = True  # 不检查界面缩放
    driver = webdriver.Ie(executable_path=drivePath, capabilities=capabilities)
    return driver


def _init_selenium_driver():
    '''
    @summary: 尝试初始化各个不同的webdriver
    @return: webdriver
    '''
    Util.info_print('尝试初始化浏览器', 3)

    try:
        Util.info_print('尝试初始化chrome浏览器', 4)
        return _init_selenium_chrome_driver()
    except Exception as e:
        print("失败", e)

    try:
        Util.info_print('尝试初始化火狐浏览器', 4)
        return _init_selenium_firefox_driver()
    except Exception as e:
        print("失败", e)

    try:
        Util.info_print('尝试初始化IE浏览器', 4)
        return _init_selenium_ie_driver()
    except Exception as e:
        print("失败", e)


def _selenium_operations(driver: webdriver, user_name: str, user_password: str):
    # 登录界面
    Util.info_print('登录界面', 3)
    driver.get('https://users.nexusmods.com/auth/sign_in')
    Util.info_print('请在页面中登录N网账户', 3)
    Util.info_print('如果设置在conf.ini的账户密码正确，这个过程会自动完成。', 3)
    Util.info_print('如果不正确，请手动输入账户密码', 3)
    Util.info_print('每一步操作都设置了一定的的可行时间，超过时间程序就会退出', 3)

    wait = WebDriverWait(driver, 300)
    username_inputer = wait.until(presence_of_element_located((By.ID, "user_login")))
    userpassword_inputer = wait.until(presence_of_element_located((By.ID, "password")))
    commit_button = wait.until(presence_of_element_located((By.XPATH, '//input[@type="submit"]')))

    username_inputer.send_keys(user_name)
    userpassword_inputer.send_keys(user_password)
    commit_button.click()

    wait.until(EC.url_changes)
    # 欢迎界面

    index_a = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="links"]/div[@class="left-link"]/a[1]')))
    index_a.click()
    Util.info_print('等待进入首页，请勿操作', 3)

    # 返回首页后
    # Util.info_print('等待从首页中获取cookies', 3)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".intro > h1:nth-child(1)")))
    nexus_cookies_list = driver.get_cookies()
    driver.quit()

    nexus_cookies = dict()
    for cookie in nexus_cookies_list:
        nexus_cookies[cookie['name']] = cookie['value']

    return nexus_cookies


def save_cookies_to_file(nexus_cookies: dict):
    '''
    @summary: 将cookies信息保存到resources/Nexus_Cookies.txt
    '''
    with open(cookies_json_location, 'w', encoding="utf-8")as f:
        json.dump(nexus_cookies, f)


def get_cookies_by_selenium_login(user_name: str, user_password: str):
    '''
    @summary: 通过selenium获取cookies信息，并记录下来，返回
    @return: cookies:dict
    '''
    driver = _init_selenium_driver()
    if not driver:
        Util.info_print('尝试初始化浏览器失败', 3)
        return
    nexus_cookies = _selenium_operations(driver, user_name, user_password)
    save_cookies_to_file(nexus_cookies)
    return nexus_cookies


def get_cookies_from_file():
    '''
    @summary: 从文件中读取cookies信息
    @return: cookies:dict
    '''
    with open(cookies_json_location, "r", encoding="utf-8")as f:
        nexus_cookies = json.load(f)
    return nexus_cookies


def get_cookies_by_input():
    '''
    @summary: 让用户手工输入cookies信息
    @return: cookies:dict
    '''
    a = input("尝试手动获取Cookies信息？(输入y代表尝试，输入其他东西代表不尝试并退出)\n")
    if a == "y":
        cookes_dict = dict()
        try:
            cookies_str = input("请输入手动获取的cookies:")
            for cookie in cookies_str.split(';'):
                cookie_one_list = cookie.split('=')
                cookes_dict[cookie_one_list[0]] = cookie_one_list[1]
            save_cookies_to_file(cookes_dict)
            return cookes_dict
        except Exception as e:
            print("失败", e)
    Util.warning_and_exit(1)


if __name__ == "__main__":
    # host = ".baidu.com"
    # init_selenium_driver()
    # a = get_cookie_from_chrome(host)
    # b = get_cookies_by_selenium_login("", "")
    b = get_cookies_by_selenium_login("444640050@qq.com", "XuGuoHao444640050")
    # _init_selenium_driver()
    # print(b)
    pass
