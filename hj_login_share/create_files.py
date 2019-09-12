#!/usr/bin/env python
# -*- encoding:utf-8 -*-
#Arthor:Timbaland
#date:20180124
import os
import sys, os,time
import configparser,codecs
import pymysql
# import winrm
# 连接mysql数据库参数字段
con = None
ip = '192.168.128.28'
user = 'root'
password = '123456'
dbname = 'gzy'
port = 3306
charset = 'utf8'
db = pymysql.connect(host=ip, user=user, passwd=password, db=dbname, port=port, charset=charset)
cursor = db.cursor()
sn_name = []

# 获取学生学号
query_sno = '''SELECT sid from student_info

'''
try:
    cursor.execute(query_sno)
    result = cursor.fetchall()
    # 获取教室云桌面数量
    sn_count = len(result)

    for id in range(0,sn_count,1):

        sn_name.append(result[id][0])

    # print type(cursor.fetchall()[0])

    db.commit()

except ValueError:
    db.roolback
    print ('error')
# 关闭游标和mysql数据库连接
cursor.close()
db.close()
# # print vm_name
# #crate user files

def mkdir(path):

    # 判断路径是否存在
    # 存在     True
    # 不存在   False

    isExists = os.path.exists(path)

    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path)

        print (path + ' 创建成功')
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print (path + ' 目录已存在')
        return False
def acl_dir(user):
    #切换工作目录D
    os.chdir('%s:\\%s' %(cf.get('set_disk','set_disk'),cf.get('set_class','set_class')))
    # #添加对应目录的权限
    cre_acl_ag = 'cacls %s /e /t /g %s:F' % (user, 'Everyone')
    # cre_acl = 'cacls %s /e /t /g %s:F' %(user,'Domain Users')
    # print(cre_acl)
    print(cre_acl_ag)
    os.popen(cre_acl_ag)
    time.sleep(2)
    # os.popen(cre_acl)
    # #取消对应目录的权限
    # del_acl = 'cacls %s /e /t /c /r users' %(user)
    # os.popen(del_acl)
    #共享对应目录
    share_dir = r'net share %s=%s:\%s' %(user,cf.get('set_disk','set_disk'),user)
    print (share_dir)
    os.popen(share_dir)

if __name__ == '__main__':

    cf = configparser.ConfigParser()
    # cf.readfp(codecs.open('config.ini', "r", "utf-8-sig"))
    cf.read_file(codecs.open('config.ini', "r", "utf-8-sig"))
    #basic dir目录
    bascdir = '%s:\\' %(cf.get('set_disk','set_disk'))


    for f in sn_name:
        # 定义要创建的目录
        mkpath = bascdir + str('%s' %(cf.get('set_class','set_class')))+'\\'+f
        # 调用函数
        mkdir(mkpath)
        acl_dir(f)


