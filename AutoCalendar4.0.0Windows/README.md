# SSAP-auto-calendar
# 需要安装 python 3.4 及以上版本 和 pip

python推荐安装最新版            
[安装教程](https://zhuanlan.zhihu.com/p/635089472)                            
按照上面步骤一步步来，不可能安不上。              
[python下载链接](https://www.python.org/downloads/)
~~实在不行就打劫身边一个会python的同学帮你装~~                 
python 3.4 及以上版本都预装了 pip            

#效果展示
![效果图](https://github.com/tongtongtot/SSAP-auto-calendar/assets/55981482/1bc134a6-296e-46f8-a41c-467436506d71)

## SSAP-auto-calendar for mac 教程：

1.打开schoolpal的我的日程

2.使用Chrome/Edge下载HTML文件 注意选择 网页，全部  （此时会下载一个 我的日程.html 文件和一个文件夹）

3.在右边的Release中下载mac版本并解压

4.把“我的日程.html”移动至刚才解压出来的文件夹

5.双击start文件启动      

6.把export.ics拖动至日历

## SSAP-auto-calendar for Windows 教程：   

1.打开schoolpal的我的日程

2.使用Chrome/Edge下载HTML文件 注意选择 网页，全部 （此时会下载一个 我的日程.html 文件和一个文件夹）

3.在右边的Release中下载Windows版本并解压

4.把“我的日程.html”移动至刚解压出来的文件夹

5.双击start.bat启动         

6.把export.ics拖动至日历


## Q&A
Q1: 每一次使用的时候需要删除export.ics吗？       
A1: 不需要。

Q2: 为什么我双击了 start.bat 跳出来了 Windows store？      
A2: 因为没有设置环境变量，请卸载python并按照上面的教程重新装载(推荐)          
或者参考[这个教程](https://www.jianshu.com/p/a5c5148b7434)的解决方案(不推荐)          
原因一般是环境变量没有设置好，所以方法二一般没有用。          
如果确认了python已经安装并且会调整环境变量(此处特指Path变量)，请自行调整，但请自负风险。                

Q3: 我用的是虚拟机，我已经按照教程装载了 python ,为什么还是没有办法使用 python ？      
A3: 虚拟机的路径不太一样，建议在 C:/ 下重新装python, 否则环境变量可能无法识别。             

Q4: 有什么自定义功能吗？      
A4:       
1.可以自定义读取的文件 (使用 --read_path your_path),    
2.可以自定义输出的文件 (使用 --save_path your_path),              
3.可以自定义是否不显示某些课程 (使用 --exclude 默认不显示升旗和早晚自习),              
4.可以自定义不显示课程的名称 (使用 --exclude --exclude_class class_name(课程名称/课程名称的一部分) 注：只要名字有包含添加的字符就会删去，支持添加多个课程，课程之间用空格连接),      
&emsp; 4.1.若不想重新输入所有课程，只想增加不显示的课程名称的话，请使用 --exclude --exclude_extra class_name 即可,     
&emsp; 4.2.可以自定义不显示星期几的课程 (使用 --exclude --exclude_dateofWeek 日期(星期几) 即可)
e.g. python3 main.py --exclude --exclude_extra FAP 辅导 --exclude_dateofWeek 3 4 5 的意思是：不显示某些课程，除了默认不显示的课程外，也不显示字段中存在"FAP"和"辅导"的课程，并且不显示星期一和星期二的课程。
5.可以自定义是否使用开始前提示 (使用 --alarms 默认提前5分钟, 使用 --alarm_set_time minutes 来修改提前的时间),                 
6.可以自定义提醒的方式 (使用 --alarm_mode mode 目前支持 "display" 和 "audio" 两种模式),             
7.可以自定义是否重复日历(按周重复，默认关闭，默认20周 使用 --repeat 打开该功能 使用 --repeat_weeks week 来修改默认值),   
8.添加了手表模式，可以将地址添加到名称后面防止手表无法显示地址的问题 使用 --watch_mode 打开该功能,               
9.添加了精细地点模式，修复了某些地图APP搜索位置错误的bug 使用 --precise_location 打开该功能,                    

Q5: 如果我的课表并不整齐(比如第三节没课) 或者 有一天因为放假全天没课，这个还可以正常显示吗？                     
A5: 可以的。但是这个方法目前仍然在公测阶段，需要各位的bug反馈来敲定最终的方法      

Q6: 为什么有换回第一次用另外一个文件下载环境了？             
A6: ~~不然代码会很丑很抽象，还不如这样写。~~             
A6改: 你TM之前都改了什么东西啊，明明就不用这么抽象

Q7: 我有 bug 想要 report, 有没有作者的联系方式？            
A7: 可以在 github 上 report, 也可以联系作者的邮箱: tongtongtot@163.com            

Q8: 为什么想要写Lite版本,删除了多少功能?
A8: 经过调查，大部分的功能(如“重复日历”“精确地址”等功能)并未被使用，这些功能只会让项目变得臃肿。另外，原先的代码存在有不少隐患，可能会为之后新增功能带来不少麻烦，因此长痛不如短痛选择将其全部删除。但是请放心，常用的功能仍然可以自定义(如自定义输入输出路径，不显示课程和手表模式)，完成版也绝对不会收费/打广告，请放心使用。

------

## SSAP-auto-calendar 4.0 教程

**全自动处理是基于Chrome的,所以在使用之前请确认您的电脑已经安装了Chome。**

**我们建议您下载/更新最新版本的Chrome以免遇到无法下载依赖库的问题。**

SSAP-auto-calendar 4.0是全自动处理，您只需双击start文件即可全自动运行。                             

使用时请先打开calendar.config文件，并在填写您的账号与密码以继续使用。                    

我们不会也不能获取到您的密码，您的密码仅仅会保存在本地(您的电脑)和https://sendeltastudent.schoolis.cn/网站上，所以请放心使用。

初次打开可能比较慢，因为需要下载依赖包，时间视您使用的网络而有波动，请您稍作等待。

感谢您使用我们的产品，也欢迎您提供宝贵的意见与建议。
