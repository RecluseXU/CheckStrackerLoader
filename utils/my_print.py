#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   my_print.py
@Time    :   2020/03/18 23:14:54
@Author  :   Recluse Xu
@Version :   1.0
@Contact :   444640050@qq.com
@License :   (C)Copyright 2017-2022, Recluse
@Desc    :   None
'''

# here put the import lib
import locale

_is_chinese = None

chinese_info_print_dict = {
    '000': '本程序由Recluse制作',
    '001': '本程序用于一键更新前置MOD Stracker\'s Loader',
    '002': '本程序不会用于盗号, 偷取信息 等非法操作',
    '003': '但由于源码是公开的, 可能存在被魔改成盗号程序的可能。故建议从github获取本程序。',
    '004': 'github地址：https://github.com/RecluseXU/CheckStrackerLoader',
    '005': 'B站联系地址：https://www.bilibili.com/video/av91993651',
    '006': 'https://www.nexusmods.com/monsterhunterworld/mods/2639',
    '007': '输入回车键开始',
    '100': '初始化',
    '101': '\t创建resources目录',
    '102': '\t创建lib目录',
    '103': '\t创建conf.ini',
    '104': '这次输入的信息会记录在conf.ini中，如果需要更改，用记事本修改conf.ini的内容即可',
    '105': '请输入N网账号或邮箱:',
    '106': '请输N网密码:',
    '107': '\t尝试获取 conf.ini信息',
    '108': '\t\t读取conf.ini',
    '109': '\t尝试获取 Cookies 信息',
    '110': '\t\tNexus_Cookies.json存在',
    '111': '\t\t\t尝试通过Nexus_Cookies.json获取Cookies信息',
    '112': '\t\t\t\tCookies信息验证成功，',
    '113': '\t\t\t\tCookies信息验证失败',
    '114': '\t\t尝试通过登录N网记录Cookies信息',
    '115': '\t\t尝试通过手动输入, 获知Cookies信息',
    '116': '\t\t\t\t手工输入的Cookies信息验证成功',
    '117': '\t\t\t\t手工输入的Cookies信息验证失败',
    '': '',
    '200': '获取MOD信息',
    '201': '\t尝试获取N网 "Stracker\'s Loader" 文件信息页',
    '202': '\t\t尝试通过爬虫得到 "Stracker\'s Loader" 文件页',
    '203': '\t\t由于爬虫等待时间未过，从本地记录中获取',
    '204': '\t\t\t获取成功',
    '204_1': '\t尝试分析文件页，得到 "Stracker\'s Loader" 最新版信息',
    '205': '\t\t最新版本上传日期(存在时区误差)',
    '206': '\t\t最新版本下载地址',
    '207': '已安装的版本与最新版发布时间一致，无需更新',
    '208': '\t尝试获取N网 "Stracker\'s Loader" 最新版文件下载页',
    '209': '\t尝试分析N网 "Stracker\'s Loader" 最新版文件下载页',
    '210': '\t尝试获取N网 "Stracker\'s Loader" 最新版文件下载url',
    '211': '\t\t最新版文件下载url',
    '212': '\t\t最新版文件类型',
    '213': '\t尝试下载"Stracker\'s Loader" 最新版文件',
    '214': '\t\t文件已保存为',
    '215': '\t尝试解压"Stracker\'s Loader" 文件',
    '216': '\t尚未编写该压缩文件类型解压方法',
    '217': '\t请自行尝试在已经下载好的文件中手动安装',
    '218': '\t检查是否要删除旧文件',
    '219': '\t\t尝试删除旧版\"Stracker\'s Loader\"文件',
    '220': '\t\t\t\t文件不存在',
    '221': '\t尝试获取\"Stracker\'s Loader\"文件信息',
    '222': '\t\t新下载的\"Stracker\'s Loader\"所包含的文件: ',
    '223': '\t尝试安装\"Stracker\'s Loader\"文件',
    '224': '\t更新安装信息',
    '225': '\t\t更新 已安装版本N网作者上传时间信息',
    '226': '\t\t更新 已安装版本文件 信息',
    '227': '\t\t程序运行完毕',
    '': '',
    'vc_0': '\t需要安装VC吗？',
    'vc_1': '\t\t这个是Stracker\'s Loader的运行库。没有安装这个,但安装了Stracker\'s Loader，会进不了游戏。',
    'vc_2': '\t\t要是你不确定是否已经安装，那么建议安装.',
    'vc_3': '\t\t输入y开始下载安装，输入其他跳过',
    '': '',
    'loc_0': '尝试获取MHW目录',
    'loc_1': '\t尝试从conf.ini中获取 MHW 目录',
    'loc_2': '\t尝试从注册表获取 MHW 目录',
    'loc_3': '请手动选择 MHW 目录',
    'loc_4': '尝试获取MHW路径失败',
    '': '',
    'Coo_0': '\t\t\t尝试初始化浏览器',
    'Coo_1': '\t\t\t\t尝试初始化 Chrome 浏览器',
    'Coo_2': '\t\t\t\t尝试初始化 Firefox 浏览器',
    'Coo_3': '\t\t\t\t尝试初始化 IE 浏览器',
    'Coo_4': '\t\t\t尝试初始化浏览器失败',
    'Coo_5': '\t\t\t登录界面',
    'Coo_6': '\t\t\t请在页面中登录N网账户',
    'Coo_7': '\t\t\t如果设置在conf.ini的账户密码正确，这个过程会自动完成。',
    'Coo_8': '\t\t\t如果不正确，请手动输入账户密码',
    'Coo_9': '\t\t\t每一步操作都设置了一定的的可行时间，超过时间程序就会退出',
    'Coo_10': '\t\t\t等待进入首页Cookies，请勿操作',
    'Coo_11': '\t\t\t尝试手动获取Cookies信息？(输入y代表尝试，输入其他东西代表不尝试并退出)',
    'Coo_12': '\t\t\t请输入手动获取的cookies:',
    '': '',
}
english_info_print_dict = {

}


def info_print(info_num):
    '''
    @summary: 根据信息号码 和 是否为中文输出内容
    '''
    if _is_system_using_chinese():
        print(chinese_info_print_dict[info_num])
    else:
        print(english_info_print_dict[info_num])


def _is_system_using_chinese():
    '''
    @summary: 判断系统是否在使用中文
    '''
    global _is_chinese
    if _is_chinese is None:
        if locale.getdefaultlocale()[0] == "zh_CN":
            _is_chinese = True
        else:
            _is_chinese = False
    return _is_chinese
