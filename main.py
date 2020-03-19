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
from utils.nexus_cookies import get_cookies_by_selenium_login, get_cookies_from_file, get_cookies_by_input, set_cookies_json_location, set_lib_location_location
from utils.nexus_cookies import set_info_print_func as set_coo_my_print_func
from utils.location_helper import Location
from utils.location_helper import set_info_print_func as set_loc_my_print_func
from utils.my_print import info_print
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
locate = None


def is_login(my_cookies):
    '''
    @summary: 通过检验cookies,得知是否已经成功登录N网
    '''
    global headers
    response = my_session.get(
        url="https://www.nexusmods.com/monsterhunterworld/mods/1982?tab=images",
        headers=headers,
        cookies=my_cookies
        )
    file_page_html = response.content.decode()

    location = locate.get_resources_folder()+ 'is_login.html'
    with open(location, 'w', encoding='utf-8')as f:
        f.write(file_page_html)
    xpath_data = etree.HTML(file_page_html)
    a = xpath_data.xpath('//*[@id="login"]')
    if len(a) == 0:
        return True
    return False


def get_cookies_info(user_name: str, user_pwd: str):
    '''
    @summary: 获取cookies信息
    @return: cookies:dict
    '''

    nexus_cookies_location = locate.get_cookies_txt_file()
    if Util.is_file_exists(nexus_cookies_location):
        info_print("110")
        info_print("111")
        my_cookies = get_cookies_from_file()
        # print(my_cookies)
        if is_login(my_cookies):
            info_print("112")
            return
        else:
            info_print("113")

    info_print("114")
    my_cookies = get_cookies_by_selenium_login(user_name, user_pwd)
    if my_cookies is not None:
        return my_cookies

    info_print("115")
    my_cookies = get_cookies_by_input()
    if is_login(my_cookies):
        info_print("116")
    else:
        info_print("117")
        Util.warning_and_exit(1)
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
        location = locate.get_resources_folder() + 'mod_file_page.html'
        with open(location, 'w', encoding='utf-8')as f:
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
        info_print('202')
        page_html = spider_mod_file_page()
        is_spider = True
    else:
        info_print('203')
        location = locate.get_resources_folder() + 'mod_file_page.html'
        with open(location, 'r')as f:
            page_html = f.read()
            is_spider = False
    info_print('204')
    return page_html, is_spider


def analyze_mod_file_page(html: str):
    '''
    @summary: 解析得到 MOD 的文件页,得到一些数据保存到配置中，并返回下载页数据
    @return: 最新版发布的时间, 最新版下载的URL
    '''
    try:
        xpath_data = etree.HTML(html)
        a = xpath_data.xpath('//*[@id="file-container-main-files"]//div[@class="stat"]/text()')
        a = a[0].strip()
        last_publish_date = datetime.datetime.strptime(a, r"%d %b %Y, %I:%M%p")

        a = xpath_data.xpath('//*[@id="file-container-main-files"]')[0]
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

        location = locate.get_resources_folder() + "mod_download_page.html"
        with open(location, 'w', encoding='utf-8')as f:
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
        file_id = re.search(r"const file_id = \d+", html).group()[16:]
        game_id = re.search(r"const game_id = \d+", html).group()[16:]
        return file_id, game_id

    except Exception as e:
        print("失败", e)
        Util.warning_and_exit(1)


def spider_download_file(file_id, game_id):
    '''
    @summary: 根据留在页面上的ajax信息,向N网服务器提交请求得到下载链接
    @return: 下载用的url:str , 文件类型:str
    '''
    data = {
            "fid": file_id,
            "game_id": game_id,
        }
    ajax_head = headers.copy()
    ajax_head['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
    ajax_head['Origin'] = 'https://www.nexusmods.com'
    try:
        url = "https://www.nexusmods.com/Core/Libs/Common/Managers/Downloads?GenerateDownloadUrl"
        response = my_session.post(url=url, headers=ajax_head, data=data, cookies=get_cookies_from_file())
        download_url_str = response.content.decode("utf-8")
        download_url = json.loads(download_url_str)['url']
        file_type = re.search(r'\.[a-z]+\?', download_url).group()[1:-1]

        location = locate.get_resources_folder() + "download_file_url.json"
        with open(location, 'w', encoding='utf-8')as f:
            f.write(file_type+"="+download_url)

        return download_url, file_type
    except Exception as e:
        print("失败", e)


def downloadFile(url, location, dl_host):
    '''
    @summary: 下载MOD文件
    '''
    def formatFloat(num):
        return '{:.2f}'.format(num)

    download_head = headers.copy()
    download_head['Host'] = dl_host

    with open(location, 'wb')as f:
        count = 0
        count_tmp = 0
        time_1 = time.time()
        try:
            response = my_session.get(url, stream=True, headers=download_head, cookies=get_cookies_from_file())
            content_length = float(response.headers['content-length'])
            for chunk in response.iter_content(chunk_size=1):
                if chunk:
                    f.write(chunk)
                    count += len(chunk)
                    if time.time() - time_1 > 2:
                        p = count / content_length * 100
                        speed = (count - count_tmp) / 1024 /2
                        count_tmp = count
                        print("\t\t" + formatFloat(p) + '%' + ' Speed: ' + formatFloat(speed) + 'KB/S')
                        time_1 = time.time()
        except Exception as e:
            print('失败', e)

    info_print('214')
    print("\t\t\t" + location)
    time.sleep(1)


def first_time_run():
    '''
    @summary: 第一次运行的工作
    '''
    info_print('100')
    info_print('101')
    location = locate.get_resources_folder()[:-1]
    Util.creat_a_folder(location)

    info_print('102')
    location = locate.get_lib_folder()[:-1]
    Util.creat_a_folder(location)

    info_print('103')
    info_print('104')
    info_print('105')
    N_name = input()
    info_print('106')
    N_pwd = input()
    Conf_ini.creat_new_conf_ini(locate.get_conf_file(), N_name, N_pwd)


def is_first_time_run():
    '''
    @summary: 根据conf.ini文件是否存在,判断是否是第一次运行
    @return: bool
    '''
    return not Util.is_file_exists(locate.get_run_folder()+'conf.ini')


def to_install_VC():
    '''
    @summary: 询问安装VC
    '''
    info_print('vc_0')
    info_print('vc_1')
    info_print('vc_2')
    info_print('vc_3')
    a = input('->')
    if a == "y":
        vc_x64_url = "https://download.visualstudio.microsoft.com/download/pr/3b070396-b7fb-4eee-aa8b-102a23c3e4f4/40EA2955391C9EAE3E35619C4C24B5AAF3D17AEAA6D09424EE9672AA9372AEED/VC_redist.x64.exe"
        vc_location = locate.get_resources_folder() + 'VCx64.exe'
        downloadFile(vc_x64_url, vc_location, "download.visualstudio.microsoft.com")
        Util.run_a_exe(vc_location)


def init_locate():
    '''
    @summary: 初始化路径信息
    '''
    global locate
    locate = Location()
    set_cookies_json_location(locate.get_resources_folder()+'Nexus_Cookies.txt')
    set_lib_location_location(locate.get_lib_folder())


def init_inject_func():
    '''
    @summary: 将一些函数分发到需要的地方
    '''
    set_loc_my_print_func(info_print)
    set_coo_my_print_func(info_print)


def run():
    info_print('000')
    info_print('001')
    info_print('002')
    info_print('003')
    info_print('004')
    info_print('005')
    info_print('006')
    info_print('007')
    input('->')

    init_inject_func()
    init_locate()

    # 信息获取
    is_first_time = is_first_time_run()
    if is_first_time:
        first_time_run()

    info_print('107')
    info_print('108')
    conf_ini = Conf_ini(locate.get_run_folder())

    info_print('109')
    username, userpwd = conf_ini.get_nexus_account_info()
    get_cookies_info(username, userpwd)

    info_print('200')
    info_print('201')
    file_page_html, is_spider = get_mod_file_page(conf_ini.is_safe_to_spide())
    if is_spider:  # 更新最后一次爬虫的时间信息
        conf_ini.set_new_last_spide_time()
    
    info_print('204_1')
    last_publish_date, last_download_url = analyze_mod_file_page(file_page_html)
    info_print('205')
    print("\t\t\t" + str(last_publish_date))
    info_print('206')
    print("\t\t\t" + last_download_url)
    last_publish_timeStamp = Util.transform_datetime_to_timeStamp(last_publish_date)
    installed_version_timeStamp = conf_ini.get_installed_SL_upload_date()
    if last_publish_timeStamp == installed_version_timeStamp:
        info_print('207')
        Util.warning_and_exit()

    info_print('208')
    download_page_html = spider_download_file_page(last_download_url)
    info_print('209')
    file_id, game_id = analyze_download_file_page(download_page_html)
    print('\t\tgame_id\t'+game_id, 2)
    print('\t\tfile id\t'+file_id, 2)

    info_print('210')
    download_url, file_type = spider_download_file(file_id, game_id)
    info_print('211')
    print("\t\t\t" + download_url)
    info_print('212')
    print("\t\t\t" + file_type)

    info_print('213')
    dl_loader_location = locate.get_resources_folder() + 'StrackerLoader.' + file_type
    downloadFile(download_url, dl_loader_location, 'cf-files.nexusmods.com')
# 英文化！！！！！！！！
#
    info_print('215')
    if file_type == 'zip':
        Util.unzip_all(dl_loader_location, locate.get_dl_loader_folder(), '')
    else:
        info_print('216')
        print('\t\t' + file_type)
        info_print('217')
        Util.warning_and_exit(1)

    info_print('218')
    old_mod_file_list = conf_ini.get_mod_file_list()
    if len(old_mod_file_list) > 0:
        info_print('219')
        for _file in old_mod_file_list:
            print('\t\t\t'+_file)
            if Util.is_file_exists(locate.get_mhw_folder()+_file):
                Util.delete_file(locate.get_mhw_folder()+_file)
            else:
                info_print('220')

    info_print('221')
    sl_file_list = Util.get_file_list_in_folder(locate.get_dl_loader_folder())
    info_print('222')
    print('\t\t\t' + str(sl_file_list))

    info_print('223')
    for _file in sl_file_list:
        print('\t\t' + _file)
        Util.copy_file(locate.get_dl_loader_folder()+_file, locate.get_mhw_folder()+_file)

    info_print('224')
    info_print('225')
    conf_ini.set_installed_SL_upload_date(last_publish_date)
    info_print('226')
    conf_ini.set_mod_file_list(sl_file_list)

    locate.save_to_conf_ini_file()
    info_print('227')

    if is_first_time:
        to_install_VC()

    print('3DM biss')
    Util.warning_and_exit(0)


# def init_webbrowser_driver(): 
#     # chrome 尝试
    # import requests
    # from lxml import etree
    # url_base = "http://npm.taobao.org"

    # r = requests.get("http://npm.taobao.org/mirrors/chromedriver/")
    # html = r.content.decode()
    # xpath_data = etree.HTML(html)
    # a = xpath_data.xpath('///html/body/div[1]/pre/a')[2:]

    # download_page_url_list = list()
    # for i in a:
    #     if i.xpath('./text()')[0].find("icon") != -1:
    #         break
    #     download_page_url_list.append(url_base + i.xpath('./@href')[0] + "chromedriver_win32.zip")
    
#     for i in download_page_url_list:
#         print(i)

#     Util.creat_a_folder(Util.get_lib_folder()+'chromedriver')
#     i = 0
#     Util.creat_a_folder(Util.get_lib_folder()+'chromedriver\\buffer')
#     for url in download_page_url_list:
#         location = Util.get_lib_folder()+'chromedriver\\buffer\\' + str(i) + '.zip'
#         t_headers = {g
#             'Host': "cdn.npm.taobao.org",
#             'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"}
#         response = requests.get(url, stream=True, headers=t_headers)
#         with open(location, 'wb')as f:
#             f.write(response.content)
#         i = i+1

#         unzip_location = Util.get_lib_folder()+'chromedriver\\' + str(i) + '.zip'
#         Util.unzip_all(location, unzip_location, '')   

        
if __name__ == "__main__":
    run()
    
    # init_locate()

    # conf_ini = Conf_ini(locate.get_run_folder())
    # l = conf_ini.get_mod_file_list()
    # print(l)
    # conf_ini.set_mod_file_list(['123.json',"678.json"])
    # l = conf_ini.get_mod_file_list()


    # print(l)
    # is_login(get_cookies_from_file())
    # print()
    # init_webbrowser_driver()
    # spider_download_file(9908, 2531)
    
    # run_folder_location = Util.get_run_folder()
    # downloaded_mod_location = run_folder_location+'\\resources\\StrackerLoader.' + "zip"
    # downloaded_mod_unpack_location = run_folder_location+'\\resources\\StrackerLoade\\'
    # Util.unzip_all(downloaded_mod_location, downloaded_mod_unpack_location, '')
    # a = is_first_time_run()
    # print(a)
    # print('3DM Biss')
    # Util.get_file_list_in_folder("F:\\Workspace\\CheckStrackerLoader")



    # with open(r'F:\Workspace\CheckStrackerLoader\dist\resources\mod_file_page.html')as f:
    #     html = f.read()
    # analyze_mod_file_page(html)