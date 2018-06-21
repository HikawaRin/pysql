# coding = utf8
# mysql for test ip:118.24.5.150 user:admin pass:admin
import pymysql
from lxml import etree
import time
import copy
# 使用 with codecs.open(path, "w", "utf-8")as f: 格式保存结果防止乱码
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
        self.result = ["ModelID SchemaID Location Date \r\n"]
    
    def LoadXML(self, path):
        self.xmltree = etree.parse(path)

    def LoadDict(self, database, path):
        # 从数据库中读取ID, ElementName和NodeType信息构成ID-节点名字典和节点名字-节点类型字典
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
            # 不是复杂数组内的情况, flag为0
            if self.Type[node.tag] == "Link":
                # 连接节点，无数据
                for child in node:
                    self.getdata(child, 0)
            elif self.Type[node.tag] == "Data":
                # 简单数据节点，无子元素，带有简单数据
                s = str(ModelID) + " " + str(self.ID[node.tag]) + " 0 " + node.text + " \r\n"
                self.result.append(s)
            else:
                # 数组情况，跳转至数组情况(flag == 1)
                self.getdata(node, 1)
        elif flag == 1:
            # 数组情况falg为1，设定数组父节点
            if arrparentnode is None:
                arrparentnode = node
            # 判断是否为复杂数组
            if node[0].tag == "array":
                # 多重数组情况(!只能处理同阶数组)
                # 判断是否为1维数组
                if len(node[0]) == 0:
                    # 1维数组，读取数据
                    for i in range(len(node)):
                        s = str(ModelID) + " "
                        s += str(self.ID[arrparentnode.tag]) + " "
                        s += locinf + str(i) + " "
                        s += node[i].text + " \r\n"
                        self.result.append(s)
                else:
                    # 多维数组进行降阶
                    for i in range(len(node)):
                        sublocinf = locinf + str(i) + ","
                        self.getdata(node[i], 1, sublocinf, arrparentnode)                                    
            else:
                # 复杂数组情况,首级子节点必为连接结点
                for i in range(len(node)):
                    sublocinf = locinf + str(i) + ","
                    self.getdata(node[i], 2, sublocinf, None)
        else:
            # 复杂数组内情况，flag为2
            if self.Type[node.tag] == "Link":
                # 连接节点，无数据
                for child in node:
                    self.getdata(child, 2, locinf, None)
            elif self.Type[node.tag] == "Data":
                # 简单数据节点，无子元素，带有简单数据
                s = str(ModelID) + " " + str(self.ID[node.tag]) + " " + locinf + "0 " + node.text + " \r\n"
                self.result.append(s)
            else:
                # 数组情况，跳转至数组情况(flag == 1)
                self.getdata(node, 1, locinf, None)

    def WriteTXT(self, path):
        with codecs.open(path, "w", "utf-8")as f:
            f.writelines(self.result)

class xml_writer:
    """object organize xml form sql and write data to xml"""
    def __init__(self):
        self.Type = {}
        pass
    
    def SAVE(self, path = "test1.xml"):
        if self.xmltree is not None:
            with open(path, "wb+") as f:
                self.xmltree.write(f, encoding="utf-8", xml_declaration=True, pretty_print=True)

    def set_nodeinfo(self):
        datatype = self.database.Execute("SELECT ElementName, NodeType FROM UnitSchema;")
        for data in datatype:
            self.Type[data[0]] = data[1]

    def Organize(self, database):
        # 先从数据库中抓取xml结构（如结构不变可考虑本地留存结构模板xml直接导入加快速度），再通过节点名称匹配注入数据
        self.database = database
        nodes = list(self.database.Execute("SELECT ID, ParentID, OrderID, ElementName FROM UnitSchema;"))
        # 找到根结点
        for item in nodes:
            if(item[1] == 0):
                root = etree.Element(item[3])
                ID=str(item[0])
                self.xmltree = etree.ElementTree(root)
                nodes.remove(item)
                break
        
        self.add_child(self.xmltree.getroot(), nodes, ID)

        self.set_nodeinfo()

        sqlpath = "SELECT UnitSchema.ElementName, UnitData.location, UnitData.Data FROM UnitSchema, UnitData WHERE UnitData.SchemaID = UnitSchema.ID && UnitData.ModelID = 1";
        data = list(self.database.Execute(sqlpath))
        # self.write_data(self.xmltree.getroot(), data)
        
        write_node_data(self.xmltree.getroot(), self.Type, data)
        print(etree.tostring(root, pretty_print=True).decode("utf8"))
        print(data)

    def add_child(self, node, data, ID):
        subdata = []
        flag = False
        for item in data:
            if(str(item[1]) == ID):
                subdata.append(item)
                flag = True
        if flag is True:
            subdata.sort(key = (lambda item:item[2]))
            for item in subdata:
                child = etree.Element(item[3])
                node.append(child)
                ID=str(item[0])
                data.remove(item)
                self.add_child(child, data, ID)
            subdata.clear()

    # def write_data(self, node, data):
    #     if self.Type[node.tag] == "Link":
    #         for child in node:
    #             self.write_data(child, data)
    #     elif self.Type[node.tag] == "Data":
    #         for item in data:
    #             if node.tag == item[0]:
    #                 node.text = item[2]
    #                 data.remove(item)
    #                 break
    #     else:
    #         if len(node) == 0:
    #             # 多维数组情况
    #             subdata = []
    #             deletdata = []
    #             # 取出数组数据，将location转换为list[int]
    #             for item in data:
    #                 if(node.tag == item[0]):
    #                     deletdata.append(item)
    #                     litem  = list(item)
    #                     locs = item[1]
    #                     subs = locs.split(",")
    #                     for i in subs:
    #                         i = int(i)
    #                     litem[1] = subs
    #                     subdata.append(litem)            
    #             # 删除data中的重复数据
    #             for item in deletdata:
    #                 data.remove(item)
    #             deletdata.clear()
    #             # 创建array节点写入数据
    #             write_array_data(node, subdata)    
    #         else:
    #             # 复杂数组情况，deepcopy数组根结点，获取
    #             pass

def write_array_data(node, data):
    if len(data) == 0:
        return
    else:
        if len(data[0][1]) == 1:
            # 一维数组，写入数据
            data.sort(key = (lambda item:item[1]))
            for item in data:
                anode = etree.Element("array")
                anode.text = item[2]
                node.append(anode)
        else:
            # 多维数组，进行降维
            nodelist = [[]]
            for i in range(len(data)):
                while int(data[i][1][0]) >= len(nodelist):
                    nodelist.append([])
                index = int(data[i][1].pop(0))
                nodelist[index].append(data[i])
            
            for i in range(len(nodelist)):
                s = "array" + str(i)
                croot = etree.Element(s)
                node.append(croot)
                write_array_data(croot, nodelist[i])

def write_node_data(node, node_data_type, data):
    if node_data_type[node.tag] == "Link":
        for child in node:
            write_node_data(child, node_data_type, data)
    elif node_data_type[node.tag] == "Data":
        for item in data:
            if node.tag == item[0]:
                node.text = item[2]
                data.remove(item)
                break
    else:
        if len(node) == 0:
            # 多维数组情况
            subdata = []
            deletdata = []
            # 取出数组数据，将location转换为list[int]
            for item in data:
                if(node.tag == item[0]):
                    deletdata.append(item)
                    # location转换为list[int]
                    litem  = list(item)
                    locs = item[1]
                    if isinstance(locs,str):
                        subs = locs.split(",")
                        for i in subs:
                            i = int(i)
                    
                        litem[1] = subs
                    subdata.append(litem)            
            # 删除data中的重复数据
            for item in deletdata:
                data.remove(item)
            deletdata.clear()
            # 创建array节点写入数据
            write_array_data(node, subdata)    
        else:
            # 复杂数组情况，deepcopy数组根结点，分组写入数据
            subdata = []
            deletdata = []
            nodelist = []
            # 获取复杂节点下的所有数据
            #  获取复杂节点下的所有数据节点名称
            subdatanode(node, node_data_type, nodelist)
            #  获取数据节点数据
            for datanode in nodelist:
                for item in data:
                    if(datanode == item[0]):
                        deletdata.append(item)
                        litem  = list(item)
                        locs = item[1]
                        subs = locs.split(",")
                        for i in subs:
                            i = int(i)
                        litem[1] = subs
                        subdata.append(litem)
                # 删除data中的重复数据
                for item in deletdata:
                    data.remove(item)
                deletdata.clear()
            # 将数据按location分组
            datalist = [[]]
            for i in range(len(subdata)):
                while int(subdata[i][1][0]) >= len(datalist):
                    datalist.append([])
                index = int(subdata[i][1].pop(0))
                datalist[index].append(subdata[i])
            #  写入数据
            for arrdata in datalist:
                ctree = copy.deepcopy(node[0])
                node.append(ctree)
                write_node_data(ctree, node_data_type, arrdata)

def subdatanode(node, node_data_type, nodelist):
    for child in node:
        if node_data_type[child.tag] == "Link":
            for child in node:
                subdatanode(child, node_data_type, nodelist)
        elif node_data_type[child.tag] == "Data":
            nodelist.append(child.tag)
        else:
            if len(child) == 0:
                nodelist.append(child.tag)
            else:
                subdatanode(child, node_data_type, nodelist)
            
    
if __name__=="__main__":
    start =time.clock()

    global ModelID
    ModelID = 1
    # z = SchemaGenerator("unit_test.xml")
    # z.WriteTXT("unit.txt")
    x = mysql()
    x.Database()
    # y = exportData(x)
    # y.Export()
    # y.WriteTXT("data.txt")
    k = xml_writer()
    k.Organize(x)
    # k.SAVE()
    
    end = time.clock()
    print('Running time: %s Seconds'%(end-start))
