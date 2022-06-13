from pyecharts import Bar, Line
from tkinter import INSERT
import os
import chardet
import re
import time

#登录日志是读取的文件名，可以修改
def read_content(content_file, text , record_file="result/登录记录2003.csv" ):
    print("正在读取文件...")
    with open(content_file , "rb") as f_code:        
        code = chardet.detect(f_code.readline())['encoding']
        print(code)
    with open(content_file , "r", encoding=code) as f:        
        head = f.readline().replace('\n', '').split(',')
        
        for each in head:
            if each == '日期':
                row_date = head.index(each)
            elif each == '时间':
                row_time = head.index(each)
            elif each == '事件':
                row_event = head.index(each)
            elif each == '用户':
                row_user = head.index(each)
        add_head = head[row_date] + "," + head[row_time] + "\n"
        
        (record_file, add_head)
        
        content = f.read().split('\n')
        
        print("读取文件完成")
        print("正在筛选记录...")
        for each in content:
            if content == ' ':
                break
            else:
                row = each.split(',')
                if len(row) < 3:
                    continue
                elif row[row_event] == '680' and row[row_user] == 'Administrator':
                    #测试电脑的远程事件时680，用户为Administrator，可以根据需求修改
                    add_content = row[row_date] + "," + row[row_time]
                    add_record(record_file, add_content)
        
        print("筛选记录完成（登录记录2003.csv）")
        print("正在生成结果...")
        count_record(record_file)

    with open(r'result\登录结果2003.csv','r') as f:
        for line in f:
            content = line.split(',')
            for i in content:
                if content.index(i) == 4:
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
        print("结果文件生成成功（登录结果2003.csv）")
        print("正在生成可视化文件...")
        display_data(data_record)

                
def time_to_format(use_time):
    hour = use_time // 3600
    minute = (use_time - hour*3600) // 60
    second = use_time - hour*3600 - minute*60
    use_time_format = "%d:%d:%d" % (hour, minute, second)
    return use_time_format


def save_result(data_record, save_file="result/登录结果2003.csv"):
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
    # bar.show_config()
    y = bar.print_echarts_options()
    y2 = line.print_echarts_options()
    with open('web/index winows2003.txt', 'r', encoding='utf-8') as f:
        z = f.read().format(y,y2)
    with open('result/visual_of_log2003.html', 'w', encoding='utf-8') as f:
        f.write(z)
    #print("create the visual file: %s complete" % str("visual_of_log.html"))
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
        os.system("cls")
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
        print(e)
        #continue
