import time
import os
import re
import argparse
from configparser import ConfigParser
from datetime import datetime, timedelta

try:
	from bs4 import BeautifulSoup
except ImportError:
    os.system("pip3 install beautifulsoup4")
    os.system("pip3 install lxml")
    from bs4 import BeautifulSoup

try:
    from chromedriver_py import binary_path
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.action_chains import ActionChains
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
except ImportError:
    os.system("pip3 install selenium")
    from chromedriver_py import binary_path
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

try:
    import chromedriver_autoinstaller
except ImportError:
    os.system("pip3 install chromedriver_autoinstaller")
#下载所需文件

class options():    
    def get_opt(self):
        parser = argparse.ArgumentParser()

        parser.add_argument("--save_path", type=str, default='课表.ics', help="The path to store the calender.")
        # parser.add_argument("--read_path", type=str, default="我的日程.html", help="The read path.")

        parser.add_argument("--exclude", action="store_true", default=False, help="Whether to exclude some class or not.")
        parser.add_argument("--exclude_class", nargs='+', default=["早自习","升旗","晚自习","早读","期末考","期中考"], help="The name of the classes that are being removed")
        parser.add_argument("--exclude_dateofWeek", nargs='+', default=[], help="Exclude classes that you are not going to school (For some Reason XD).")
        parser.add_argument("--exclude_extra",nargs='+', default=[], help="Easier ways to exclude classes that you are not going to take (For some Reason XD).")

        parser.add_argument("--watch_mode", action="store_true", default=False, help="Show location on watches")
        
        self.opt = parser.parse_args()
        return self.opt
#options类

if __name__ == '__main__':

    opt = options().get_opt()
    config = ConfigParser()
    config.read('calendar.config', 'utf-8')

    option = webdriver.ChromeOptions()
    option.add_argument("headless")
    browser = webdriver.Chrome(options=option)
    
    browser.get(r'https://sendeltastudent.schoolis.cn/')
    browser.encoding = 'utf-8'

    wait = WebDriverWait(browser,10,0.5)
    wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, 'input')))
    inputTags = browser.find_elements(By.TAG_NAME, "input")
    inputTags[0].send_keys(config['account']['name'])
    inputTags[1].send_keys(config['account']['password'])

    login_buttons = browser.find_elements(By.TAG_NAME, "button")
    ActionChains(browser).click(login_buttons[0]).perform()

    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'body > div.ng-scope > div > topbar > div > div > div > span:nth-child(3)')))
    schedule_button = browser.find_element(By.CSS_SELECTOR,'body > div.ng-scope > div > topbar > div > div > div > span:nth-child(3)')
    ActionChains(browser).click(schedule_button).perform()
    
    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,'body > div.ng-scope > div > ui-view > div > schedule > div > xb-my-calendar-with-print > div.ng-pristine.ng-untouched.ng-valid.ng-isolate-scope.fc.fc-unthemed.fc-ltr.ng-not-empty > div.fc-view-container > div > table > tbody > tr > td > div.fc-scroller.fc-time-grid-container > div > div.fc-content-skeleton > table > tbody > tr > td:nth-child(2) > div > div:nth-child(2) > a.fc-time-grid-event.fc-v-event.fc-event.fc-start.fc-end.fc-short > div.fc-content')))
    data = browser.page_source

    browser.close()

    with open(opt.save_path, "w", encoding='utf-8') as f:
        f.write("BEGIN:VCALENDAR\nVERSION:2.0\nCALSCALE:GREGORIAN\nMETHOD:PUBLISH\nCLASS:PUBLIC\nBEGIN:VTIMEZONE\nTZID:Asia/Shanghai\nTZURL:http://tzurl.org/zoneinfo-outlook/Asia/Shanghai\nX-LIC-LOCATION:Asia/Shanghai\nBEGIN:STANDARD\nTZOFFSETFROM:+0800\nTZOFFSETTO:+0800\nTZNAME:CST\nEND:STANDARD\nEND:VTIMEZONE\n")
    #撰写头文件并覆盖之前内容
        
    soup = BeautifulSoup(data, 'lxml')
    divs = soup.find_all('div')
    h2 = soup.find_all('h2')
    #处理成需要的样子
    #内容存储于div中
    #日期存储于h2中（作为标题和表头存在）

    for k in h2:
        if k.string is not None:
            date_list = re.findall(r"\d+", k.string)
            #用于寻找日期
            year = date_list[0]
            month = date_list[1]
            day = date_list[2]
            #分别找到年月日
            break

    classes,loc,flag,typ = [],[],False,0
    pointer,deltas = 0,[]
    #class存储课表,loc存储上课位置,typ判断目前搜索到了课表/上课地点; flag看课表是否出现; pointer和delta用于标记这个课程时星期几

    def check_next(k):
        return k.attrs == {'class': ['fc-highlight-container']}

    for i in range(len(divs)):
        k = divs[i]
        if k.string is not None:
            flag = True
            if k.string == "确定":
                continue
            #由于中间可能有杂七杂八的东西和其他的空格
            #但是在“确定”之后一定是课表
            #最近更新2024.03.03
            if typ == 0:
                classes.append(k.string)
                deltas.append(pointer)
            else:
                loc.append(k.string)
            typ = 1 - typ
            #课表内容和位置交替出现
            
        if flag and i+2 < len(divs) and check_next(divs[i+2]):
            pointer += 1
        #经过查询，发现每个表格都在不同的class中且class的名称都会包含'fc-highlight-container'
        #因此每一次发现'fc-highlight-container'日期就加一

    #此时classes和loc数组已经存储了所有需要用到的信息
    #classes格式为["课程名字 时间"]...

    def check(name, pos):
        if opt.exclude is False:
            return False
        #如果不删除某些课程，直接退出
        if len(opt.exclude_dateofWeek) > 0:
            if str(pos) in opt.exclude_dateofWeek:
                return True
        for s in opt.exclude_class:
            if name.count(s) > 0:
                return True
        for s in opt.exclude_extra:
            if name.count(s) > 0:
                return True
        #如果这个课程应该被删除，则删除
        return False

    def get_time(time, delta):
        time = datetime.strptime(f"{year}-{month}-{day} {time}:00", "%Y-%m-%d %H:%M:%S") + timedelta(days=delta)
        return time.strftime("%Y%m%dT%H%M%S")
        #将得到的日期格式化，并在现有日期上增加delta日

    def get_str(name, loc, start_time, end_time, delta):
        #ics格式化
        Vevent = 'BEGIN:VEVENT\n'
        #开始event
        Vevent += f"DTSTART;TZID=Asia/Shanghai:{get_time(start_time, delta)}\n"
        Vevent += f"DTEND;TZID=Asia/Shanghai:{get_time(end_time, delta)}\n"
        #开始时间和结束时间
        if opt.watch_mode is True:	
            Vevent += f"SUMMARY:{name}{loc}\n"
        #手表上无法显示地点，因此加在名字后面
        else:
            Vevent += f"SUMMARY:{name}\n"
            Vevent += f"LOCATION:{loc}\n"

        Vevent += 'END:VEVENT\n'
        #结束课程
        return Vevent

    for i in range(len(classes)):
        name = classes[i][:-11]
        if(check(name,deltas[i])):
            continue
        time = classes[i][-11:]
        #时间长度固定为11位，所以分别取最后11位(时间)和其他位置(课程名称)
        #时间格式为 HH:MM - HH:MM, 为课程开始到截止的时间
        time_start, time_end = time.split('-')

        with open(opt.save_path, "a", encoding='utf-8') as f:
            f.write(get_str(name, loc[i], time_start, time_end, deltas[i]))
        #将信息写入.ics文件格式
        #name是课程名称; time是时间; loc是地点

    with open(opt.save_path, "a", encoding='utf-8') as f:
        f.write("END:VCALENDAR\n")

    print("Thanks for using SSAP-autoCalender!")