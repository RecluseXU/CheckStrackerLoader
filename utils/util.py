#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   util.py
@Time    :   2020/02/24 10:13:15
@Author  :   Recluse Xu
@Version :   1.0
@Contact :   444640050@qq.com
@License :   (C)Copyright 2017-2022, Recluse
@Desc    :   None
'''

# here put the import lib
import winreg
import hashlib
import os
import time


class Util(object):
    @staticmethod
    def get_MHW_Install_Address():
        '''
        @return: MHW目录
        '''
        try:
            aReg = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
            aKey = winreg.OpenKey(aReg, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\Steam App 582010")
            data = winreg.QueryValueEx(aKey, "InstallLocation")[0]
            Util.info_print(data, 2)
            return data
        except Exception as e:
            print("->Fail", e)
            Util.warning_and_exit(1)

    @staticmethod
    def is_file_exists(file_path: str):
        '''
        @summary: 检测路径下的文件是否都已经存在
        @return: :bool
        '''
        return os.path.exists(file_path)
    
    @staticmethod
    def get_run_folder():
        '''
        @staticmethod
        @return: 返回程序运行的目录:str
        '''
        location = os.path.abspath(os.curdir)
        Util.info_print(location, 2)
        return location

    @staticmethod
    def get_file_MD5(file_location, file_name):
        try:
            with open(file_location + '\\' + file_name, 'rb')as f:
                file_bytes = f.read()
            md5_str = hashlib.md5(file_bytes).hexdigest()
            Util.info_print(md5_str, 2)
            return md5_str
        except Exception as e:
            print("->失败", e)
            Util.warning_and_exit(1)
    
    @staticmethod
    def info_print(info, space=0):
        '''
        @summary: 美化输出
        '''
        for i in range(space):
            print('\t', end="")
        print(info)
    
    @staticmethod
    def warning_and_exit(statue_code=0):
        '''
        @summary: 警告用户这个程序将在10s后退出
        '''
        print('将在 10 秒后自动退出')
        time.sleep(10)
        exit(statue_code)



if __name__ == "__main__":
    lacate = Util.get_run_folder() + '\\utils\\ini.py'
    print(lacate)
    a = Util.is_file_exists(lacate)
    print(a)