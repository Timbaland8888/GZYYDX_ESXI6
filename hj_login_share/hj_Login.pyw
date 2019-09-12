# -*- encoding:utf-8 -*-
#!/bin/user/python

from tkinter import *
from tkinter.messagebox import *
import pymysql
import os


# from mstsc_rdp import Authentication

class LoginPage(Frame):
    def __init__(self):
        Frame.__init__(self)
        self.username = StringVar()
        self.password = StringVar()
        self.pack()
        self.createForm()

    def createForm(self):
        Label(self, bg='#B9D3EE', fg='red').grid(row=0, stick=W, pady=10)
        Label(self, bg='#B9D3EE', text='学号: ').grid(row=1, stick=W, pady=10)
        Entry(self, textvariable=self.username).grid(row=1, column=1, stick=E)
        Label(self, bg='#B9D3EE', text='密码: ').grid(row=2, stick=W, pady=10)
        Entry(self, textvariable=self.password, show='*').grid(row=2, column=1, stick=E)
        Button(self, bg='#B03060', text='登陆', command=self.loginCheck).grid(row=3, stick=W, pady=10)
        Button(self, bg='#B03060', text='退出', command=self.quit).grid(row=3, column=1, stick=E)

    def loginCheck(self):
        sid = self.username.get()
        secret = self.password.get()
        sql = """ select * from student_info where sid ='%s' and pwd ='%s' """ % (sid, secret)
        try:
            con = pymysql.connect('192.168.128.28', 'root', '123456', 'gzy')
            cursor = con.cursor()
            cursor.execute(sql)
            result = cursor.fetchall()
            # print(result)
            # print(len(result))

        except:
            print('请检查数据库服务器网络')
        finally:

            if len(result) != 0:
                host = '192.168.128.28'
                sharedir = result[0][0]
                sname = str(result[0][1])
                print type
                # netuse = r"""net use u: \\192.168.128.28\%s  "123" /user:"gzucm\%s""" % (sharedir, sharedir)
                netuse = r"""net use u: \\192.168.128.28\%s  """ % ( sharedir)
                #修改挂载盘名称
                renetdisk = """  """
                #入域用户
                # netuse = r"""net use u: \\GZYHJLIC\%s  """ % (sharedir)
                # print(netuse)
                # print("login success")
                # do_to = Authentication()
                # do_to.cmdkey_pc(host)

                cmd = r"start u: "

                os.system(netuse)
                os.system(r'wscript .\rename.vbs %s\%s' %(sharedir,sname))
                os.system(cmd)

                # print(cmd)
                self.destroy()
                # secret.MainPage()
                # do_to.conect_pc(host)
                self.quit()
            else:
                showinfo(title='错误', message='学号或密码错误！')
                # print('账号或密码错误！')


if __name__ == '__main__':

    delnetuse = "net use u: /del /y"
    os.system(delnetuse)
    root = Tk()
    root.title('作业')
    root.iconbitmap('1.ico')
    # root.iconphoto('1.ico')

    width = 320
    height = 240
    Label(root, bg='#B9D3EE', text="汇 捷       版本：V1.0", fg='#27408B').pack(side="bottom")
    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()
    alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
    root.geometry(alignstr)  # 居中对齐
    root['background'] = '#B9D3EE'
    page1 = LoginPage()
    page1['background'] = '#B9D3EE'
    root.mainloop()
