#!/usr/bin/evn python
# -*- encoding:utf-8 -*-
# function: connect exsi server api  for restart vm
# date:2019-09-09
# Arthor:Timbaland
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

_Arthur_ = 'Timbaland'
import pysphere, pymysql
from pysphere import VIServer
import logging
import ssl
import datetime, os, time
import ConfigParser, codecs

# 全局取消证书验证,忽略连接VSPHERE时提示证书验证
ssl._create_default_https_context = ssl._create_unverified_context

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class VcentTools(object):
    def __init__(self, host_ip, user, password,flag):
        self.host_ip = host_ip
        self.user = user
        self.password = password
        self.flag = flag
    # 可以连接esxi主机，也可以连接vcenter

    def _connect(self):

        server_obj = VIServer()

    def esxi_version(self):
        server_obj = VIServer()
        try:
            server_obj.connect(self.host_ip, self.user, self.password)
            servertype, version = server_obj.get_server_type(), server_obj.get_api_version()
            server_obj.disconnect()
            return servertype, version
        except Exception as  e:
            server_obj.disconnect()
            print e

    def vm_status(self, vm_name):

        server_obj = VIServer()
        try:
            server_obj.connect(self.host_ip, self.user, self.password)
            # servertype, version = server_obj.get_server_type(),server_obj.get_api_version()


        except Exception as  e:
            server_obj.disconnect()
            print e

        # 通过名称获取vm的实例
        try:
            vm = server_obj.get_vm_by_name(vm_name)
            if vm.is_powered_off() == False:
                server_obj.disconnect()
                return 1

            if vm.is_powered_off() == True:
                server_obj.disconnect()
                return 2

        except Exception as e:
            server_obj.disconnect()
            return 3

    def vmaction(self, vm_name, vm_hz):

        server_obj = VIServer()
        try:
            server_obj.connect(self.host_ip, self.user, self.password)
        except Exception as  e:
            server_obj.disconnect()
            print e

        # 通过名称获取vm的实例
        try:
            vm = server_obj.get_vm_by_name(vm_name)
        except Exception as e:
            server_obj.disconnect()
            return 0
        if vm.is_powered_off() == False:
            try:
                vm.power_off()
                # print (type(int(vm_hz)))
                for i in range(1, int(vm_hz)):
                    print u'虚拟机%s 正在关机中。。。。\n' % (vm_name)
                    time.sleep(1)
                print u'关机完成'
                server_obj.disconnect()

                return 1
            except Exception as e:
                server_obj.disconnect()
                print e

        if vm.is_powered_off() == True:
            try:
                # vm.power_on()
                print u'虚拟机%s 已经关机' % (vm_name)
                server_obj.disconnect()

            except Exception as e:
                server_obj.disconnect()
                return 2

class Class_VM(object):
    def __init__(self, host, user, pwd, port, db, charset):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.port = port
        self.db = db
        self.charset = charset

    # 获取教室里面的虚拟机信息
    def get_vmname(self, query_sql):
        try:
            # 连接mysql数据库参数字段
            con = None
            db = pymysql.connect(host=self.host, user=self.user, passwd=self.pwd, db=self.db, port=self.port,
                                 charset=self.charset)
            cursor = db.cursor()
            vmlist = []
            cursor.execute(query_sql)
            result = cursor.fetchall()
            # 获取教室云桌面数量
            vm_count = len(result)
            print unicode('教室云桌面虚拟机数量共{0}台'.format(vm_count), 'utf-8')

            # print len(cursor.fetchall())
            # cursor.execute(query_vm)
            for vm_id in range(0, vm_count, 1):
                # print result[vm_id][0]
                # print result[vm_id][1]
                vmlist.append(result[vm_id][0])
                # print result[vm_id][0]

            # print type(cursor.fetchall()[0])

            db.commit()

        except ValueError:
            db.roolback
            print 'error'
        # 关闭游标和mysql数据库连接
        cursor.close()
        db.close()
        return vmlist


if __name__ == '__main__':
    cf = ConfigParser.ConfigParser()
    # cf.read('config.ini',encoding="utf-8")
    cf.readfp(codecs.open('config.ini', "r", "utf-8-sig"))
    # print cf.get('vm_retime','set_retime')
    # print type(cf.get('vc','vc_ip'))
    # 连接vsphere
    # print cf.get('vc','vc_ip'),cf.get('vc','vc_acount'),cf.get('vc','vc_pwd')

    # obj = VcentTools('10.22.14.130', 'administrator@vsphere.local', '1qaz@WSX')
    # print obj.host_ip,obj.password,obj.user,obj.esxi_version()
    # 查询教室虚拟机
    query_vm = '''  SELECT  b.vm_name 
                    from hj_dg a 
                    INNER JOIN hj_vm b on a.id = b.dg_id 
                    WHERE b.vm_type = 1  and del_flag=0
                   '''
    # 查询虚拟机信息
    p = Class_VM(cf.get('hj_db', 'db_host'), cf.get('hj_db', 'db_user'), cf.get('hj_db', 'db_pwd'),
                 cf.getint('hj_db', 'db_port'), cf.get('hj_db', 'db'), 'utf8')
    # print p.get_vmname(query_vm)[0]
    # 获取当前时间
    now_date = datetime.datetime.now().strftime('%H:%M')


    while True:
        obj1 = VcentTools(cf.get('vc1', 'vc_ip'), cf.get('vc1', 'vc_acount'), cf.get('vc1', 'vc_pwd'), flag='obj1')
        obj2 = VcentTools(cf.get('vc2', 'vc_ip'), cf.get('vc2', 'vc_acount'), cf.get('vc2', 'vc_pwd'), flag='obj2')
        obj3 = VcentTools(cf.get('vc3', 'vc_ip'), cf.get('vc3', 'vc_acount'), cf.get('vc3', 'vc_pwd'), flag='obj3')
        obj4 = VcentTools(cf.get('vc4', 'vc_ip'), cf.get('vc4', 'vc_acount'), cf.get('vc4', 'vc_pwd'), flag='obj4')
        obj5 = VcentTools(cf.get('vc5', 'vc_ip'), cf.get('vc5', 'vc_acount'), cf.get('vc5', 'vc_pwd'), flag='obj5')
        obj6 = VcentTools(cf.get('vc6', 'vc_ip'), cf.get('vc6', 'vc_acount'), cf.get('vc6', 'vc_pwd'), flag='obj6')
        obj7 = VcentTools(cf.get('vc7', 'vc_ip'), cf.get('vc7', 'vc_acount'), cf.get('vc7', 'vc_pwd'), flag='obj7')
        obj8 = VcentTools(cf.get('vc8', 'vc_ip'), cf.get('vc8', 'vc_acount'), cf.get('vc8', 'vc_pwd'), flag='obj8')
        obj9 = VcentTools(cf.get('vc9', 'vc_ip'), cf.get('vc9', 'vc_acount'), cf.get('vc9', 'vc_pwd'), flag='obj9')
        obj10 = VcentTools(cf.get('vc10', 'vc_ip'), cf.get('vc10', 'vc_acount'), cf.get('vc10', 'vc_pwd'), flag='obj10')
        obj11 = VcentTools(cf.get('vc11', 'vc_ip'), cf.get('vc11', 'vc_acount'), cf.get('vc11', 'vc_pwd'), flag='obj11')
        obj12 = VcentTools(cf.get('vc12', 'vc_ip'), cf.get('vc12', 'vc_acount'), cf.get('vc12', 'vc_pwd'), flag='obj12')
        if datetime.datetime.now().strftime('%H:%M') == cf.get('vm_retime', 'set_retime'):
            for vmname in p.get_vmname(query_vm):
                if obj1.vmaction(vmname, cf.get('vm_hz', 'vm_hz')) == 0:
                    print 'is not exsit %s' % (cf.get('vc1', 'vc_ip'))
                if obj2.vmaction(vmname, cf.get('vm_hz', 'vm_hz')) == 0:
                    print 'is not exsit %s' % (cf.get('vc2', 'vc_ip'))
                if obj3.vmaction(vmname, cf.get('vm_hz', 'vm_hz')) == 0:
                    print 'is not exsit %s' % (cf.get('vc3', 'vc_ip'))
                if obj4.vmaction(vmname, cf.get('vm_hz', 'vm_hz')) == 0:
                    print 'is not exsit %s' % (cf.get('vc4', 'vc_ip'))
                if obj5.vmaction(vmname, cf.get('vm_hz', 'vm_hz')) == 0:
                    print 'is not exsit %s' % (cf.get('vc5', 'vc_ip'))
                if obj6.vmaction(vmname, cf.get('vm_hz', 'vm_hz')) == 0:
                    print 'is not exsit %s' % (cf.get('vc6', 'vc_ip'))
                if obj7.vmaction(vmname, cf.get('vm_hz', 'vm_hz')) == 0:
                    print 'is not exsit %s' % (cf.get('vc7', 'vc_ip'))
                if obj8.vmaction(vmname, cf.get('vm_hz', 'vm_hz')) == 0:
                    print 'is not exsit %s' % (cf.get('vc8', 'vc_ip'))
                if obj9.vmaction(vmname, cf.get('vm_hz', 'vm_hz')) == 0:
                    print 'is not exsit %s' % (cf.get('vc9', 'vc_ip'))
                if obj10.vmaction(vmname, cf.get('vm_hz', 'vm_hz')) == 0:
                    print 'is not exsit %s' % (cf.get('vc10', 'vc_ip'))
                if obj11.vmaction(vmname, cf.get('vm_hz', 'vm_hz')) == 0:
                    print 'is not exsit %s' % (cf.get('vc11', 'vc_ip'))
                if obj12.vmaction(vmname, cf.get('vm_hz', 'vm_hz')) == 0:
                    print 'is not exsit %s' % (cf.get('vc12', 'vc_ip'))
                logger.info(u'正在关机%s' % (vmname))
                # time.sleep(10)
        nowdate = datetime.datetime.now().strftime
        logger.info(u'现在时间%s,还未到关机时间%s' % (now_date, cf.get('vm_retime', 'set_retime')))

        time.sleep(1)
