#Test sql operation using python connect MySQL

import pymysql
import _tkinter
import tkinter

app = tkinter.Tk()
#open sql
db = pymysql.connect("118.24.5.150","admin","admin","test2" )

title = db.cursor() 
#using cursor() creat cursor
cursor = db.cursor()

title.execute("SELECT column_name from information_schema.columns where table_schema='test2' and table_name='test'") 
#using execute() scan SQL 
cursor.execute("SELECT * FROM test")
 
#using fetchone() get single data
td = title.fetchall()
data = cursor.fetchall()

#print (data); 
#print ("Database version : %s " % data)
 
#close sql
db.close()

listb = tkinter.Listbox(app)

for item in data:
    listb.insert(0, item)
listb.insert(0, td)
listb.pack()
app.mainloop()
