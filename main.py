import datetime
import time
import requests
import re
import os

proxies = {"http": None, "https": None}  # 取消系统代理
url = 'http://englishservice.siboenglish.com//MobService/index'  # okhttp

#用户信息
userID = ''
classID = ''
EssayList = {}

def login(username, password):
    global userID
    # 发送Post数据请求
    data = {'jyh': '4002_01',
            'parm': '{"schoolID":"603eca2bf34d42a7a9620bd5b7de1453","loginName":"' + username + '","password":"' + password + '","ts":2,"appVersion":"2.0.8"}',
            'sign': '', 'ts': ''}
    ret = requests.post(url=url, data=data, proxies=proxies).text

    # 返回结果处理
    ret = ret.replace('\\r\\n', '').replace('\\', '')
    # print(ret)
    try:
        reg = 'Msg": "(.*)",  "Dat'
        msg = re.search(reg, ret).group(1)

        if msg == '登录成功':
            reg = '"UserName": "(.*)",    "User'
            name = re.search(reg, ret).group(1)

            reg = '0,    "ID": "(.*)",    "Updat'
            userID = re.search(reg, ret).group(1)

            print('登录成功：' + name)
            return True
        else:
            print(msg)
            return False
            # print(msg)
            # print(name)
            # print(userId)
    except:
        print('链接服务器失败')
        return False

def queryJob():
    # 发送Post数据请求
    data = {'jyh': '2022',
            'parm': '{"studentID":"a6f9201fcfb1477b81d8d28d23ad0b05"}',
            'sign': '',
            'ts': ''}
    ret = requests.post(url=url, data=data, proxies=proxies).text

    # 处理返回数据
    ret = ret.replace('\\r\\n', '').replace('\\', '')
    reg = 'Msg": "(.*)",  "Data":'
    job = re.search(reg, ret).group(1)
    print(job)
def getClassInformation(userID):
    global classID
    # 发送Post数据请求
    data = {'jyh':'1001',
            'parm':'{"userID":"' + userID + '","ts":2}',
            'sign':'',
            'ts':''}
    ret = requests.post(url=url, data=data, proxies=proxies).text

    #返回数据处理
    ret = ret.replace('\\r\\n', '').replace('\\', '')
    reg = 'ClassID": "(.*)",      "ClassBH":'
    classID = re.search(reg, ret).group(1)

def getEssayList(keyword, pageStart, userID, classID):
    global EssayList
    EssayList.clear()
    #发送Post数据请求
    data = {'jyh':'2002',
            'parm':'{"keyWord":"' + keyword + '","eassyType":"","grade":0,"orderType":1,"pageStart":' + pageStart + ',"pageSize":10,"ts":2,"userID":"' + userID + '","classID":"' + classID + '"}',
            'sign':'',
            'ts':''}
    ret = requests.post(url=url, data=data, proxies=proxies).text

    # 返回数据处理
    ret = ret.replace('\\r\\n', '').replace('\\', '')
    reg1 = '([0-9a-fA-F]{32})'
    reg2 = '"Title": "(.*?)",      "CreateTime"'
    IDList = re.findall(reg1, ret)
    TitleList = re.findall(reg2, ret)

    for i in range(10):
        EssayList[TitleList[i]] = IDList[i]
        print(str(i + 1) + '：' + TitleList[i] + '(' + IDList[i] + ')')
def TouchEassy(EssayID):
    # 发送Post数据请求
    data = {'jyh':'2003',
            'parm':'{"essayID":"' + EssayID + '","userID":"' + userID + '","classID":"' + classID + '"}',
            'sign':'',
            'ts':''}
    ret = requests.post(url=url, data=data, proxies=proxies).text

    # 返回数据处理
    ret = ret.replace('\\r\\n', '').replace('\\', '')
    reg = 'ExerciseState": (.*),      "EssayID'
    Status = re.search(reg, ret).group(1)
    if(Status == '1'):
        print('进入文章，此文章已做完。')
        return True
    else:
        print('进入文章，该文章待完成。')
        return False

def DoJob(EssayID):
    # 发送Post数据请求
    data = {'jyh': '2023',
            'parm': '{"essayID":"' + EssayID + '"}',
            'sign': '',
            'ts': ''}
    ret = requests.post(url=url, data=data, proxies=proxies).text

    # 返回数据处理
    ret = ret.replace('\\r\\n', '').replace('\\', '')
    reg1 = 'TestItemNumber": (.*?),      "TestItemType'
    reg2 = 'Answer": "(.*?)",'
    Number = re.findall(reg1, ret)
    Answer = re.findall(reg2, ret)

    ans = ''
    for i in range(len(Number)):
        if(i == len(Answer) - 1):
            ans += Number[i] + '-' + Answer[i]
        else:
            ans += Number[i] + '-' + Answer[i] + ';'
    print('答案：' + ans)
    SubmitAnswer(EssayID, ans)
def SubmitAnswer(EssayID, ans):
    # 发送Post数据请求
    data = {'jyh': '2010',
            'parm': '{"essayID":"' + EssayID + '","userID":"' + userID + '","classID":"' + classID + '","createTime":"' + time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime()) + '","itemResult":"' + ans + '"}',
            'sign': '',
            'ts': ''}
    ret = requests.post(url=url, data=data, proxies=proxies).text

    # 返回数据处理
    ret = ret.replace('\\r\\n', '').replace('\\', '')
    reg = '"Msg": "(.*)",  "Data"'
    Status = re.search(reg, ret).group(1)
    print(Status)
def QueryResult(EssayID):
    # 发送Post数据请求
    data = {'jyh': '2011',
            'parm': '{"essayID":"' + EssayID + '","userID":"' + userID + '","classID":"' + classID + '"}',
            'sign': '',
            'ts': ''}
    ret = requests.post(url=url, data=data, proxies=proxies).text
    ret = ret.replace('\\r\\n', '').replace('\\', '')
    reg = 'wordsNum": (.*?)  },  "Num'
    wordsNum = re.search(reg, ret).group(1)
    print("获得单词数量：" + wordsNum)
    return int(wordsNum)

def QueryResolution(EssayID):
    # 发送Post数据请求
    data = {'jyh': '2009',
            'parm': '{"essayID":"' + EssayID + '"}',
            'sign': '',
            'ts': ''}
    ret = requests.post(url=url, data=data, proxies=proxies).text

    # 返回数据处理
    ret = ret.replace('\\r\\n', '').replace('\\', '')
    #reg = 'ExerciseState": (.*),      "EssayID'
    #Status = re.search(reg, ret).group(1)
    print(ret)

if __name__ == '__main__':
    #login("2020416246", "123456789")    # 登录
    #queryJob()                          # 查询近期是否有未完成的作业
    #getClassInformation(userID)         # 获取班级信息 classID

    #getEssayList('', '0', userID, classID)              #   获取文章列表
    #TouchEassy('73530923d1444a80898926ebd905e4f1')      #   点击进入文章，查询是否做完此文章

    #DoJob('73530923d1444a80898926ebd905e4f1')           #   阅读文章 - 预测答案 - 提交答案
    #QueryResult('73530923d1444a80898926ebd905e4f1')     # 利用漏洞查询文章答案

    #QueryResolution('addea8aa94c2485598e4b3bbb19b9c0d')  # 查询题目解析

    # User Login
    while True:
        username = input("请输入学号：")
        password = input("请输入密码：")
        if login(username, password):
            queryJob()
            getClassInformation(userID)
            break


    Count = 0
    nowPage = 0
    # 确认
    while True:
        Task = int(input("请输入待刷阅读量："))
        flag = input('确认刷' + str(Task) + '词？（y）：')
        if flag == 'y':
            break

    while True:
        if Count >= Task:
            break

        getEssayList('', str(nowPage), userID, classID)
        for (key, value) in EssayList.items():
            if not TouchEassy(value):
                DoJob(value)
                Count += QueryResult(value)
                if Count >= Task:
                    break
        nowPage += 1

    print("任务完成，欢迎下次使用。")
    print("本次共刷取阅读量：" + str(Count))
    os.system('pause')