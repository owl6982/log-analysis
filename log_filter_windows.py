from pyecharts import Bar, Line
from tkinter import INSERT
import os
import chardet
import re
import time

#默认读取文件名为登录日志，可以根据需求修改
def read_content(text, content_file, record_file="result/登录记录.csv"):
    print("正在读取文件...")
    with open(content_file , "rb") as f_code:        
        code = chardet.detect(f_code.readline())['encoding']
        print(code)
    with open(content_file , "r", encoding=code) as f:        
        head = f.readline().replace('\n', '').split(',')
        
        for each in head:
            if each == '级别':
                row_user = head.index(each)
            elif each == '日期和时间':
                row_date_time = head.index(each)
            elif each == '来源':
                row_source = head.index(each)
            elif each == '事件 ID':
                row_event = head.index(each)
            elif each == '任务类别':
                row_classify = head.index(each)
                
        add_head = "日期,时间\n"
        create_record(record_file, add_head)
        
        content = f.read().split('\n')
        content_list = []
        for each in content:
            if 1:
                content_list.append(each)
            else:
                continue
        print("读取文件完成")
        print("正在筛选记录...")

        for each in content_list:
            if each == '':
                continue
            else:
                row = each.split(',')
                if len(row) < 3:
                    continue
                elif row[row_event] == '4624':
                    row_date, row_time = row[row_date_time].split(' ')
                    add_content = row_date + "," + row_time# + "," + row[6]
                    add_record(record_file, add_content)
        
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
                    
def create_record(record_file, head):
    with open(record_file, "w", encoding="gb2312") as f:
        f.write(head)


def add_record(record_file, row):
    with open(record_file, "a", encoding="gb2312") as f:
        f.write(row + "\n")
        


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
            date_all = date.split('/')
            date_days = int(date_all[0])*365 + int(date_all[1])*30 + int(date_all[2])
            
            if date_days not in data_record:    
                date_time = [time]
                compare_time = [time_to_second]
                use_time = 0
                data_record[date_days] = [date, date_time[0], date_time[0], use_time, 1]
    

            else:
                date_time.append(time)
                compare_time.append(time_to_second)
                max_time = compare_time.index(max(compare_time))
                min_time = compare_time.index(min(compare_time))
                use_time = compare_time[max_time] - compare_time[min_time]
                use_time_format = str(time_to_format(use_time))

                data_record[date_days][1:4] = [date_time[min_time], date_time[max_time], use_time_format]
                data_record[date_days][-1] += 1

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
            f.write(data_record[each][0] + "," + data_record[each][1] + "," + str(data_record[each][2]) + "," + str(data_record[each][3]) + "," + str(data_record[each][4]) + "\n")


def display_data(data_record):
    bar = Bar("每日登录次数", width=1200, height=800)
    line = Line("每日登录次数", width=1200, height=800)
    li_time = []
    li_count = []
    order = list(data_record.keys())
    order.sort()
    for each in order:
        li_time.append(data_record[each][0])
        li_count.append(data_record[each][-1])
    bar.add("日期", li_time, li_count,is_more_utils=True)
    line.add("日期", li_time, li_count,is_more_utils=True)
    # bar.show_config()
    y = bar.print_echarts_options()
    y2 = line.print_echarts_options()
    with open('web/index windows.txt', 'r', encoding='utf-8') as f:
        z = f.read().format(y,y2)

    with open('result/visual_of_log.html' ,'w', encoding='utf-8') as f:
        f.write(z)
    #bar.render("result/visual_of_log.html")


if __name__ == '__main__':
    os.system("cls")
    try:
        os.mkdir("result")
    except:
        pass
    #while True:
    try:
        #file_name = input("请输入日志文件名（不输入路径，默认为当前路径，默认文件名为：登录日志.csv）：")
        #os.system("cls")
        file_name = ''
        if file_name != '':
            try:
                read_content(file_name)
                print("可视化文件生成成功（render.html）")
                print("----------------------------------------------------")
            except:
                print("文件不存在")
               #continue
        else:
            read_content()
            print("文件生成成功")
            print("可视化文件生成成功（render.html）")
            print("----------------------------------------------------")
    except Exception as e:
        print("错误：")
        print(repr(e))
       # continue
