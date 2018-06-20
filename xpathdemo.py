#!/usr/bin/env python
#coding=utf8

from lxml import etree

dict = {
    '饱和特性' : 1,
    '状态' : 2,
    '设置' : 3,
    '输入补偿文件' : 4,
    '输出补偿文件' : 5,
    '扫描参数' : 6,
    '测量设置' : 7,
    '测量仪器' : 8,
    '测量信息' : 9,
    '测量数据' : 10,
    '扫描频率' : 11,
    '起始功率' : 12,
    '截止功率' : 13,
    '电源测量' : 14,
    '前级放大' : 15,
    '输入探头状态' : 16,
    '探头设置' : 17,
    '输出探头状态' : 18,
    '延迟扫描时间' : 19,
    '信号源' : 20,
    '功率计' : 21,
    '行波管电源' : 22,
    '起始时间' : 23,
    '结束时间' : 24,
    '总用时间' : 25,
    '备注' : 26,
    '补偿参数' : 27,
    '静态数据' : 28,
    '过程数据' : 29,
    '分析数据' : 30,
    '输入探头' : 31,
    '输出探头' : 32,
    '电源地址' : 33,
    '电源类型' : 34,
    '最小量程' : 35,
    '最大量程' : 36,
    '校准值' : 37,
    '输入补偿' : 38,
    '输出补偿' : 39,
    '输出功率_float' : 40,
    '电源数据' : 41,
    '电源类型_int64' : 42,
    '输入功率' : 43,
    '输出功率' : 44,
    '小信号输入功率' : 46,
    '小信号输出功率' : 47,
    '小信号增益' : 48,
    '饱和点输入功率' : 49,
    '饱和点输出功率' : 50,
    '饱和点增益' : 51
    }

def getData(node):
    child = node.xpath("./*")
    text = node.xpath("normalize-space(./text())")
    if(len(child) == 0):
        Id = dict[node.tag]
        s = str(ModelID) + " " + str(Id) + " 0 " + text
        #print(s)
        f.write(s)
        f.write("\n")
    elif(len(child) > 1):
        if(child[0].tag == child[1].tag):
        #array
            for i in range(len(child)):
                text = child[i].xpath("normalize-space(./text())")
                Id = dict[node.tag]
                s = str(ModelID) + " " + str(Id) + " " + str(i) + " " + text
                #print(s)
                f.write(s)
                f.write("\n")
        else:
            for item in child:
                getData(item)
    else:
        for item in child:
            getData(item)
        

if __name__=="__main__":
    xml = etree.parse("test2.xml")
    root = xml.getroot()
    f = open('data3.txt','a')
    global ModelID
    ModelID = 2
    print("ModelID ID order data")
    f.write("ID ElementName order data")
    f.write("\n")
    getData(root)
    f.close()
    print("Done")
