
import pymysql

class mysql:
    """sql object to get data from mysql database"""
    def __init__(self, host, user, password):
        self.host = host
        self.user = user
        self.password = password
        self.database = None

    def __del__(self):
        if self.database is not None:
            self.database.close()

    def Database(self, database):
        self.database = pymysql.connect(self.host, self.user, self.password, database)
        if self.database is None:
            print("connect database fail")
        else:
            print("Database changed to:", database);

    def SELECT(self, column_name = "*", table_name = " ", where = None):
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
            for item in data:
                print(item)


            
            
