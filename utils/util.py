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
import zipfile
import shutil
import datetime
from tkinter.filedialog import askdirectory


class Util(object):

    @staticmethod
    def run_a_exe(location: str):
        '''
        @summary: 运行一个exe文件
        '''
        os.system(location)

    @staticmethod
    def creat_a_folder(location: str):
        '''
        @summary: 在程序目录下创建resources文件夹
        '''
        if os.path.exists(location) is False:
            os.mkdir(location)


    @staticmethod
    def get_Firefox_Install_Address():
        '''
        @return: FireFox目录:str
        '''
        try:
            aReg = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
            aKey = winreg.OpenKey(
                aReg, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall")
            i = 0
            while 1:
                i = i+1
                keyname = winreg.EnumKey(aKey, i)
                if(keyname.find('Firefox') != -1):  # 因为firefox在注册表里的键带着一个版本号，所以不能写死，这里通过关键词找到键名
                    print(keyname)
                    break

            aKey = winreg.OpenKey(
                aReg, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\\" + keyname)
            data = winreg.QueryValueEx(aKey, "InstallLocation")[0]
            return data + '\\'
        except Exception as e:
            print("->Fail\t可能此电脑未安装Firefox", e)
            aKey.close()

    @staticmethod
    def is_file_exists(file_path: str):
        '''
        @summary: 检测路径下的文件是否都已经存在
        @return: :bool
        '''
        return os.path.exists(file_path)

    @staticmethod
    def get_file_MD5(file_location):
        '''
        @staticmethod
        @return: 返回目标文件的MD5:str
        '''
        try:
            with open(file_location, 'rb')as f:
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
        @staticmethod
        @summary: 简单输出
        '''
        for i in range(space):
            print('\t', end="")
        print(info)

    @staticmethod
    def warning_and_exit(statue_code=0):
        '''
        @staticmethod
        @summary: 警告用户这个程序将在10s后退出
        '''
        print('将在 10 秒后自动退出')
        time.sleep(10)
        exit(statue_code)

    @staticmethod
    def unzip_single(src_file, dest_dir, password):
        '''
        @staticmethod
        @summary: 从zip压缩包中解压单个文件到目标文件夹。
        '''
        if password:
            password = password.encode()
        zf = zipfile.ZipFile(src_file)
        try:
            zf.extractall(path=dest_dir, pwd=password)
        except RuntimeError as e:
            print(e)
        zf.close()

    @staticmethod
    def unzip_all(source_dir: str, dest_dir: str, password: str):
        '''
        @staticmethod
        @summary: 从zip压缩包中解压多个文件
        '''
        if not os.path.isdir(source_dir):    # 如果是单一文件
            Util.unzip_single(source_dir, dest_dir, password)
        else:
            it = os.scandir(source_dir)
            for entry in it:
                if entry.is_file() and os.path.splitext(entry.name)[1] == '.zip':
                    Util.unzip_single(entry.path, dest_dir, password)

    @staticmethod
    def copy_file(origin_file_location, copy_file_location):
        '''
        @staticmethod
        @summary: 复制一个文件到目标路径, 若已经存在，则覆盖
        '''
        try:
            shutil.copyfile(origin_file_location, copy_file_location)
        except Exception as e:
            print(e)
            Util.warning_and_exit(1)

    @staticmethod
    def transform_datetime_to_timeStamp(d_time: datetime):
        '''
        @staticmethod
        @summary: 将datetime对象转换为时间戳，返回
        @return: timeStamp:int
        '''
        timeStamp = int(time.mktime(d_time.timetuple()))
        return timeStamp

    @staticmethod
    def is_win_x64():
        '''
        @staticmethod
        @summary: 返回操作系统是否是64位
        @return: bool
        '''
        return 'PROGRAMFILES(X86)' in os.environ


if __name__ == "__main__":
    # lacate = Util.get_run_folder()
    # print(lacate)
    a = Util.is_win_x64()
    print(a)
