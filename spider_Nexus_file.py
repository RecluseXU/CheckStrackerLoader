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
import requests
from fake_useragent import UserAgent
import datetime
import time
from lxml import etree
import re
from utils.util import Util
from utils.ini import Conf_ini
from utils.nexus_cookies import get_cookies_by_selenium_login, get_cookies_from_file
import json


my_session = requests.session()
ua = UserAgent()
headers = {
    "Connection": "keep-alive",
    "DNT": "1",
    "Host": "www.nexusmods.com",
    "Referer": "https://www.nexusmods.com",
    "TE": "Trailers",
    "Upgrade-Insecure-Requests": "1",
    'User-Agent': ua.firefox,
    }


def is_login(my_cookies):
    '''
    @summary: 通过检验cookies,得知是否已经成功登录N网
    '''
    global headers
    headers['cookie'] = my_cookies
    response = my_session.get(
        url="https://www.nexusmods.com/monsterhunterworld",
        headers=headers)
    file_page_html = response.content.decode()
    with open('is_login.html', 'w', encoding='utf-8')as f:
        f.write(file_page_html)
    xpath_data = etree.HTML(file_page_html)
    a = xpath_data.xpath('//*[@id="login"]')
    if len(a) == 0:
        return True
    return False


def get_cookies_info(run_location, user_name, user_pwd):
    '''
    @summary: 获取cookies信息
    @return: cookies:dict
    '''
    if Util.is_file_exists(run_location + "\\Nexus_Cookies.json"):
        Util.info_print('Nexus_Cookies.json存在', 2)
        Util.info_print('尝试通过Nexus_Cookies.json获取Cookies信息', 3)
        my_cookies = get_cookies_from_file()
        if is_login(my_cookies):
            Util.info_print('Cookies信息验证成功，', 4)
            return
        else:
            Util.info_print('Cookies信息验证失败，', 4)
    Util.info_print('尝试通过登录N网记录Cookies信息', 2)
    my_cookies = get_cookies_by_selenium_login(user_name, user_pwd)
    return my_cookies


def spider_mod_file_page():
    '''
    @summary: 爬虫得到 MOD 的文件页
    @return: session
    '''
    try:
        response = my_session.get(
            url="https://www.nexusmods.com/monsterhunterworld/mods/1982?tab=files",
            headers=headers)
        file_page_html = response.content.decode()
        # print(file_page_html)
        with open("mod_file_page.html", 'w', encoding='utf-8')as f:
            f.write(file_page_html)
        headers['Referer'] = "https://www.nexusmods.com/monsterhunterworld/mods/1982?tab=files"
        return file_page_html
    except Exception as e:
        print("失败", e)
        Util.warning_and_exit(1)


def get_mod_file_page(is_safe_to_spide: bool):
    '''
    @summary: 获取 Stracker\'s Loader 的文件页
    @return: 网页:str, 使用了爬虫:bool
    '''
    if is_safe_to_spide:
        Util.info_print('通过爬虫得到 "Stracker\'s Loader" 文件页', 2)
        page_html = spider_mod_file_page()
        is_spider = True
    else:
        Util.info_print('由于爬虫等待时间未过，从本地记录中获取', 2)
        with open('mod_file_page.html', 'r')as f:
            page_html = f.read()
            is_spider = False
    Util.info_print('获取成功', 3)
    return page_html, is_spider


def analyze_mod_file_page(html: str):
    '''
    @summary: 解析得到 MOD 的文件页,得到一些数据保存到配置中，并返回下载页数据
    @return: 最新版发布的时间, 最新版下载的URL
    '''
    try:
        xpath_data = etree.HTML(html)
        a = xpath_data.xpath('//*[@id="file-expander-header-9908"]//div[@class="stat"]/text()')
        a = a[0].strip()
        last_publish_date = datetime.datetime.strptime(a, r"%d %b %Y, %I:%M%p")
        
        a = xpath_data.xpath('//*[@id="file-expander-header-9908"]')[0]
        last_download_url = a.xpath('..//a[@class="btn inline-flex"]/@href')[1]

        return last_publish_date, last_download_url
    except Exception as e:
        print("失败", e)
        Util.warning_and_exit(1)


def spider_download_file_page(download_page_url):
    '''
    @summary: 爬虫得到 MOD 的文件页
    @return: 下载页html:str
    '''
    try:
        response = my_session.get(url=download_page_url, headers=headers)
        download_page_html = response.content.decode()
        # print(file_page_html)
        with open("mod_download_page.html", 'w', encoding='utf-8')as f:
            f.write(download_page_html)
        headers['Referer'] = download_page_url
        return download_page_html
    except Exception as e:
        print("失败", e)
        Util.warning_and_exit(1)


def analyze_download_file_page(html: str):
    '''
    @summary: 解析 MOD 的下载页
    @return: file_id, game_id
    '''
    try:
        xpath_data = etree.HTML(html)
        file_id = re.search(r"const file_id = \d+", html).group()[16:]
        game_id = re.search(r"const game_id = \d+", html).group()[16:]
        return file_id, game_id

    except Exception as e:
        print("失败", e)
        Util.warning_and_exit(1)


def spider_download_file(file_id, game_id):
    '''
    @summary: 根据留在页面上的ajax信息,向N网服务器提交请求得到下载链接
    @return: 下载用的url:str
    '''
    data = {
            "fid": file_id,
            "game_id": game_id,
        }
    headers['Cookie'] = get_cookies_from_file()
    
    try:
        url = "https://www.nexusmods.com/Core/Libs/Common/Managers/Downloads?GenerateDownloadUrl"
        response = my_session.post(url=url, headers=headers, data=data)
        download_url_dict = response.content.decode()
        download_url = json.loads(download_url_dict)['url']
        print(download_url)
        with open('download_file_url.json', 'w', encoding='utf-8')as f:
            f.write(download_url)

        return download_url
    except Exception as e:
        print("失败", e)


def downloadFile(url):
    '''
    @summary: 下载文件
    '''
    r = requests.get(url, stream=True, headers=headers)
    length = float(r.headers['content-length'])
    with open('Str', 'wb')as f:
        count = 0
        count_tmp = 0
        time1 = time.time()
        for chunk in r.iter_content(chunk_size=512):
            if chunk:
                f.write(chunk)
                count += len(chunk)
                if time.time() - time1 > 3:
                    p = count / length * 100
                    speed = (count - count_tmp) / 1024 / 1024 / 2
                    count_tmp = count
                    print(name + ': ' + formatFloat(p) + '%' + ' Speed: ' + formatFloat(speed) + 'M/S')
                    time1 = time.time()

def run():
    # 信息获取
    Util.info_print("获取本地信息")
    Util.info_print('尝试从注册表获取 MHW 目录', 1)
    MHW_Install_Address = Util.get_MHW_Install_Address()
    Util.info_print('尝试获取当前目录', 1)
    run_folder_location = Util.get_run_folder()
    Util.info_print('尝试获取 StrackerLoader-dinput8.dll 的 MD5', 1)
    dinput8_dll_md5 = Util.get_file_MD5(MHW_Install_Address, 'dinput8.dll')

    Util.info_print('尝试获取 conf.ini信息', 1)
    if not Util.is_file_exists(run_folder_location+'\\conf.ini'):
        Util.info_print('conf.ini不存在,创建conf.ini', 2)
        N_name = input('请输入N网账号或邮箱:')
        N_pwd = input('请输N网密码:')
        Conf_ini.creat_new_conf_ini(run_folder_location + '\\conf.ini', dinput8_dll_md5, N_name, N_pwd)
    Util.info_print('读取conf.ini', 2)
    conf_ini = Conf_ini(run_folder_location)

    Util.info_print('尝试获取 Cookies 信息', 1)
    username, userpwd = conf_ini.get_nexus_account_info()
    get_cookies_info(run_folder_location, username, userpwd)

    Util.info_print("获取MOD信息")
    Util.info_print('尝试获取N网 "Stracker\'s Loader" 文件信息页', 1)
    file_page_html, is_spider = get_mod_file_page(conf_ini.is_safe_to_spide())
    if is_spider:  # 更新最后一次爬虫的时间信息
        conf_ini.set_new_last_spide_time()

    Util.info_print(r'尝试分析文件页，得到 "Stracker\'s Loader" 最新版信息', 1)
    last_publish_date, last_download_url = analyze_mod_file_page(file_page_html)
    Util.info_print("最新版本上传日期\t" + str(last_publish_date), 2)
    Util.info_print("最新版本下载地址\t" + last_download_url, 2)

    Util.info_print('尝试获取N网 "Stracker\'s Loader" 最新版文件下载页', 1)
    download_page_html = spider_download_file_page(last_download_url)
    Util.info_print('尝试分析N网 "Stracker\'s Loader" 最新版文件下载页', 1)
    file_id, game_id = analyze_download_file_page(download_page_html)
    Util.info_print('game_id\t'+game_id, 2)
    Util.info_print('file id\t'+file_id, 2)

    Util.info_print('尝试获取N网 "Stracker\'s Loader" 最新版文件下载url', 1)
    download_url = spider_download_file(file_id, game_id)
    Util.info_print("最新版文件下载url\t" + download_url, 2)

    Util.info_print('尝试获取N网 "Stracker\'s Loader" 最新版文件下载url', 1)
    # downloadFile()

if __name__ == "__main__":
    # run()
    
    # is_login(get_cookies_from_file())
    # print()

    spider_download_file(9908, 2531)


    
    # a = getcookiefromchrome()
    # a = Util.get_run_folder()
    # print(a)
    print('3DM Biss')