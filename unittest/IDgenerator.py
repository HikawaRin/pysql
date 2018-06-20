#coding = utf8
#mysql for test ip:118.24.5.150 user:admin pass:admin
import pymysql
from lxml import etree
import time
import copy
#使用 with codecs.open(path, "w", "utf-8")as f: 格式保存结果防止乱码
import codecs

class SchemaGenerator:
    """read a xml file and give each node a special id"""
    def __init__(self):
        pass

    def __init__(self, path):
        self.LoadXML(path)
        self.counter = 1
        self.result = ["ID ParentID ElementName OrderID DataType \r\n"]
    
    def LoadXML(self, path):
        self.xmltree = etree.parse(path)

    def generate(self, node, parent_node_id, order):
        if len(node) == 0:
            s = str(self.counter) + " " + str(parent_node_id) + " " + node.tag + " " + str(order) + " Data \r\n"
            self.result.append(s)
            self.counter += 1
            return
        else:
            if node[0].tag == "array":
                s = str(self.counter) + " " + str(parent_node_id) + " " + node.tag + " " + str(order) + " Array \r\n"
                self.result.append(s)
                self.counter += 1
                return
            else:
                s = str(self.counter) + " " + str(parent_node_id) + " " + node.tag + " " + str(order) + " Link \r\n"
                self.result.append(s)
                nodeID = copy.deepcopy(self.counter)
                self.counter += 1

                for i in range(len(node)):
                    self.generate(node[i], nodeID, i)

    def WriteTXT(self, path):
        root = self.xmltree.getroot()
        self.generate(root, 0, 0)

        print(self.result)
        with codecs.open(path, "w", "utf-8")as f:
            f.writelines(self.result)

class mysql:
    """sql object to get data from mysql database"""
    def __init__(self, host = "118.24.5.150", user = "admin", password = "admin"):
        self.host = host
        self.user = user
        self.password = password
        self.database = None

    def __del__(self):
        if self.database is not None:
            self.database.close()

    def SAVE(self):
        if self.database is not None:
            self.database.commit()
        else:
            print("No useable database")

    def Database(self, database = "unittest"):
        self.database = pymysql.connect(self.host, self.user, self.password, database, charset = "utf8", local_infile = 1)
        if self.database.open:
            print("Database changed to:", database)
        else:
            print("connect database fail")

    def Execute(self, s):
        if self.database is None:
            print("No useable database")
            return
        else:
            cursor = self.database.cursor()
            cursor.execute(s)
            data = cursor.fetchall()
            cursor.close()
            return data

    def PExecute(self, s):
        data = self.Execute(s)
        for item in data:
            print(item)

class exportData:
    """export data from exit xml file"""
    def __init__(self):
        pass

    def __init__(self, database, xmlpath = "unit_test.xml", schemapath = "UnitSchema"):
        self.LoadXML(xmlpath)
        self.LoadDict(database, schemapath)
        #print(self.ID)
        #print(self.Type)
        self.result = ["ModelID SchemaID Location Date \r\n"]
    
    def LoadXML(self, path):
        self.xmltree = etree.parse(path)

    def LoadDict(self, database, path):
        #从数据库中读取ID, ElementName和NodeType信息构成ID-节点名字典和节点名字-节点类型字典
        self.ID = {}
        self.Type = {}
        self.database = database
        nodes = self.database.Execute("SELECT ID, ElementName, NodeType FROM " + path + ";")
        for node in nodes:
            self.ID[node[1]] = node[0]
            self.Type[node[1]] = node[2]

    def Export(self):
        root = self.xmltree.getroot()
        self.getdata(root, 0)
        print(self.result)

    def getdata(self, node, flag, locinf = "", arrparentnode = None):
        if flag == 0:
            #不是复杂数组内的情况, flag为0
            if self.Type[node.tag] == "Link":
                #连接节点，无数据
                for child in node:
                    self.getdata(child, 0)
            elif self.Type[node.tag] == "Data":
                #简单数据节点，无子元素，带有简单数据
                s = str(ModelID) + " " + str(self.ID[node.tag]) + " 0 " + node.text + " \r\n"
                self.result.append(s)
            else:
                #数组情况，跳转至数组情况(flag == 1)
                self.getdata(node, 1)
        elif flag == 1:
            #数组情况falg为1，设定数组父节点
            if arrparentnode is None:
                arrparentnode = node
            #判断是否为复杂数组
            if node[0].tag == "array":
                #多重数组情况(!只能处理同阶数组)
                #判断是否为1维数组
                if len(node[0]) == 0:
                    #1维数组，读取数据
                    for i in range(len(node)):
                        s = str(ModelID) + " "
                        s += str(self.ID[arrparentnode.tag]) + " "
                        s += locinf + str(i) + " "
                        s += node[i].text + " \r\n"
                        self.result.append(s)
                else:
                    #多维数组进行降阶
                    for i in range(len(node)):
                        sublocinf = locinf + str(i) + ","
                        self.getdata(node[i], 1, sublocinf, arrparentnode)                                    
            else:
                #复杂数组情况,首级子节点必为连接结点
                for i in range(len(node)):
                    sublocinf = locinf + str(i) + ","
                    self.getdata(node[i], 2, sublocinf, None)
        else:
            #复杂数组内情况，flag为2
            if self.Type[node.tag] == "Link":
                #连接节点，无数据
                for child in node:
                    self.getdata(child, 2, locinf, None)
            elif self.Type[node.tag] == "Data":
                #简单数据节点，无子元素，带有简单数据
                s = str(ModelID) + " " + str(self.ID[node.tag]) + " " + locinf + "0 " + node.text + " \r\n"
                self.result.append(s)
            else:
                #数组情况，跳转至数组情况(flag == 1)
                self.getdata(node, 1, locinf, None)

    def WriteTXT(self, path):
        with codecs.open(path, "w", "utf-8")as f:
            f.writelines(self.result)

def arr_data(node, nodeID, locinf, result):
    """get array data"""
    for i in range(len(node)):
        s = str(ModelID) + " " + nodeID + " " + locinf + "," + str(i) + " " + node[i].text + " \r\n"
        result.append(s)
    
if __name__=="__main__":
    start =time.clock()

    global ModelID
    ModelID = 1
    #z = SchemaGenerator("unit_test.xml")
    #z.WriteTXT("unit.txt")
    x = mysql()
    x.Database()
    y = exportData(x)
    y.Export()
    #y.WriteTXT("data.txt")
    
    end = time.clock()
    print('Running time: %s Seconds'%(end-start))
