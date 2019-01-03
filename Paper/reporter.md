# 微波元器件饱和特性测试数据存储研究  

## 第一章 背景与意义  

二战时对军用雷达的需求，催生出了微波元件，微波元件指在微波系统中实现对微波信号的定向传输、衰减、隔离、滤波、相位控制、波形及极化变换、阻抗变换与调配等功能作用的元件。在今天随着微波技术的不断进步，微波元器件已广泛大量用于通信系统、遥感测绘、雷达、导航、生物医学、电子对抗、人造卫星、宇宙飞船等多种领域。得益于通信技术的迅速发展、市场需求的不断扩大及太赫兹领域的广阔前景，微波元器件及相关介质材料的市场规模也随之急剧上升，发展前景十分乐观。  
为了保证微波元器件的质量并及时发现和解决问题，对微波器件的各种特性参数进行测试是一项必不可少的任务，微波元件的生产及发展离不开微波测试。微波测试技术是微波技术学科的重要组成部分，近年来随着计算机科学的发展及现代计算机的普及，测试技术也正经历着信息化，系统化，自动化，智能化的变革过程。自动化测试将微波测量过程中所涉及到的所有信息都数字化，由系统监控测量过程信息并自动进行调整，最大限度的降低了人员对测量过程带来的干涉，节约大量人力资源，使得测试结果更具有客观性，可重复性。与传统手动测试方法相比，自动化测试系统具有节约测试时间，提高测试精度，减少人为因素的干预的优点，可以同时测量多个参数所需数据，特别是在多个参数互相影响的情况下，可得出更加符合元器件真实使用情况下的特性参数，自动化已成为测试技术发展的必然趋势。近年来构建通用化、网络化、高性能自动测试系统，实现软硬件资源共享，实现测试程序集的可移植性和可重用性已成为发展的主流趋势。  
在自动化测试系统中，一切收集到的信息都会被数据化，而微波元器件涉及的特性参数非常多，且每个特性中涉及的数据也非常多，为将从仪器中收集到的离散的数据结构化供系统调用以完成测试完成后的数据处理分析，有必要实现特性参数数据的数据结构化、持久化，这也是自动化测试系统中的重要组成部分；为了实现测试程序集的可移植性与可重用性，避免并行化自动测试中数据发生混淆有必要实现数据的规范性。  
本文对饱和特性参数这一基础参数进行分析，实现了一种基于对象模型的数据存储方案，在第二章中具体阐述了这一方案，其中第一节具体介绍了这一存储方法使用的主要技术，第二节给出了具体的代码实现。

## 第二章 饱和特性测试数据存储  

### 2.1 主要技术  

#### 2.1.1 XML及XPath  

XML（可扩展标记语言 EXtensible Markup Language）是标记语言的一种，其设计宗旨是传输数据。XML具有自我描述性，且本身不具备任何行为。XML可以通过自定义标签设计出适合特定使用场景的格式规范。XML常用于数据的结构化、存储和传输，是数据交换的公共语言。XPath是一门在XML文档中查找信息的语言，通过XPath可在XML文档中通过元素和属性进行导航。  

#### 2.1.2 关系数据库管理系统  

关系数据库管理系统（Relational Database Management System：RDBMS）是指包括相互联系的逻辑组织和存取这些数据的一套程序 (数据库管理系统软件)。关系数据库管理系统就是管理关系数据库，并将数据逻辑组织的系统。本文采用的是RDBMS中的MySQL软件产品。  

#### 2.1.3 Python  

Python 是一门简单易学且功能强大的编程语言。它拥有高效的高级数据结构，并能够用简单又有效的方式进行面向对象编程。Python 优雅的语法和动态类型，再结合它的解释性，使其在大多数平台的众多领域中，成为编写脚本或开发应用程序的理想语言。本文选用目前的稳定版本Python 3.6作为开发环境。  

### 2.2 实现方式  

#### 2.2.1 将XML文件转化为关系表  

由参考文献[2]中提出的数据存储规范可知特性参数中待处理的数据规模非常大，直接导致了数据的模式非常大，符合半结构化数据的特征，直接使用对象模型进行存储不仅会在使用上带来不便，在效率上也会产生不良的影响，对整个系统的稳定性埋下隐患。为了数据的长期稳定性以及实际使用过程中的方便性，有必要将半结构化数据先进行转换再存储。  
根据已建立空间行波管自动测试系统测试数据存储规范的同一基于XML的数据传输规范，本文将基于XML格式结构化的数据基于一种简单的数据模式转换为关系型数据。具体方法如下：  

  1. 根据XML标签的状态将标签分类为Link、Data、Array三种标签类型，其中Link标签表示该标签是只用于表示数据结构的标签，其必然带有子标签且本身不携带数据，Link标签是专为展现数据的结构而设计出的抽象标签；Data标签则表示一个具体的数据，Data标签必然不存在子标签，携带且只携带一个真实存在的数据；Array标签表示其子标签构成一个数组，是Link标签的拓展，具有Link标签的所有已有特征，在此基础上Array标签还表示其子标签具有相同的结构，Array标签的子标签可以是Data标签以表示一个简单数组，也可以是Link标签以表示一个结构体构成的数组，也可以是Array标签以表示一个多维数组。  

  2. 将XML解析为树形结构，通过一次遍历记录所有用于重现节点的节点信息及位置信息，将XML表示的数据的结构转化为一张结构关系表。  

  3. 检索XML文件中的所有Data节点获取对应的真实数据得到与节点相对应的数据关系表。  

通过这三个步骤可以将XML分解为两张互相关联的关系表，从而将半结构化的数据转换为关系型的数据。  
第一步与第二步没有依赖关系，在实际实现时可以同时完成，本文采用Python及lxml包将XML解析为DOM树实现上述算法：  
用于将XML标签分类并将XML表示的结构转换为结构关系表的部分代码如下  

```python
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
```  

为了体现两张关系表是分离的，即可将一个统一的格式运用于多次测试中，此处代码展示的是从数据库中读取数据作为结构信息的方法（即本节第三部分的内容），实际使用时可选择从本地直接加载XML的方法。
用于将XML中的数据转换为数据关系表的部分代码如下：  

```python
class XpathExportData:
    """a new way to export data from exit xml file by tree"""
    # 维护两棵xml树, 数据xml树位于本地, id xml树位于数据库中(或从本地读取)遍历数据xml树, 通过xpath对应到id xml树, 将数据与id对应
    def __init__(self, database, dataxmlpath = "unit_test.xml", schemapath = "UnitTest"):
        # 导入数据xml树
        self.LoadXML(dataxmlpath)
        # 导入id xml树
        self.LoadSchemaTree(database, schemapath)
        # print(etree.tostring(self.idxmltree.getroot(), pretty_print=True).decode("utf8"))
        # 导出的数据, 用空格分隔元素
        self.result = ["ModelID SchemaID Location Date \r\n"]
        # 导入节点信息字典
        self.Type = {}
        self.set_nodeinfo(schemapath)

    def LoadXML(self, path):
        self.dataxmltree = etree.parse(path)

    def LoadSchemaTree(self, database, path):
        # 从数据库中读取数据构建schema tree, 可考虑从本地读取提高速度
        self.database = database
        s1 = "SELECT ID, ParentID, OrderID, ElementName FROM " + path +"Schema;"
        nodes = list(self.database.Execute(s1))
        # 找到根结点
        for item in nodes:
            if(item[1] == 0):
                root = etree.Element(item[3], ID = str(item[0]))
                ID=str(item[0])
                self.idxmltree = etree.ElementTree(root)
                nodes.remove(item)
                break

        self.add_child(self.idxmltree.getroot(), nodes, ID)

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
                    child = etree.Element(item[3], ID = str(item[0]))
                    node.append(child)
                    ID=str(item[0])
                    data.remove(item)
                    self.add_child(child, data, ID)
                subdata.clear()

    def set_nodeinfo(self, mark):
        s = "SELECT ElementName, NodeType FROM " + mark + "Schema;"
        datatype = self.database.Execute(s)
        for data in datatype:
            self.Type[data[0]] = data[1]

    def Export(self, ModelID):
        self.ModelID = ModelID
        root = self.dataxmltree.getroot()
        xpath = "/" + root.tag
        self.getdata(root, 0, xpath)

    def getdata(self, node, flag, xpath, locinf = "", arrparentnode = None):
        if flag == 0:
            # 不是复杂数组内的情况, flag为0
            if self.Type[node.tag] == "Link":
                # 连接节点，无数据
                for child in node:
                    cxpath = xpath + "/" + str(child.tag)
                    self.getdata(child, 0, cxpath)
            elif self.Type[node.tag] == "Data":
                # 简单数据节点，无子元素，带有简单数据
                xs = xpath + "/@ID"
                nodeid = (self.idxmltree.xpath(xs))[0]
                s = str(self.ModelID) + " " + str(nodeid) + " 0 " + node.text + " \r\n"
                self.result.append(s)
            else:
                # 数组情况，跳转至数组情况(flag == 1)
                self.getdata(node, 1, xpath)
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
                        xs = xpath + "/@ID"
                        nodeid = (self.idxmltree.xpath(xs))[0]
                        s = str(self.ModelID) + " "
                        s += str(nodeid) + " "
                        s += locinf + str(i) + " "
                        s += node[i].text + " \r\n"
                        self.result.append(s)
                else:
                    # 多维数组进行降阶
                    for i in range(len(node)):
                        sublocinf = locinf + str(i) + ","
                        self.getdata(node[i], 1, xpath, sublocinf, arrparentnode)
            else:
                # 复杂数组情况,首级子节点必为连接结点
                for i in range(len(node)):
                    sublocinf = locinf + str(i) + ","
                    cxpath = xpath + "/" + str(node[i].tag)
                    print(sublocinf)
                    self.getdata(node[i], 2, cxpath, sublocinf, None)
        else:
            # 复杂数组内情况，flag为2
            if self.Type[node.tag] == "Link":
                # 连接节点，无数据
                for child in node:
                    cxpath = xpath + "/" + str(child.tag)
                    self.getdata(child, 2, cxpath, locinf, None)
            elif self.Type[node.tag] == "Data":
                # 简单数据节点，无子元素，带有简单数据
                xs = xpath + "/@ID"
                nodeid = (self.idxmltree.xpath(xs))[0]
                s = str(self.ModelID) + " " + str(nodeid) + " " + locinf + "0 " + node.text + " \r\n"
                self.result.append(s)
            else:
                # 数组情况，跳转至数组情况(flag == 1)
                self.getdata(node, 1, xpath, locinf, None)

    def WriteTXT(self, path):
        with codecs.open(path, "w", "utf-8")as f:
            f.writelines(self.result)
```  

通过以上的Python代码即可复现本节所陈述的XML到关系表的转换算法

#### 2.2.2 将转化后的关系表存储到数据库中  

根据上文所阐述的XML到关系表的转换算法中关系表的构造可以很容易在数据库中构建对应的数据库表单，通过MySQL中提供的LOAD DATA LOCAL INFILE接口可以快速将存储的关系表导入数据库对应表单中，完成数据及数据结构的存储。  

#### 2.2.3 将数据库中的数据转化为XML文件  

通过前两部分的算法我们可以将XML分解为结构关系表及数据关系表并存储到数据库中。在数据库已经存储了相关信息的情况下我们可以根据第一部分所述的方法逆推出通过关系表构建XML文件的方法，即首先通过结构关系表中的信息重现没有数据的XML文件，再将数据关系表中的数据插入到对应位置即可复原XML文件。从而完成XML数据的持久化，将XML作为在数据库与自动测试系统间传输数据的桥梁。  
实现XML文件复原的部分代码如下：  

```python
class xml_writer:
    """object organize xml form sql and write data to xml"""
    def __init__(self):
        self.Type = {}
        pass

    def SAVE(self, path = "test2.xml"):
        if self.xmltree is not None:
            with open(path, "wb+") as f:
                self.xmltree.write(f, encoding="utf-8", xml_declaration=True, pretty_print=True)

    def set_nodeinfo(self, mark):
        s = "SELECT ID, NodeType FROM " + mark + "Schema;"
        datatype = self.database.Execute(s)
        for data in datatype:
            self.Type[data[0]] = data[1]

    def Organize(self, database, mark, modelid):
        # 先从数据库中抓取xml结构（如结构不变可考虑本地留存结构模板xml直接导入加快速度），再通过节点名称匹配注入数据
        self.database = database
        s1 = "SELECT ID, ParentID, OrderID, ElementName FROM " + mark +"Schema;"
        nodes = list(self.database.Execute(s1))
        # 找到根结点
        for item in nodes:
            if(item[1] == 0):
                root = etree.Element(item[3], ID = str(item[0]))
                ID=str(item[0])
                self.xmltree = etree.ElementTree(root)
                nodes.remove(item)
                break
        self.add_child(self.xmltree.getroot(), nodes, ID)

        self.set_nodeinfo(mark)
        sqlpath = "SELECT " + mark + "Schema.ID, " + mark + "Data.location, "+ mark + "Data.Data "
        sqlpath += "FROM " + mark + "Schema, " + mark + "Data "
        sqlpath += "WHERE " + mark + "Data.SchemaID = " + mark + "Schema.ID && "+ mark + "Data.ModelID = " + str(modelid) + ";"
        data = list(self.database.Execute(sqlpath))
        write_node_data(self.xmltree.getroot(), self.Type, data)
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
                child = etree.Element(item[3], ID = str(item[0]))
                node.append(child)
                ID=str(item[0])
                data.remove(item)
                self.add_child(child, data, ID)
            subdata.clear()
```  

## 第三章 总结与展望  

## 参考文献  

[1]马竹娟,汪宏喜.一种XML数据库到关系数据库的映射模型[J].计算机与现代化,2010(02):180-182+187.  
[2]赵笠铮, 李谷斌, 黄桃, 宫大鹏, 李盛楠, 刘佳, 张杰, 李斌, “空间行波管自动测试系统测试数据存储规范及管理研究”[A], 中国电子学会真空电子学分会第二十一届学术年会论文集[C], 2018.  
