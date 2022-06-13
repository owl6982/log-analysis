from __future__ import print_function
import ctypes, sys

from pyecharts import Bar, Line
from tkinter import INSERT
import os
import chardet
import re

import mmap
import contextlib

from Evtx.Evtx import FileHeader
from Evtx.Views import evtx_file_xml_view



def read_content(text, record_file="result/登录记录.csv"):
    print("正在读取文件...")
    
    content_file = read_output()
    
    with open(content_file , 'rb') as f_code:        
        code = chardet.detect(f_code.readline())['encoding']
        print(code)

    with open(content_file , "r", encoding=code) as f:
        content = f.read().split('\n')
        li_date_time = []
        li_date = []
        li_time = []
        add_time = False
        date_time_format = re.compile(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}")
        for each in content:
            if add_time and "</TimeCreated>" in each:
                li_date_time.append(re.findall(date_time_format, each)[0])
                add_time = False
                continue
            if "</EventID>" in each and "4624" in each: #这里是登录事件id，可以根据需求修改
                add_time = True
            else:
                pass

        for each in li_date_time:
            li_date.append(each.split()[0])
            li_time.append(each.split()[1])
        
        
        add_head = "日期,时间\n"
        create_record(record_file, add_head)
        
        
        print("读取文件完成")
        print("正在筛选记录...")

        add_record(record_file, li_date, li_time)
        
        print("筛选记录完成（登录记录.csv）")
        print("正在生成结果...")

        count_record(record_file)

    with open(r'result\登录结果.csv','r') as f:
        for line in f:
            contact = line.split(',')
            for i in contact:
                    if contact.index(i) == 4:
                        text.insert(INSERT,i+'\n')
                    else:
                        text.insert(INSERT,i+'\t\t')



def read_output():

    os.system("cls")
    try:
        os.mkdir("result")
    except:
        pass
        
    try:
        if read_log():
            print('ok1')
            #C:/windows/system32/winevt/logs/security.evtx
            EvtxPath = "C:/windows/system32/winevt/logs/security.evtx" #日志文件的路径
            with open("result/log_xml.txt", "w") as f_w:
                print("@@@@@@@@@@@@@")
                with open(EvtxPath,'r') as f:
                    with contextlib.closing(mmap.mmap(f.fileno(),0,access=mmap.ACCESS_READ)) as buf:
                        fh = FileHeader(buf,0)
                        for xml, record in evtx_file_xml_view(fh):
                            f_w.write(xml +"\n--------------------\n")
        else:
            print('ok2')
            if sys.version_info[0] == 3:
                ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
                

        
        print("可视化文件生成成功（render.html）")
        print("----------------------------------------------------")
        os.system("pause")

    except Exception as e:
        print("错误：")
        print(repr(e))
        os.system("pause")

    content_file="result/log_xml.txt"
    return content_file
    
    

def read_log():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
        
    except:
        return False
    
def create_record(record_file, head):
    with open(record_file, "w", encoding="gb2312") as f:
        f.write(head)


def add_record(record_file, li_date, li_time):
    with open(record_file, "a", encoding="gb2312") as f:
        li_date_time = tuple(zip(li_date, li_time))
        for each in li_date_time:
          f.write(each[0] + "," + each[1] + "\n")


def count_record(record_file):
    
    with open(record_file, "r", encoding="gb2312") as f:
        f.readline()
        content = f.read().split('\n')
        dates = []
        times = []
        data_record = {}
        date_time = []
        compare_time = []

        for each in content:
            if ',' not in each:
                continue
            date, time = each.split(',')
            time_format = time.split(':')
            time_to_second = int(time_format[0])*3600 + int(time_format[1])*60 + int(time_format[2])
            
            
            if date not in data_record:    
                date_time = [time]
                compare_time = [time_to_second]
                use_time = 0
                data_record[date] = [date_time[0], date_time[0], use_time, 1]

            else:
                date_time.append(time)
                compare_time.append(time_to_second)
                max_time = compare_time.index(max(compare_time))
                min_time = compare_time.index(min(compare_time))
                use_time = compare_time[max_time] - compare_time[min_time]
                use_time_format = str(time_to_format(use_time))

                data_record[date][:3] = [date_time[min_time], date_time[max_time], use_time_format]
                data_record[date][3] += 1

        save_result(data_record)
        print("结果文件生成成功（结果.csv）")
        print("正在生成可视化文件...")
        display_data(data_record)

        
def time_to_format(use_time):
    hour = use_time // 3600
    minute = (use_time - hour*3600) // 60
    second = use_time - hour*3600 - minute*60
    use_time_format = "%d:%d:%d" % (hour, minute, second)
    return use_time_format


def save_result(data_record, save_file="result/登录结果.csv"):
    with open(save_file, "w", encoding="gb2312") as f:
        f.write("登录日期,登录时间,注销时间,使用时间,登录次数\n")
        order = list(data_record.keys())
        order.sort()
        for each in order:
            f.write(each + "," + data_record[each][0] + "," + data_record[each][1] + "," + str(data_record[each][2]) + "," + str(data_record[each][3]) + "\n")


def display_data(data_record):
    bar = Bar("每日登录次数", width=1200, height=800)
    line = Line("每日登录次数", width=1200, height=800)
    li_time = []
    li_count = []
    order = list(data_record.keys())
    order.sort()
    for each in order:
        li_time.append(each)
        li_count.append(data_record[each][-1])
    bar.add("日期", li_time, li_count,is_more_utils=True)
    line.add("日期", li_time, li_count,is_more_utils=True)
    x = bar.print_echarts_options()
    x2 = line.print_echarts_options()
    with open('web/index windows.txt', 'r', encoding='utf-8') as f:
        w = f.read().format(x,x2)
    with open('result/visual_of_auto.html', 'w', encoding='utf-8') as f:
        f.write(w)
    #bar.render("result/visual_of_log.html")

  



