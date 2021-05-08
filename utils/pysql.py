import os,sys
import pymysql
from . import readini


def sqldecorate(obj):
    father_path = os.path.dirname(os.path.dirname(__file__))

    filepath = os.path.join(father_path,"config","testenv.ini")
    cf = readini.readini(filepath)

    obj.conn=pymysql.connect(host=cf.get('test_db','host'),\
                                  port=int(cf.get('test_db','port')),\
                                  user=cf.get('test_db','user'),\
                                  password=cf.get('test_db','password'),\
                                  database=cf.get('test_db','database')
                                  )

    return obj

@sqldecorate
class PyMySQL:

    def __init__(self):
        pass

    def mysqldel(self,table,data=None):

        sql = "delete from " + table
        where = " where "
        for key in data.keys():
            if isinstance(data[key], str):
                value = "'" + str(data[key]) + "'"
            else:
                value = str(data[key])
            where += str(key) + "=" + value + " and "

        sql = sql + " " + where.strip(' and ')
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)
        except:
            self.conn.ping()              #超时重连，默认300s
            cursor = self.conn.cursor()
            cursor.execute(sql)
        finally:
            self.conn.commit()
            self.conn.close()

    def mysqlupdate(self,table,filter,data=None):

        sql = "update " + table
        setcolumn=" set "
        for key in data.keys():
            if isinstance(data[key], str):
                value = "'" + str(data[key]) + "'"
            else:
                value = str(data[key])
            setcolumn+=str(key) + "=" + value +","

        where = " where "
        for key in filter.keys():
            if isinstance(filter[key], str):
                value = "'" + str(filter[key]) + "'"
            else:
                value = str(filter[key])
            where += str(key) + "=" + value + " and "

        sql = sql +setcolumn.strip(",") +" "+ where.strip(' and ')
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)
        except:
            self.conn.ping()              #超时重连，默认300s
            cursor = self.conn.cursor()
            cursor.execute(sql)
        finally:
            self.conn.commit()
            self.conn.close()


    def mysqlget(self, sql):

        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)
        except:
            self.conn.ping()  # 超时重连，默认300s
            cursor = self.conn.cursor()
            cursor.execute(sql)
        result = cursor.fetchone()  # 获取一条数据,返回的是元祖形式
        if result is not None:
            if len(result)==1:
                result=result[0]
        self.conn.close()

        return result

    def mysqlinsert(self, table,data):
        '''

        :param table: 插入表
        :param data: 插入数据（字段和值组成的字典）
        :return:
        '''

        sql=" insert into "+ table+" "

        column=''
        column_value=''
        for key,value in data.items():
            column+=key+","
            if isinstance(value, str):
                column_value += "'" + str(value) + "'"+","
            else:
                column_value += str(value)+","

        sql=sql+"("+column.strip(',')+") values ("+column_value.strip(',')+")"

        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)
        except:
            self.conn.ping()  # 超时重连，默认300s
            cursor = self.conn.cursor()
            cursor.execute(sql)
        finally:
            self.conn.commit()
            self.conn.close()




    def checkdbok(self,tb=None,data=None):

        sql="select count(*) from "+ tb
        where=" where "
        for key in data.keys():
            if isinstance(data[key], str):
                value = "'" + str(data[key]) + "'"
            else:
                value = str(data[key])
            where += str(key) + "=" + value + " and "

        sql = sql +" " + where.strip(' and ')

        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)
        except:
            self.conn.ping()  # 超时重连，默认300s
            cursor = self.conn.cursor()
            cursor.execute(sql)
        result = cursor.fetchone()[0]  # 获取一条数据
        self.conn.close()
        return result>0
        pass





class PyMySQL_EXECUTE:
    father_path = os.path.dirname(os.path.dirname(__file__))

    filepath = father_path + "\\config\\testenv.ini"

    def __init__(self):
        cf=readini.readini(self.filepath)
        self.conn=pymysql.connect(host=cf.get('test_db','host'),\
                                  port=int(cf.get('test_db','port')),\
                                  user=cf.get('test_db','user'),\
                                  password=cf.get('test_db','password'),\
                                  database=cf.get('test_db','database')
                                  )



    def __call__(self,*args,**kwargs):
        sql=args[0]

        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)
        except:
            self.conn.ping()  # 超时重连，默认300s
            cursor = self.conn.cursor()
            cursor.execute(sql)

        result=None
        if sql.startswith("select"):
            result = cursor.fetchone()[0]  # 获取一条数据

        self.conn.commit()
        self.conn.close()
        return result
        pass


    def mysqlinsert(self, sql):

        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)
        except:
            self.conn.ping()  # 超时重连，默认300s
            cursor = self.conn.cursor()
            cursor.execute(sql)
        self.conn.commit()
        self.conn.close()


    def checkdbok(self,tb,key,value):

        sql="select count(*) from "+ tb +" where "+key+ "='"+value+"'"

        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)
        except:
            self.conn.ping()  # 超时重连，默认300s
            cursor = self.conn.cursor()
            cursor.execute(sql)
        result = cursor.fetchone()[0]  # 获取一条数据
        self.conn.close()
        return result>0
        pass




