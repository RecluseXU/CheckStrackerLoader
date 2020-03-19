#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   location_helper.py
@Time    :   2020/03/10 13:42:51
@Author  :   Recluse Xu
@Version :   1.0
@Contact :   444640050@qq.com
@License :   (C)Copyright 2017-2022, Recluse
@Desc    :   None
'''

# here put the import lib
import os
import winreg
import time
import configparser
from tkinter.filedialog import askdirectory

_info_print_func = None


class Location(object):
    def __init__(self):
        self.run_folder = os.path.abspath(os.curdir)+"\\"

        self.conf_ini_file = self.run_folder+'conf.ini'
        self.resources_folder = self.run_folder + 'resources\\'
        self.lib_folder = self.run_folder + 'lib\\'
        self.cookies_txt_file = self.resources_folder + "Nexus_Cookies.txt"
        self.dl_loader_folder = self.resources_folder + 'StrackerLoade\\'

        self.mhw_folder = _get_MHW_Install_Address(self.conf_ini_file)

    def get_run_folder(self):
        '''
        @return: 返回程序运行的目录的路径:str
        '''
        return self.run_folder

    def get_resources_folder(self):
        '''
        @return: 返回程序运行目录下的resources目录的路径:str
        '''
        return self.resources_folder

    def get_lib_folder(self):
        '''
        @return: 返回程序运行目录下的lib目录的路径:str
        '''
        return self.lib_folder

    def get_conf_file(self):
        '''
        @return: 返回程序运行目录下conf.ini的路径:str
        '''
        return self.conf_ini_file

    def get_mhw_folder(self):
        '''
        @return: 返回程序运行目录下的lib目录的路径:str
        '''
        return self.mhw_folder

    def get_cookies_txt_file(self):
        '''
        @return: 返回记录cookies的文件的路径
        '''
        return self.cookies_txt_file

    def get_dl_loader_folder(self):
        '''
        @return: 返回资源文件夹下的strackloader目录
        '''
        return self.dl_loader_folder

    def save_to_conf_ini_file(self):
        '''
        @summary: 将路径记录保存到文件中
        '''
        config = configparser.ConfigParser()
        config.read(self.conf_ini_file, encoding='utf-8')
        if "Locations" not in config.sections():
            config.add_section("Locations")
        config.set("Locations", "mhw_folder", self.mhw_folder)
        with open(self.conf_ini_file, "w") as f:
            config.write(f)


def _is_file_exists(file_path: str):
    '''
    @summary: 检测路径下的文件是否都已经存在
    @return: :bool
    '''
    return os.path.exists(file_path)


def _is_effective_MHW_location(location):
    '''
    @summary: 检测路径是否为MHW目录，通过其下是否有mhw启动程序判断。
    @return: :bool
    '''
    return _is_file_exists(location+"MonsterHunterWorld.exe")


def _warning_and_exit(statue_code=0):
    '''
    @summary: 警告用户这个程序将在10s后退出
    '''
    print('将在 10 秒后自动退出')
    time.sleep(10)
    exit(statue_code)


def _get_MHW_Install_Address(conf_ini_file):
    '''
    @return: MHW目录:str
    '''
    _info_print('loc_0')
    _info_print('loc_1')
    if _is_file_exists(conf_ini_file):
        try:
            config = configparser.ConfigParser()
            config.read(conf_ini_file, encoding='utf-8')
            mhw_folder = config.get('Locations', 'mhw_folder')
            if _is_effective_MHW_location(mhw_folder):
                return mhw_folder
        except Exception as e:
            print("失败", e)

    _info_print('loc_2')
    try:
        aReg = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
        aKey = winreg.OpenKey(
                aReg, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\Steam App 582010")
        data = winreg.QueryValueEx(aKey, "InstallLocation")[0]
        location = data + '\\'
        # 验证是否真的是存在的
        if _is_effective_MHW_location(location):
            return location
    except Exception as e:
        print("失败", e)

    _info_print('loc_3')
    try:
        location = askdirectory() + "/"
        if _is_effective_MHW_location(location):
            return location
    except Exception as e:
        print("失败", e)

    _info_print('loc_4')
    _warning_and_exit(1)


'''
for print
'''


def _info_print(info_num):
    '''
    @summary: 根据信息号码 和 是否为中文输出内容
    '''
    global _info_print_func
    _info_print_func(info_num)


def set_info_print_func(func):
    '''
    @return: 设置输出函数
    '''
    global _info_print_func
    _info_print_func = func


if __name__ == "__main__":
    l = Location()
    l.save_to_conf_ini_file()
    a = l.get_mhw_folder()
    print(a)
    a = _is_effective_MHW_location(a)
    print(a)