# -*- coding: utf-8 -*-
from threading import Thread  
import subprocess 
import re 
from queue import Queue    
import time
import pandas as pd
path = r'C:\Users\chaoqun chen\Desktop\ip.txt'#文件存放路径，每一行都是一个ip地址
strlist = [] #以列表保存的所有的ip
with open(path,'r') as file:
    for i in file.readlines():
        strlist.append(i.strip())

# 获取链路状态
def getLinkState(ip):
    #运行ping程序
    p = subprocess.Popen(["ping.exe", ip], 
            stdin = subprocess.PIPE, 
            stdout = subprocess.PIPE, 
            stderr = subprocess.PIPE, 
            shell = True)  

    #得到ping的结果
    out = str(p.stdout.read())
    #print(out)

    #找出丢包率，这里通过‘%’匹配
    regex = re.compile(u'\w*%\w*')
    packetLossRateList = regex.findall(out)
    packetLossRate = packetLossRateList[0]

    #找出往返时间，这里通过‘ms’匹配
    regex = re.compile(u'\w*ms')
    timeList = regex.findall(out)
    minTime = timeList[-3]
    maxTime = timeList[-2]
    averageTime = timeList[-1]
    result = {'packetLossRate':packetLossRate,'minTime':minTime,'maxTime':maxTime,'averageTime':averageTime}
    return result

packetLossRate=[]
minTime = []
averageTime =[]
maxTime = []
ips = []
num_threads=250 #开启250个进程
start_time = time.time()


q=Queue()#建立一个队列
def pingme(i,queue):#i是进程号，quene是ip队列
    while True:  
        ip=queue.get()  
        print('Thread %s pinging %s' %(i,ip))
        try:
            result = getLinkState(ip)
            packetLossRate.append(result.get('packetLossRate'))
            minTime.append(result.get('minTime'))
            averageTime.append(result.get('averageTime'))
            maxTime.append(result.get('maxTime'))
            ips.append(ip.strip())
            print(result)
        except IndexError:#表示ping失败，无法解析到速度
            print(ip +' failed')
            packetLossRate.append('100%')
            minTime.append('9999')
            averageTime.append('9999')
            maxTime.append('9999')
            ips.append(ip.strip()) 
        queue.task_done()  

#start num_threads threads  
for i in range(num_threads):  
    t=Thread(target=pingme,args=(i,q))  
    t.setDaemon(True)  
    t.start()  

for ip in strlist:  
    q.put(ip)  #把所有的ip都保存到队列中 
print('main thread waiting...')   
q.join();
end_time=time.time()
print('程序总共运行时间：%s'%(end_time-start_time))

result=pd.DataFrame({'ip':ip,'packetLossRate': packetLossRate, 'maxTime': maxTime, 'minTime':minTime, 'averageTime': averageTime}).sort_values(by='averageTime')

print(result.head(5))
#保存结果文件
result.to_csv(r'C:\Users\chaoqun chen\Desktop\ping_result.csv',encoding='utf-8')