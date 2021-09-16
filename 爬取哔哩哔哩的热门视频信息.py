#!/usr/bin/env python
# coding:utf-8
import requests
import time
import csv
import sys,io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')
                                        #用于解决返回json数据乱码
def html(url):                          #获取页面的基本信息
    headers = {
            'User-Agent':"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3823.400 QQBrowser/10.7.4307.400"
        }
    response = requests.get(url=url,headers=headers).json()
    return response


def data(response):                     #接受页面相关的信息，进行解析
    acess = response['data']['list']    #获取相对应的数据
    Datalist = []                       #将抓取的信息全部放到这个列表中
    for i in acess:
        title = i['title']              # 视频名字
        name = i['owner']['name']       # up名字
        access = i['desc']              # 视频简介
        list = i['short_link_v2']       # 视频的链接
        type = i['tname']               # 视频类型
        like = i['stat']['like']        # 点赞数量
        coin = i['stat']['coin']        # 投币数量
        favorite = i['stat']['favorite']# 收藏量
        share = i['stat']['share']      # 分享量
        # print(name,title,access,type,like,coin,favorite,share,list)
        access = access.replace('\n', '')

        time.sleep(0.5)                 #设置一个时间，防止ip被封

        Datalist.append([title,type,name,access,like,coin,favorite,share,list])
        # print(access)
    return Datalist


def down(Datalist):                     #将数据保存到csv文件中
    path = 'C:\\Users\\Administrator\\Desktop\\学习\\Python学习\\爬虫\\4.爬取豆瓣热门的视频相关信息\\'
    with open(path + '哔哩哔哩热门视频信息.csv','w',encoding='utf-8',newline='') as fp:
        writer = csv.writer(fp)
        writer.writerow(['视频名称','视频类型','up名字','视频简介','点赞数量','投币数','收藏数','分享数','视频链接'])
        for each in Datalist:
            writer.writerow(each)


if __name__=='__main__':

    video = []
    url_1 = 'https://api.bilibili.com/x/web-interface/popular?ps=20&pn={}'
    #抓包发现热门视频一共11页，因此从1开始循环11次
    for i in range(1,12):
        url = url_1.format(i)
        a = data(html(url))
        print('数据全部抓取完成！')
        video = video + a              #将所有的数据全部放到这个列表中，然后进行统一写入
    down(video)
    # a = html(url_1)
    # down(data(a))
