import os
import re
from option import options
from datetime import datetime, timedelta

try:
	from bs4 import BeautifulSoup
except ImportError:
	os.system("pip3 install beautifulsoup4")
	os.system("pip3 install lxml")
	from bs4 import BeautifulSoup
#新功能，将直接下载所需文件

def get_time(time, delta):
	time = datetime.strptime(f"{year}-{month}-{day} {time}:00", "%Y-%m-%d %H:%M:%S") + timedelta(days=delta)
	return time.strftime("%Y%m%dT%H%M%S")
	#将得到的日期格式化，并在现有日期上增加delta日

def get_str(name, loc, start_time, end_time, delta):
	#ics格式化
	str = 'BEGIN:VEVENT\n'
	#开始event
	str += f"DTSTART;TZID=Asia/Shanghai:{get_time(start_time, delta)}\n"
	str += f"DTEND;TZID=Asia/Shanghai:{get_time(end_time, delta)}\n"
	#开始时间和结束时间
	if opt.watch_mode is True:	
		str += f"SUMMARY:{name}{loc}\n"
	#手表上无法显示地点，因此加在名字后面
	elif opt.precise_location is True:
		str += f"SUMMARY:{name}\n"
		str += f"LOCATION:广东省广州市龙溪大道省实路1号 {loc}\n"
	#防止苹果识别错误
	else:
		str += f"SUMMARY:{name}\n"
		str += f"LOCATION:{loc}\n"
	#加入课程名称和地点名称
	if opt.repeat is True:
		str += f"RRULE:FREQ=WEEKLY;UNTIL={get_time(start_time, opt.repeat_weeks * 7)}\n"
	#每周重复课程
	if opt.alarms is True:
		str += f"BEGIN:VALARM\n"
		str += f"TRIGGER:-PT{opt.alarm_set_time}M\n"
		if opt.alarm_mode == "audio" or opt.alarm_mode == 'all':
			str += f"ACTION:AUDIO\n"
		if opt.alarm_mode == "display" or opt.alarm_mode == 'all':
			str += f"ACTION:DISPLAY\n"
		str += f"END:VALARM\n"
	#添加警报
	str += 'END:VEVENT\n'
	#结束课程
	return str

def check(name):
	if opt.exclude is False:
		return False
	#如果不删除某些课程，直接退出
	for str in opt.exclude_class:
		if name.count(str) > 0:
			return True
	#如果这个课程应该被删除，则删除
	return False

def check_next(k):
	return k.attrs == {'class': ['fc-highlight-container']}

if __name__ == '__main__':

	opt = options().get_opt()
	print(opt)
	#opt中存的是个性化设置中的内容

	with open(opt.read_path,"r") as f:
		data=f.read()
	#读取html文件

	soup = BeautifulSoup(data, 'lxml')
	divs = soup.find_all('div')
	h2 = soup.find_all('h2')
	#处理成需要的样子
	#内容存储于div中
	#日期存储于h2中（作为标题和表头存在）
	
	# with open("debug.txt","w") as f:
	# 	f.write(soup.prettify())
	#用于debug
	
	for k in h2:
		if k.string is not None:
			date_list = re.findall(r"\d+", k.string)
			#用于寻找日期
			# print(date_list, k.string)
			year = date_list[0]
			month = date_list[1]
			day = date_list[2]
			#分别找到年月日
			# print(opt.year,opt.month,opt.day)
			break

	classes = []
	flag = False #看课表是否出现
	pointer = 0  #星期几
	deltas = []  #星期几
	for i in range(len(divs)):
		k = divs[i]
		if k.string is not None:
			flag = True
			if k.string == "确定":
				continue
			#由于中间可能有杂七杂八的东西和其他的空格
			#但是在“确定”之后一定是课表
			#最近更新2023.11.15
			classes.append(k.string)
			deltas.append(pointer)
			
		if flag and i+2 < len(divs) and check_next(divs[i+2]):
			pointer += 1
		#经过查询，发现列的换行符为'fc-highlight-container'
		#因此每一次发现'fc-highlight-container'日期就加一

	#此时classes已经存储了所有的信息
	#classes格式为 ["课程名字 时间","地点"]...

	str = ""

	for k in range(len(classes)//2):
		i,j = 2 * k, 2 * k + 1
		name = classes[i][:-11]
		if(check(name)):
			continue
		time = classes[i][-11:]
		#i,j分别为课程名字和地点的下标
		#时间长度固定为11位，所以分别取最后11位(时间)和其他位置(课程名称)
		#时间格式为 HH:MM - HH:MM, 为课程开始到截止的时间
		time_start, time_end = time.split('-')
		loc = classes[j]
		str += get_str(name, loc, time_start, time_end, deltas[k * 2])
		#将信息制成.ics文件格式
		# name是课程名称
		# time是时间
		# loc是地点

	str += "END:VCALENDAR\n"
	#结束写入.ics文件

	with open(opt.save_path, "a") as f:
		f.write(str)
	#将信息写入.ics文件