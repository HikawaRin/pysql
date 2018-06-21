# pysql
use python control sql

# 对于复杂结构的两种思路
## 方案一：添加节点数据类型属性
        添加一个用于表示节点所带数据类型的属性，属性包含(null， simple， array， repeat）四种状态。
        1. null表示节点下无数据，节点为连接节点
        2. simple表示节点下只有一项简单数据(如：int，string等)
        3. array表示节点下为数组类型数据
        4. repeat表示存在节点的复用