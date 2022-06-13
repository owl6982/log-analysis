from pyecharts import Bar, Line
from tkinter import INSERT
import os
import chardet
import re
import time


def read_content(content_file,text):
	li = []
	li_result = []
	log_date_times = []
	log_ips = []
	log_ports = []
	log_dates = []
	log_times = []
	log_users = []
	log_sshds = []

	print("reading the file: %s ..." % content_file)
	try:
		with open(content_file , "rb") as f_code:	   
			code = chardet.detect(f_code.readline())['encoding']
			print(code)
		with open(content_file, "r", encoding=code) as f:
			li_month = (('Jan ', '01-'), ('Feb ', '02-'), ('Mar ', '03-'), ('Apr ', '04-'), ('May ', '05-'), ('Jun ', '06-'), ('Jul ', '07-'), ('Aug ', '08-'), ('Sep ', '09-'), ('Oct ', '10-'), ('Nov ', '11-'), ('Dec ', '12-'))
			content = f.read()
			for each in li_month:
				content = content.replace(each[0], each[1])
				#这里要把月份全部替换了

			li = content.split('\n')
			li_close = []
			close_port_format = re.compile('\[(.*?)\]')
			close_time_format = re.compile("\d\d:\d\d:\d\d")

			for each in li:
				if "Accepted" in each:
					li_result.append(each)
				if "session closed" in each and "sshd" in each:
					close_port = re.findall(close_port_format, each)[0]
					close_user = each.split()[-1]
					close_time = re.findall(close_time_format, each)[0]
					li_close.append((close_port, close_user, close_time))

			date_times_format = re.compile(".+:\d\d")
			ips_format = re.compile("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}")
			ports_format = re.compile("port (\d{1,})")
			users_format = re.compile("for (.*?) from")
			sshds_format = re.compile('\[(.*?)\]')
			for each in li_result:
				log_date_times.append(re.findall(date_times_format, each)[0])
				log_ips.append(re.findall(ips_format, each)[0])
				log_ports.append(re.findall(ports_format, each)[0])
				log_users.append(re.findall(users_format, each)[0])
				log_sshds.append(re.findall(sshds_format, each)[0])

			for each in log_date_times:
				log_dates.append(each[:-9])
				log_times.append(each[-8:])

	
	except Exception as e:
		print(repr(e))
		print("read file wrong!")
		return

	print("read the file: %s complete" % content_file)

	print("creating the file: %s ..." % str("log_record_centos.csv"))
	with open(r"result/log_record_centos.csv", "w", encoding="utf-8") as f:
		head = "date,connect time,close time,use time,user,ip,port\n"
		f.write(head)
		for i in range(len(log_ips)):
			try:
				log_out_time = "00:00:00"
				for j in li_close:
					if j[0] == log_sshds[i]:
						log_out_time = li_close.pop(li_close.index(j))[2]
						break
				
				log_time_i_format = log_times[i].split(':')
				close_time_i_format = log_out_time.split(':')
				log_time_to_second = int(log_time_i_format[0])*3600 + int(log_time_i_format[1])*60 + int(log_time_i_format[2])
				close_time_to_second = int(close_time_i_format[0])*3600 + int(close_time_i_format[1])*60 + int(close_time_i_format[2])
				if log_out_time == "00:00:00":
					use_time_to_second = 0
				elif close_time_to_second < log_time_to_second:
					use_time_to_second = 24*3600 - log_time_to_second + close_time_to_second
				else:
					use_time_to_second = close_time_to_second - log_time_to_second

				use_time = time_to_format(use_time_to_second)
				contents = "%s,%s,%s,%s,%s,%s,%s\n" % (log_dates[i], log_times[i], log_out_time, use_time, log_users[i], log_ips[i], log_ports[i])

			except Exception as e:
				contents = "%s,%s,-1,-1,%s,%s,%s\n" % (log_dates[i], log_times[i], log_users[i], log_ips[i], log_ports[i])
			finally:
				f.write(contents)

	print("create the file: %s complete" % str("log_record_centos.csv"))

	print("reading the file: %s ..." % str("log_result_centos.csv"))
	with open(r"result/log_record_centos.csv", "r", encoding="utf-8") as f:
		f.readline()
		li_contents = f.read().split("\n")
		di_contents = {}
		for each in li_contents:
			datas = each.split(',')
			if datas[0] == "":
				pass
			elif datas[0] not in di_contents:
				di_contents[datas[0]] = [datas[1], datas[2], datas[3]] + [1]
			elif datas[0] in di_contents:
				di_contents[datas[0]][1] = datas[2]
				di_contents[datas[0]][-1] += 1
				log_time_i_format = di_contents[datas[0]][2].split(':')
				close_time_i_format = datas[3].split(':')
				log_time_to_second = int(log_time_i_format[0])*3600 + int(log_time_i_format[1])*60 + int(log_time_i_format[2])
				close_time_to_second = int(close_time_i_format[0])*3600 + int(close_time_i_format[1])*60 + int(close_time_i_format[2])
				use_time_to_second = close_time_to_second + log_time_to_second
				use_time = time_to_format(use_time_to_second)
				di_contents[datas[0]][2] = use_time

	with open(r"result/log_result_centos.csv", "w", encoding="utf-8") as f:
			head = "date,log time,logout time,day use time, logon times\n"
			f.write(head)
			li_keys = list(di_contents.keys())
			li_keys.sort()
			li_logon_times = []
			for each in li_keys:
				contents = "%s,%s,%s,%s,%d\n" % (each, di_contents[each][0],di_contents[each][1],di_contents[each][2],di_contents[each][-1])
				f.write(contents)
				li_logon_times.append(di_contents[each][-1])

	print("read the file: %s complete" % str("log_result_centos.csv"))

	print("creating the visual file: %s ..." % str("visual_of_centos.html"))
	bar = Bar("每日登录次数", width=1200, height=800)
	line = Line("每日登录次数", width=1200, height=800)
	bar.add("date", li_keys, li_logon_times,is_more_utils=True)
	line.add("date", li_keys, li_logon_times,is_more_utils=True)
	# bar.show_config()
	y = bar.print_echarts_options()
	y2 = line.print_echarts_options()
	with open('web/index centos.txt', 'r', encoding='utf-8') as f:
		z = f.read().format(y,y2)

	with open('result/visual_of_centos.html', 'w', encoding='utf-8') as f:
		f.write(z)

	#print("create the visual file: %s complete" % str("visual_of_centos.html"))
	#bar.render("result/visual_of_centos.html")


	with open(r'C:\Users\kirido\Desktop\手动导出\result\log_record_centos.csv','r',encoding='utf-8') as f:
		for line in f:
			content = line.split(',')
			for i in content:
				if content.index(i) == 6:
					text.insert(INSERT,i+'\n')
				else:
					text.insert(INSERT,i+'\t\t')



def time_to_format(use_time):
	hour = use_time // 3600
	minute = (use_time - hour*3600) // 60
	second = use_time - hour*3600 - minute*60
	use_time_format = "%d:%d:%d" % (hour, minute, second)
	return use_time_format


if __name__ == '__main__':
	try:
		os.mkdir("result")
	except:
		pass
	
