import mysql.connector
import constant
import requests
import json
import time
from datetime import datetime, time, timedelta
import json

def getAllBooks():
    query = "SELECT * FROM Books1"
    result = []

    try:
        db = mysql.connector.connect(host=constant.DB_HOST, user=constant.DB_USERNAME, password=constant.DB_PASSWORD,database=constant.DB_NAME)
        cursur = db.cursor()
        data = cursur.execute(query)
        Books = cursur.fetchall()
        for i in Books:
            data = {"id": i[0], "bookname": i[1], "auther": i[2], "items": i[3]}

            result.append(data)
        return result
    except:
        result.append({"status": "500", "msg": "somthing went to wrong"})

    return result


def thiru(data):

    query = "insert into Books1 (book_name,book_author,item) values(%s,%s,%s)"
    result = False
    try:
        db = mysql.connector.connect(host=constant.DB_HOST,user=constant.DB_USERNAME,password=constant.DB_PASSWORD,database=constant.DB_NAME)
        cursur = db.cursor()
        data1 = cursur.execute(query,data)
        db.commit()
        result = True


    except:
        print("somethin")
    return result


def insert_data(val):
    query1="insert into Books1 (book_name,book_author,item) values(%s,%s,%s)"
    result=False
    try:
        db12 = mysql.connector.connect(host=constant.DB_HOST, user=constant.DB_USERNAME, password=constant.DB_PASSWORD,database=constant.DB_NAME)
        cursur = db12.cursor()
        
        data1 = cursur.execute(query1,val)
        db12.commit()
        result = True
    except:
        print("somthing  wrong")

    return result


def api_data(add):


    url = f"https://www.googleapis.com/books/v1/volumes?q={add}+inauthor:keyes&key=AIzaSyCLf1J-zhHycgx9PvwNX5lOAAXrcYiiNt0"


    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    return response.json()
    

def list_books():
    list11=["money","telugu",]
    for i in list11:
        try:

            
    
            reasponse=api_data(i)
            items=reasponse["items"]
            for j in items:
                book_title=j["volumeInfo"]["title"]
                author_name=j["volumeInfo"]["authors"][0]
                k="teledhu"
                val=[book_title, author_name,k]
                insert_data(val)

        except:
            print("failed to url",i)

       

def addstudent(data12):
    query = "insert into student(stu_rollnum,stu_name,gender,password,role)values(%s,%s,%s,%s,%s)"
    result=False
    try:
        db = mysql.connector.connect(host=constant.DB_HOST,user=constant.DB_USERNAME,password=constant.DB_PASSWORD,database=constant.DB_NAME)
        cursur=db.cursor()
        data1=cursur.execute(query,data12)
        db.commit()
        result=True
    except:
        print("something went wrong in the database connection")
    return result


def GetStudent():
    query = "select * from student"
    result = False
    result1=[]
    try:
        db = mysql.connector.connect(host=constant.DB_HOST,user=constant.DB_USERNAME,password=constant.DB_PASSWORD,database=constant.DB_NAME)
        cursur=db.cursor()
        data=cursur.execute(query)
        student=cursur.fetchall()
        for student_id in student:
            result1.append({"id":student_id[0],"stu_rollnum":student_id[1],"stu_name":student_id[2],"gender":student_id[3],"admin":student_id[5]})
        result=True
    except:
        print("something went wrong in the database connection")

    return result1
        

def get_all_student():
    query = "SELECT * FROM student"
    result = []
    db = mysql.connector.connect(host=constant.DB_HOST, user=constant.DB_USERNAME, password=constant.DB_PASSWORD,database=constant.DB_NAME)
    cursur = db.cursor()
    cursur.execute(query)
    student = cursur.fetchall()
    for i in student:
        result.append({"id":i[0],"bookid": i[1], "stu_id": i[2], "issue_date": i[3],"return_date": i[4],"role": i[5]})
    return result

def get_perticular_student_data(data12):
    query1 = "select * from student where stu_rollnum = %s and password = %s"
    result = False
    result1=[]
    try:
        db = mysql.connector.connect(host=constant.DB_HOST, user=constant.DB_USERNAME, password=constant.DB_PASSWORD,database=constant.DB_NAME)
        cursur = db.cursor()
        data1=cursur.execute(query1,data12)
        library = cursur.fetchall()
        for i in library:
            result1.append({"id":i[0],"stu_rollnum": i[1], "stu_name": i[2], "gender": i[3],"password": i[4],"role": i[5]})
        
        result = True

    except:
        print("somthing went wrong in perticular_data_baselogic database logic")
    return result1


def stu_takend_books(stu_id):
    query = "select * from library where stu_id =%s"
    result = False
    result1 = []
    try:
        db = mysql.connector.connect(host=constant.DB_HOST, user=constant.DB_USERNAME, password=constant.DB_PASSWORD,database=constant.DB_NAME)
        cursur = db.cursor()
        data1 = cursur.execute(query,stu_id)
        library = cursur.fetchall()
        for i in library:
            result1.append({"id": i[0], "bookid": i[1],"issue_date": i[3],"return_date": i[4],"time_period": i[5],"penalty": i[6]})
        result = True
    except:
        print("something went wrong in the database")
    
    return result1


def one_student_id(stu_rollnum,password):
    #print(stu_rollnum,password)
    result = False
    result1 =[]
    query1 = "select * from student where stu_rollnum = %s and password =%s"
    try:
        db = mysql.connector.connect(host=constant.DB_HOST, user=constant.DB_USERNAME, password=constant.DB_PASSWORD,database=constant.DB_NAME)
        cursur = db.cursor()
        
        data1=cursur.execute(query1,(stu_rollnum,password))
        library = cursur.fetchall()
        
        for i in library:
            result1.append({"id": i[0], "stu_rollnum": i[1], "stu_name": i[2], "gender": i[3],"role":i[5]})
        return result1
        result = True
    except:
        print("something went wrong in one_student_id")
    return result1

def one_student_id123(data):
    #print(stu_rollnum,password)
    result = False
    result1 =[]
    query1 = "select * from student where stu_rollnum = %s and password =%s"
    try:
        db = mysql.connector.connect(host=constant.DB_HOST, user=constant.DB_USERNAME, password=constant.DB_PASSWORD,database=constant.DB_NAME)
        cursur = db.cursor()
        
        data1=cursur.execute(query1,data)
        library = cursur.fetchall()
        
        for i in library:
            result1.append({"id": i[0], "stu_rollnum": i[1], "stu_name": i[2], "gender": i[3],"role":i[5]})
        return result1
        result = True
    except:
        print("something went wrong in one_student_id")
    return result1


def one_student_deaitiles(stu_rollnum):
    #print(stu_rollnum,password)
    result = False
    result1 =[]
    query1 = "select * from student where stu_rollnum = %s"
    try:
        db = mysql.connector.connect(host=constant.DB_HOST, user=constant.DB_USERNAME, password=constant.DB_PASSWORD,database=constant.DB_NAME)
        cursur = db.cursor()
        
        data1=cursur.execute(query1,stu_rollnum)
        library = cursur.fetchall()
        
        for i in library:
            result1.append({"id": i[0], "stu_rollnum": i[1], "stu_name": i[2], "gender": i[3],"role":i[5]})
        return result1
        result = True
    except:
        print("something went wrong in one_student_id")
    return result1
   

def student_books_data(stu_id):
    result = False
    result1=[]
    query = "select * from library where stu_id = %s"
    
    try:
        db = mysql.connector.connect(host=constant.DB_HOST, user=constant.DB_USERNAME, password=constant.DB_PASSWORD,database=constant.DB_NAME)
        cursur = db.cursor()
        data1 = cursur.execute(query,stu_id)
        library = cursur.fetchall()
        for i in library:
            result1.append({"id": i[0], "bookid": i[1], "stu_id": i[2], "issue_date": i[3],"return_date": i[4],"time_period": i[5],"penalty": i[6]})
        result = True
    except:
        print("something went wrong in the database")
    
    return result1

    




def insert_data_library(data):
    
    query = "insert into library (bookid,stu_id,issue_date,return_date,time_period) values(%s,%s,%s,%s,%s)"
    
   # query3="insert into "
    result = False
    try:
        db = mysql.connector.connect(host=constant.DB_HOST, user=constant.DB_USERNAME, password=constant.DB_PASSWORD,database=constant.DB_NAME)
        cursur = db.cursor()
       
        data1 = cursur.execute(query,data)
    

        db.commit()

        result = True
    except:
        print("somthing problem in Try Block")

    return result
def time_period_update(data):
    query="SELECT DATE_ADD(%s, INTERVAL 10 DAY)"
    result1=[]
    result = False
    date1=""
    try:
        db = mysql.connector.connect(host=constant.DB_HOST, user=constant.DB_USERNAME, password=constant.DB_PASSWORD,database=constant.DB_NAME)
        cursur = db.cursor()
       
        data1 = cursur.execute(query,data)
        data123=cursur.fetchall()
        result1.append(data123)
        result2=str(result1)
        date2=result2[4:len(result2)-4]
        
        date1=date2

        
        result = True

    except:
        print("something went wrong")
    return date1



def read_library():
    query = "select * from library"
    result = False
    result1 = []
    try:
        db = mysql.connector.connect(host=constant.DB_HOST, user=constant.DB_USERNAME, password=constant.DB_PASSWORD,database=constant.DB_NAME)
        cursur = db.cursor()
        data1 = cursur.execute(query)
        library = cursur.fetchall()
        for i in library:
            result1.append({"id": i[0], "bookid": i[1], "stu_id": i[2], "issue_date": i[3],"return_date": i[4],"time_period": i[5],"penalty":i[6]})
        result = True
    except:
        print("something went wrong in the database")
    
    return result1

def read_stu_library_data(data):
    query =  "select * from library where return_date=%s and stu_id=%s and bookid=%s"
    result = False
    result1 = []
    try:
        db = mysql.connector.connect(host=constant.DB_HOST, user=constant.DB_USERNAME, password=constant.DB_PASSWORD,database=constant.DB_NAME)
        cursur = db.cursor()
        data1 = cursur.execute(query,data)
        library = cursur.fetchall()
        for i in library:
            result1.append({"id": i[0], "bookid": i[1], "stu_id": i[2], "issue_date": i[3],"return_date": i[4],"time_period": i[5],"penalty": i[6]})
        result = True
    except:
        print("something went wrong in the read_stu_library_database")
    
    return result1

def difference(data):
    query = "SELECT DATEDIFF(%s,%s) FROM library WHERE stu_id=%s and bookid=%s"
    result = False
    result1 = []
    try:
        db = mysql.connector.connect(host=constant.DB_HOST, user=constant.DB_USERNAME, password=constant.DB_PASSWORD,database=constant.DB_NAME)
        cursur = db.cursor()
        data1 = cursur.execute(query,data)
        library = cursur.fetchall()
        data1=str(library)
        int(data1[2:len(data1)-3])
        result1.append(int(data1[2:len(data1)-3])*10)
        result = True
    except:
        print("something went wrong in the difference data related")
    
    return result1

def penalty_insert(data):
    query = "update library set fine=%s where stu_id=%s and bookid=%s"
    result = False
    try:
        db = mysql.connector.connect(host=constant.DB_HOST, user=constant.DB_USERNAME, password=constant.DB_PASSWORD,database=constant.DB_NAME)
        cursur = db.cursor()
        data1 = cursur.execute(query,data)
        db.commit()
        result = True
    except:
        print("something went wrong in the penaltydatabase")

    return result




def update_returning_date(data):
    query = "update library set return_date=%s where stu_id=%s and bookid=%s"
    result = False
    try:
        db = mysql.connector.connect(host=constant.DB_HOST, user=constant.DB_USERNAME, password=constant.DB_PASSWORD,database=constant.DB_NAME)
        cursur = db.cursor()
        data1 = cursur.execute(query,data)
        db.commit()
        result = True
    except:
        print("something went wrong in the database")

    return result


def view_notreturn_book():
    query = "select * from library where return_date IS NULL"
    result = False
    result1 = []
    try:
        db = mysql.connector.connect(host=constant.DB_HOST, user=constant.DB_USERNAME, password=constant.DB_PASSWORD,database=constant.DB_NAME)
        cursur = db.cursor()
        data1=cursur.execute(query)
        library=cursur.fetchall()
        for i in library:
            result1.append({"id": i[0], "bookid": i[1], "stu_id": i[2], "issue_date": i[3],"return_date": i[4],"time_period": i[5],"penalty": i[6]})
        result = True
    except:
        print("something went wrong in the database")

    return result1


def issue_on_date(date11):

    query = "SELECT * from library WHERE DATE(issue_date)=%s"
    result = False
    result1 = []
    try:
        db = mysql.connector.connect(host=constant.DB_HOST, user=constant.DB_USERNAME, password=constant.DB_PASSWORD,database=constant.DB_NAME)
        cursur = db.cursor()
        data1=cursur.execute(query,date11)
        library = cursur.fetchall()
        for i in library:
            result1.append({"id":i[0],"bookid": i[1], "stu_id": i[2], "issue_date": i[3],"return_date": i[4],"time_period": i[5],"penalty": i[6]})
        
        result = True

    except:
        print("somthing went wrong in issue_data database logic")
    return result1

def return_in_date(date11):

    query = "SELECT * from library WHERE DATE(return_date)=%s"
    result = False
    result1 = []
    try:
        db = mysql.connector.connect(host=constant.DB_HOST, user=constant.DB_USERNAME, password=constant.DB_PASSWORD,database=constant.DB_NAME)
        cursur = db.cursor()
        data1=cursur.execute(query,date11)
        library = cursur.fetchall()
        for i in library:
            result1.append({"id":i[0],"bookid": i[1], "stu_id": i[2], "issue_date": i[3],"return_date": i[4],"time_period": i[5],"penalty": i[6]})
        
        result = True

    except:
        print("somthing went wrong in return_in_date database logic")
    return result1

def penalty():
    pass





def joins_data():
    query = "SELECT l.* ,s.stu_name,b.book_name FROM library AS l LEFT JOIN student AS s ON l.stu_id = s.stu_rollnum LEFT JOIN Books1 AS b ON b.id =l.bookid"
    result = False
    result1 = []
    try:
        db = mysql.connector.connect(host=constant.DB_HOST, user=constant.DB_USERNAME, password=constant.DB_PASSWORD,database=constant.DB_NAME)
        cursur = db.cursor()
        data1=cursur.execute(query)
        library=cursur.fetchall()
        print(library)
        for i in library:
            result1.append({"id": i[0], "bookid": i[1], "stu_id": i[2], "issue_date": i[3],"return_date": i[4],"time_period":i[5],"penalty":i[6],"stu_name":i[7],"book_name":i[8]})
        result = True
    except:
        print("something went wrong in the database")

    return result1

def validate_username_password(username,password):
    query = "select * from student where stu_rollnum=%s and password=%s"
    result = False
    result1 = []
    try:
        db = mysql.connector.connect(host=constant.DB_HOST, user=constant.DB_USERNAME, password=constant.DB_PASSWORD,database=constant.DB_NAME)
        cursur = db.cursor()
        data1=cursur.execute(query,(username,password))
        library = cursur.fetchall()
        for i in library:
            result1.append({"stu_rollnum": i[1], "password": i[4],"role":i[5]})
        
        result = True

    except:
        print("somthing went wrong in validate_username_password database logic")
    return result1

