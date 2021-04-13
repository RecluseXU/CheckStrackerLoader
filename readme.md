由于MHW已经停止更新，StrackerLoader也无需更新，所以此程序已经变得并没有什么意义  

## 基本信息  
由于卡表收紧了对MOD的接口，导致很多文件不再支持。  
为了应对这种情况，国外有大佬利用逆向技术，制造了一个名为 StrackerLoader 的插件来重新开放这些接口。  
StrackerLoader：https://www.nexusmods.com/monsterhunterworld/mods/1982  
StrackerLoader这个插件在MHW更新的时候也需要跟着更新。  

为了方便更新这个插件，我打算制作一个一键更新插件的程序，来优化这个过程。（尽管这个过程也不复杂）  
github地址：https://github.com/RecluseXU/CheckStrackerLoader   

本程序不会用于盗号, 偷取信息 等非法操作  
但由于源码是公开的, 可能存在被魔改成非法程序的可能  
故建议从github或者N网获取本程序  


## 这个程序做了什么  
1. 检查你电脑的注册表，获知你MHW目录路径  
2. 然后检查你是否装了 StrackerLoader ，记录一些有用的信息  
3. 程序会通过 selenium ，使用账户和密码登录Nexus，获取cookies信息  
4. 爬虫访问 Nexus 的 StrackerLoader 的 MOD 页，检查配对 StrackerLoader 这个MOD是否已经更新  
如果更新了，程序会自动地下载最新版本的 StrackerLoader 并安装到MHW目录
没有更新，则给出提示后结束

程序对爬虫的间隔做了限制，仅仅允许用户以30s一次或更慢的频率来查询N网StrackerLoader这个MOD的信息。  
对于少于这个间隔的运行，程序并不会执行爬虫，而是在上一次爬虫的结果中获取信息。  

这个登录的过程大多数时候会在第一次使用本程序的时候发生，因为程序还没有获悉cookies。  
当你成功登录后，获取的cookies信息会保存在本地
在你下一次使用这个程序的时候，程序并不会立刻通过网页登录，而是先检查本地信息是否有效，若是有效则使用旧信息访问，以此减少不必要的访问


## 版本信息
v1.1  
   紧急修复了输入密码后会崩溃的BUG  
v1.2  
  添加IE webdriver作为兜底，从而修复没Chrome就会崩溃的情况  
  修改一些参数  
v1.3   
  添加了手动输入cookies项  
  添加了手动输入MHW路径项  
  添加了firefox webdriver  
  更改部分代码结构  
v1.4  
  修正了使用手动输入MHW路径安装的时候出现安装错误的情况  
  添加了下载进度显示  
v1.5
  去除调整 utils.ini.py 结构  
  增加 utils.location_helper.py 用来处理路径  
  添加 MHW 路径记录功能  
  添加 VC 下载功能  
  修复了lib地址传递错误的问题  
v1.6  
  适配新的“StrackerLoader”  
  调整获取cookies的逻辑，使得多个浏览器都能尝试  
  添加MOD文件记录，在安装新版本的时候会删除旧版本的文件  
  删除了dll的MD5校验比对功能，因为“StrackerLoader”以后可能会经常变  
  更改安装逻辑  
v1.7  
  单独抽取出输出内容做为一个模块 my_print.py  
  调整部分描述  
  修复了VC安装功能由于Cookies导致的错误  
  增加了英文输出，但是并没有测试(Add English log, But there was no test)



## 其他
自己家里打包代码：F:\Environment\Python\envs\CheckStrackerLoader\Scripts\pyinstaller --workpath F:\Workspace\CheckStrackerLoader\pyinstaller_rubbish -y -F -i F:\Workspace\CheckStrackerLoader\1.ico main.py  


2020年3月10日18:04:01
