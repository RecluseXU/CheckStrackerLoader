#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   spider_Nexus_file
@Time    :   2020/02/23 18:14:01
@Author  :   Recluse Xu
@Version :   1.0
@Contact :   444640050@qq.com
@License :   (C)Copyright 2017-2022, Recluse
@Desc    :   None
'''

# here put the import lib
import winreg
import os
import hashlib
import requests
from fake_useragent import UserAgent
import time
import json
import datetime
from lxml import etree
import sqlite3
from win32.win32crypt import CryptUnprotectData

CONF = {}

def read_conf_from_file():
    pass


def getcookiefromchrome(host='.nexusmods.com'):
    '''
    @summary: 从系统安装的谷歌浏览器中得到N网的cookie
    '''
    print(os.environ['LOCALAPPDATA'])
    cookiepath = os.environ['LOCALAPPDATA']+r"\Google\Chrome\User Data\Default\Cookies"
    sql = "select host_key,name,encrypted_value from cookies where host_key='%s'" % host
    with sqlite3.connect(cookiepath) as conn:
        cu = conn.cursor()
        cookies = {
            name: CryptUnprotectData(encrypted_value)[1].decode() for host_key, name, encrypted_value in cu.execute(sql).fetchall()}
        # print(cookies)
    return cookies


def get_MHW_Install_Address():
    '''
    @return: 怪猎目录
    '''
    print("Try to get MHW information from the registry")
    try:
        aReg = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
        aKey = winreg.OpenKey(aReg, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\Steam App 582010")
        data = winreg.QueryValueEx(aKey, "InstallLocation")[0]
        print("->", data)
        return data
    except Exception as e:
        print("->Fail", e)


def is_file_exists(path: str, filename_list: list):
    '''
    @summary: 
    @return: 检测路径下的文件是否都已经存在:bool
    '''
    print(r'Try check the file statue of '+str(filename_list))
    if len(path) > 0 and path[-1] != '/':
        path = path+"/"
    for filename in filename_list:
        if not os.path.exists(path + filename):
            print("->statue: Not installed")
            return False
    print("->statue: installed")
    return True


def get_mod_file_page():
    '''
    @summary: 爬虫得到 MOD 的文件页
    @return: session
    '''
    print(r'Try to get the lastest "Stracker\'s Loader" file page')
    ua = UserAgent()
    session = requests.session()
    headers = {
        'User-Agent': ua.random,
        "Accept": "text/css,*/*;q=0.1",
        "Host": "www.nexusmods.com"
    }
    try:
        response = session.get(
            url="https://www.nexusmods.com/monsterhunterworld/mods/1982?tab=files",
            headers=headers, verify=False)
        file_page_html = response.content.decode()
        # print(file_page_html)
        with open("mod_file_page_.html", 'w', encoding='utf-8')as f:
            f.write(file_page_html)
        print("->success")
        return session, file_page_html
    except Exception as e:
        print("->fail", e)
        return


def analyze_mod_file_page(html: str):
    '''
    @summary: 解析得到 MOD 的文件页,得到一些数据保存到配置中，并返回下载页数据
    '''
    with open('mod_file_page.html', 'r')as f:
        html = f.read()
    xpath_data = etree.HTML(html)
    last_publish_date = xpath_data.xpath('//*[@id="file-expander-header-9908"]//div[@class="stat"]/text()')[0].strip()
    # date, day = last_publish_date
    CONF['LATEST_PUBLISH_DATE'] = datetime.datetime.strptime(last_publish_date, r"%d %b %Y, %I:%M%p")

    a = xpath_data.xpath('//*[@id="file-expander-header-9908"]')[0]
    a = a.xpath('..//a[@class="btn inline-flex"]/@href')[1]
    print(a)





if __name__ == "__main__":
    # a = read_conf_from_file()
    print('3DM Biss')
    # MHW_Install_Address = get_MHW_Install_Address()
    # Mod_Install_statue = is_file_exists(MHW_Install_Address, ["dinput8.dll", "dinput-config.json"])
    # a = int(time.time())
    # get_mod_file_page()
    # a = analyze_mod_file_page("")
    a = getcookiefromchrome()
    print(a)