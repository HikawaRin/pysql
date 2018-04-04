import sys;
sys.path.append(r'E:\xml\pysql\mysqlhandle');
from PyQt5 import QtCore, QtWidgets
import mysqlclient

x = mysqlclient.mysql("118.24.5.150","admin","admin")
x.Database("test2")
x.SELECT(table_name = "test")

app = QtWidgets.QApplication(sys.argv)
widget = QtWidgets.QWidget()
widget.setWindowTitle("Client")
widget.show()

exit(app.exec_())
