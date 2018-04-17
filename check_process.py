# -*- coding: utf-8 -*-
"""
Created on Wed Apr 11 22:10:38 2018

@author: chaoqun chen
"""

import os
import time
def CheckPro(process_name):
    try:
        process = len(os.popen("ps -C %s|wc -l"%process_name).readlines())
        print(process)
        if process >= 2:
            return True
        elif process < 3 and process_name == "redis-server":
            print()
            return False
    except:
        print("Check process ERROR!!!")
        return False
        

def startProcess(process_script):
    try:
        result_code = os.system(process_script)
        if result_code == 0:
            print("run program successfully.")
            #成功执行过一次后 可休息1小时
            time.sleep(3600)
        else:
            print('run program failed, exit code: %d'%result_code)
    except:
        print("exit status = [%d]"%result_code)

if __name__ == '__main__':
    #所有需要检测的程序名称
    proArr = ["xb_col","xb_tp","xb_to_gjpt","xb_sql","xb_task","xb_cli_cqzf","xb_server_kh","xb_heart","xb_to_nj","xb_cfpp",\
              "httpd","redis-server","mysqld"] 
    while True:
        #记录异常程序名称
        errPro = []
        ret = True
        for pro in proArr:
            if CheckPro(pro)!=True:
                errPro.append(pro)
                ret = False
        if ret != True:
            errstring = ','.join(proArr)
            print(str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + ' %s 异常\n'%errstring)
            #字符串长度需要小于20 若超过20则把字符串第17-19个字符改成...
            if len(errstring)>=20:
                errstring = errstring[0:17]+'...'
            #SendMsg为需要运行的程序 需要一个字符串参数(errPro )  
            cmd = "./SendMsg " + errstring
            #运行指定程序
            startProcess(cmd)
            #每分钟检测一次
        time.sleep(60)