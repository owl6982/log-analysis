from tkinter import *
import os
from tkinter import filedialog
import tkinter.messagebox
import openpyxl
from pyecharts import Bar
from PIL import ImageTk, Image

root = Tk()
root.title("适用于多种操作系统的访问日志分析统计软件")

group = LabelFrame(root, text='请选择系统',padx=5,pady=5)
group.grid(row=1,column=0,columnspan=2, padx=10,pady=10, sticky=E+W)

v = IntVar()
global syss
syss=0
def r1():
    #print('call r1')
    global syss
    syss=1
def r2():
    #print('call r2')
    global syss
    syss=2
def r3():
    #print('call r3')
    global syss
    syss=3
def r4():
    #print('call r4')
    global syss
    syss=4
def r5():
    #print('call r5')
    global syss
    syss=5

SYSTEMS = [
    ('Centos',1,r1),
    ('Ubuntu',2,r2),
    ('window2003',3,r3),
    ('window',4,r4),
    ('自动导出并分析',5,r5)]

for sys,num,r in SYSTEMS:
    Radiobutton(group, text=sys,variable=v, value=num,command = r).grid(sticky=W)
   

def renovate():
    e1.delete(0, END)
    text.delete(1.0, END)
    

def callback():
    
    e1.delete(0, END)
    fileName=StringVar()
    fileName= filedialog.askopenfilename(defaultextension=".py")
                                         #filetypes = [("CSV",".csv"),
                                                                               #("JPG",".jpg"),
                                                                               #("Python", ".py")]
    e1.insert('insert' ,fileName)
    return fileName

def callbackhtml():
    
    fileName1 = StringVar()
    fileName1 = filedialog.askopenfilename(filetypes = [("HTML",".html")])
                                                                               #("JPG",".jpg"),
                                                                               #("Python", ".py")]
    
    os.system('%s' % fileName1)
        
def callbackcsv():

    fileName2=StringVar()
    fileName2= filedialog.askopenfilename(filetypes = [("CSV",".csv")])
                                                                               #("JPG",".jpg"),
                                                                               #("Python", ".py")]
    
    with open(r'%s' % fileName2 ,'r') as f:
        for line in f:
            content = line.split(',')
            for i in content:
                if content.index(i) == 4:
                    text.insert(INSERT,i+'\n')
                else:
                    text.insert(INSERT,i+'\t\t')

                    
class APP:
    def __init__(self,master,e1,text):
        
        frame = Frame(master)
        frame.grid(row=2,column=0,columnspan=2,sticky=N+S)
        self.text = text
        self.mater=master
        self.hi_there = Button(frame,text="分             析",bg='black', fg="green",command=self.click1, padx=200)
        #设置调整尺寸和显示位置，如果括号里没东西就按默认来
        self.hi_there.grid(row=2,column=0, columnspan=2)    #这里就默认位置了
        self.e1 = e1

    def click1(self):
        text.delete(1.0, END)
        if syss==1:
            #print(1)
            if self.e1.get() == '':
                return tkinter.messagebox.showinfo('提示','请指定操作系统日志文件位置')
                #判断是否为空，为空返回提示框
            else:
                import log_filter_centos
                log_filter_centos.read_content(content_file=self.e1.get(),text=self.text)
                os.chdir("result")
                #text.config(yscrollcommand=scroll.set)
                os.system("visual_of_centos.html")
                os.chdir("..")
        elif syss==2:
            #print(1)
            if self.e1.get() == '':
                return tkinter.messagebox.showinfo('提示','请指定操作系统日志文件位置')
                #判断是否为空，为空返回提示框
            else:
                import log_filter_ubuntu
                log_filter_ubuntu.read_content(content_file=self.e1.get(),text=self.text)
                os.chdir("result")
                os.system("visual_of_ubuntu.html")
                os.chdir("..")

        elif syss==3:
            if self.e1.get() == '':
                return tkinter.messagebox.showinfo('提示','请指定操作系统日志文件位置')
                #判断是否为空，为空返回提示框
            else:
                import log_filter_2003
                log_filter_2003.read_content(content_file=self.e1.get(),text=self.text)
                os.chdir("result")
                os.system("visual_of_log2003.html")
                #self.hi_there.command=self.doone2
                os.chdir("..")
        elif syss==4:
            if self.e1.get() == '':
                return tkinter.messagebox.showinfo('提示','请指定操作系统日志文件位置')
                #判断是否为空，为空返回提示框
            else:
                import log_filter_windows
                log_filter_windows.read_content(content_file=self.e1.get(),text=self.text)
                os.chdir("result")
                os.system("visual_of_log.html")
                os.chdir("..")
        elif syss==5:
            import log_filter_windows_auto
            log_filter_windows_auto.read_content(text=self.text)
            os.chdir("result")
            os.system("visual_of_auto.html")
            os.chdir("..")
            #切换会上一级路径
        else:
            tkinter.messagebox.showinfo('提示','请选择操作系统')




menubar = Menu(root)
openVar=IntVar()
saveVar=IntVar()
quitVar=IntVar()

filemenu = Menu(menubar, tearoff=False)
filemenu.add_command(label="重置", command=renovate)

filemenu.add_separator()
filemenu.add_command(label="退出", command=root.quit)
menubar.add_cascade(label="文件", menu=filemenu)

editVar=IntVar()

editmenu = Menu(menubar, tearoff=False)
editmenu.add_command(label="打开历史网页", command=callbackhtml)
editmenu.add_command(label="打开历史csv", command=callbackcsv)

menubar.add_cascade(label="编辑", menu=editmenu)

v1 = StringVar()
e1 = Entry(root, textvariable=v1, width=65)
e1.grid(row=0, column=0, sticky=E+W,ipadx=100)


Button(root, text="请选择系统日志" , command=callback).grid(row=0, column=1)

scroll = tkinter.Scrollbar()
scroll.grid(row=3, column=0)

text = Text(root, width=107, height=20)
text.grid(row=3, column=0, columnspan=2)


app = APP(root,e1,text)


root.config(menu=menubar)


mainloop()
