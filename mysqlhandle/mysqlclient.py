#coding = utf8
#mysql for test ip:118.24.5.150 user:admin pass:admin
import pymysql

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
            
    def SHOW_Databases(self):
        databases = pymysql.connect(self.host, self.user, self.password)
        if databases.open:
            cursor = databases.cursor()
            cursor.execute("SHOW DATABASES")
            data = cursor.fetchall()
            databases.close()
            cursor.close()
            for item in data:
                print(item)
        else:
            print("connect database fail")

    def Database(self, database = "test2"):
        self.database = pymysql.connect(self.host, self.user, self.password, database, charset = "utf8", local_infile = 1)
        if self.database.open:
            print("Database changed to:", database)
        else:
            print("connect database fail")

    def SELECT(self, column_name = "*", table_name = "SCSchemautf8", where = None):
        if self.database is None:
            print("No useable database")
            return
        else:
            cursor = self.database.cursor()
            path = "SELECT " + column_name + " FROM " + table_name
            if where is not None:
                path = path + " WHERE " + where
            cursor.execute(path)
            data = cursor.fetchall()
            cursor.close()
            for item in data:
                print(item)

    def INSERT(self, table_name = "test"):
        if self.database is None:
            print("No useable database")
            return
        else:
            title = self.database.cursor()
            st = "DESC " + table_name
            title.execute(st)
            td = title.fetchall()
            title.close()
            for item in td:
                print(item)
            s = input("VALUES:")
            s = "INSERT INTO " + table_name + " VALUES(" + s + ")"
            print(s)
            cursor = self.database.cursor()
            cursor.execute(s)
            cursor.close()

    def DELETE(self, table_name = "test", where = " "):
        print("Are you sure del:")
        mysql.SELECT(self, table_name = table_name, where = where)
        x = input("(y/n)")
        s = "DELETE FROM " + table_name + " WHERE " + where
        if x == "y":
            mysql.Execute(self, s)
            print("Use save to del from database")

    def LOAD_Local_data(self, path = "SCSchema.txt", table = "SCSchemautf8", terminated = ","):
        s = "LOAD DATA LOCAL INFILE " + "'" + path + "'" + " INTO TABLE " + table + " FIELDS TERMINATED BY " + "'" + terminated + "'" + " LINES TERMINATED BY '\r\n' IGNORE 1 LINES;"
        print(s)
        mysql.Execute(self, s)
        print("Use save to updata data")
    #def UPDATE(self, table_name = "test", Set = " ", where = None)

    def Execute(self, s):
        if self.database is None:
            print("No useable database")
            return
        else:
            cursor = self.database.cursor()
            cursor.execute(s)
            #data = cursor.fetcall()
            #if data is not None:
            #    for item in data:
            #        print(item)

            
            
