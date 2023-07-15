import mysql.connector
import datetime 
from tkinter import messagebox
import time

def connectdatabase():
    connection=mysql.connector.connect{
        host="localhost",
        database="FaceId",
        user="root",
        password="123456"
    }
    return connection
def InsertOrUpdate(id,name):
    con=connectdatabase()
    query="Select * from people where id = "+str(id)
    cursor=con.cursor()
    cursor.execute(query)
    records=cursor.fetchall()
    IsRecordExit=0
    for row in records:
        IsRecordExit=1
    if(IsRecordExit==0):
        query="insert into people (id,name) values (%s,%s)"
        cursor.execute(query,(id,name))
    else:
        query="update people set name = %s where id = %s"
        cursor.execute(query,(id,name))
    con.commit()
    con.close()
    cursor.close()



    def CheckinAndCheckout(idPeople):
        check:bool
        cur_time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cur_date=datetime.datetime.now().strftime('%Y-%m-%d')
        con=connectdatabase()
        query="select * from attendance where idpeople = "+str(idPeople)+"and date(timeCheckin) = *"+cur_date
        cursor=con.cursor()
        cursor.execute(query)
        records=cursor.fetchall()
        IsRecordExit=0

        for row in records:
            IsRecordExit=1

        if(IsRecordExit==0):
                query="insert into attendance (idPeople,timeCheckin,timeCheckout) values (%s,%s,%s)"
                cursor.execute(query,(idPeople,cur_time,None))
                check=True
        else:
                query="Update attendance set timeCheckout = %s where idPeople = %s "
                cursor.execute(query,(cur_time,idPeople))
                check=False
        con.commit()
        con.close()
        cursor.close()
        return check 
            



