#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   ini.py
@Time    :   2020/02/24 09:40:57
@Author  :   Recluse Xu
@Version :   1.0
@Contact :   444640050@qq.com
@License :   (C)Copyright 2017-2022, Recluse
@Desc    :   None
'''

# here put the import lib
import configparser
import time
import datetime


class Conf_ini(object):
    config = configparser.ConfigParser()

    def __init__(self, run_location):
        
        self.ini_location = run_location + '/conf.ini'
        self.config.read(self.ini_location, encoding='utf-8')

    def get_installed_SL_upload_date(self):
        '''
        @return: 获取已经被安装上了的MOD的上传时间(时间戳):int
        '''
        return int(self.config.get('StrackerLoader', 'installed_mod_upload_date'))

    def set_installed_SL_upload_date(self, the_time: datetime):
        '''
        @summary: 设置已经被安装上了的MOD的上传时间
        '''
        the_time = int(time.mktime(the_time.timetuple()))
        self.config.set("StrackerLoader", "installed_mod_upload_date", str(the_time))
        self.write_conf()

    def get_last_spide_time(self):
        '''
        @return: 上一次爬虫的时间戳:int
        '''
        return int(self.config.get('StrackerLoader', 'last_spide_time'))

    def set_new_last_spide_time(self):
        '''
        @summary: 设置新的爬虫时间戳
        '''
        now = datetime.datetime.now()
        now = int(time.mktime(now.timetuple()))
        self.config.set("StrackerLoader", "last_spide_time", str(now))
        self.write_conf()

    def is_safe_to_spide(self):
        '''
        @summary: 根据爬虫间隔，返回是否应爬虫
        '''
        now = datetime.datetime.now()
        now = int(time.mktime(now.timetuple()))
        wating_time = now - self.get_last_spide_time()
        if wating_time > 30:
            return True
        return False

    def get_nexus_account_info(self):
        '''
        @summary: 从设置中查询 N 网账户信息
        @return: user_name:str, user_password:str
        '''
        user_name = self.config.get('NexusAccount', 'user_name')
        user_password = self.config.get('NexusAccount', 'user_password')
        return user_name, user_password

    def set_nexus_account_info(self, user_name, user_password):
        '''
        @summary: 设置 N 网账户信息
        '''
        self.config.set('NexusAccount', 'user_name', user_name)
        self.config.set('NexusAccount', 'user_password', user_password)
        self.write_conf()

    def get_mod_file_list(self):
        '''
        @summary: 得到已经安装了的前置MOD的 文件列表
        @return: list
        '''
        file_list = self.config.get('StrackerLoader', 'mod_files')
        if len(file_list) == 0:
            return []
        if isinstance(file_list, str):
            file_list = file_list.replace(' ', '')
            if len(file_list) == 0:
                return []
            file_list = file_list.replace('\'', '').replace('\"', '').split(',')
        return file_list

    def set_mod_file_list(self, file_list: list):
        '''
        @summary: 设置已经安装了的前置MOD的 文件的信息
        '''
        self.config.set('StrackerLoader', 'mod_files', str(file_list)[1:-1])
        self.write_conf()

    def write_conf(self):
        '''
        @summary: 配置持久化
        '''
        with open(self.ini_location, "w", encoding="utf-8")as f:
            self.config.write(f)

    @staticmethod
    def creat_new_conf_ini(loaction, N_name, N_pwd):
        '''
        @summary: 初始化,创建 conf.ini
        '''
        config = configparser.ConfigParser()

        config.add_section("StrackerLoader")
        config.set("StrackerLoader", "installed_mod_upload_date", "0")
        config.set("StrackerLoader", 'last_spide_time', "0")
        config.set("StrackerLoader", 'mod_files', "")

        config.add_section("NexusAccount")
        config.set("NexusAccount", "user_name", N_name)
        config.set("NexusAccount", "user_password", N_pwd)

        with open(loaction, "w") as f:
            config.write(f)
