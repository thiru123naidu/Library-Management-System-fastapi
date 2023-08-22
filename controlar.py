from typing_extensions import Annotated
from fastapi import FastAPI
from fastapi import Depends, FastAPI, HTTPException, status,responses
from fastapi.param_functions import Form
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from dbconn import dbconnection
from utils import jwttoken


#import bcrypt
#from passlib.context import CryptContext
from pydantic import BaseModel
import constant
#from jose import JWTError, jwt

from typing import Annotated, Union
#from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
#db = mysql.connector.connect(host=constant.DB_HOST, user=constant.DB_USERNAME, password=constant.DB_PASSWORD,database=constant.DB_NAME)
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Request, HTTPException
class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, jwtoken: str) -> bool:
        isTokenValid: bool = False

        try:
            payload = jwttoken.decode_jwt_token(jwtoken)
            return payload
        except:
            payload = None
        if payload:
            isTokenValid = True
        return isTokenValid


class stu_data(BaseModel):
    stu_rollnum:int
    sname:str
    gender:str
    password:str
    role:str|None=None



def validate_token(token=Depends(OAuth2PasswordBearer(tokenUrl="/login",scheme_name="JWT"))):
    user=jwttoken.decode_jwt_token(token)
    return user

class user():
    def __init__(self,id,stu_rollnum,sname,role):
        self.id = id
        self.stu_rollnum = stu_rollnum
        self.sname = sname
        self.role = role

class tokenschema(BaseModel):
    access_token: str
    refresh_token: str

class library():
    def __init__(self,id,bookid,stu_id,issue_date,return_date):
        self.id = id
        self.bookid = bookid
        self.stu_id = stu_id 
        self.issue_date = issue_date
        self.return_date = return_date       




        

        
     


app = FastAPI()





@app.post("/Add_Book")
def Add_Book(book_name: str, book_author: str, items:str):
    data = [book_name,book_author,items]
    data1 = dbconnection.thiru(data)
    if data1:
        return {"status": 200, "msg": "successfully add the book"}
    else:
        return {"status": 201, "mas": "some thing went to wrong"}

@app.post("/addbookdata")
def addbook():
    
    data14=dbconnection.list_books()
    if not data14:
        return {"status": 200, "msg": "successfully add the book"}
    else:
        return {"status": 201, "mas": "some thing went to wrong"}
    



@app.post("/login",response_model=tokenschema)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    #list1=form_data.password,form_data.stu_rollnum
    data=dbconnection.one_student_id(form_data.username,form_data.password)
    if data:
        return {
            "access_token": jwttoken.jenerate_jwt_token(data[0]),
            "refresh_token": jwttoken.jenerate_jwt_token(data[0]),
        }
    else:
        return "please give a valid username and password"

@app.post("/login1")
def ligin1_user(stu_rollnum:int,password:str,):
    data=[stu_rollnum, password]
    data1=dbconnection.one_student_id123(data)
    print(data1)
    if len(data1)>0:
        token=jwttoken.jenerate_jwt_token(data1[0])
        response = {"token":token}
        return response
    else:
        response ={"status":401,"mag":"sry"}
        return response

    
@app.get("/tokendecode",dependencies=[Depends(JWTBearer())])
def get_tokendecode12(token):
    token_decode = jwttoken.decode_jwt_token(token)
    try:
        if token_decode==None:
            response = {"stutacode":500,"massege":"please login your account"}
            return response
        return token_decode
    except:
        print("error in token decode")
    response = {"status":200,"message":"you don't access to use this api.admin only "}
    return response
    


   
    

@app.get("/getBooks")
def getbooks(user:user=Depends(validate_token)):
    #print(user)
    data=dbconnection.getAllBooks()
    return data

@app.get("/student_taken_book's") 
def students_books(user:library=Depends(validate_token)):
    stu_id=user["stu_rollnum"]
    list1=[stu_id]
    data = dbconnection.student_books_data(list1) 
    if data:
        return data
    else:
        return {"status":2051,"msg":"please give a valid stu_id"}
    

@app.get("/joins_all_table_data")
def joints_data1(user:user=Depends(validate_token)):
    if user["role"]=="admin":

        data=dbconnection.joins_data()
    else:
        data=user["stu_name"]
        return {"status":2051,"msg":f"you don't an access to see all joint's related information Mr(or)MS---->{data}"}




class student1(BaseModel):
    stu_rollnum : int
    stu_name :str
    gender :str
    password : str
    role :str | None=None

@app.post("/insert_stu_data")  
def inser_stu_data(student12:student1,user:user=Depends(validate_token)):
    if user["role"]=="admin":
        data1=[student12.stu_rollnum,student12.stu_name,student12.gender,student12.password,student12.role]
        #print(data1[0])
        data=dbconnection.addstudent(data1)
        if data:
            return {"status":200,"msg":"Successfully added student"}
        else:
            return {"status":401,"msg":"some other error in insert_stu_data"}
    else:
        result = user["stu_name"]
        return {"status":2005,"msg":f"you don't have an access to insert the student data into the student table Mr(or)Ms------>{result}"}

    
@app.get("/read_stu_data_only admin")
def read_studata(user:user=Depends(validate_token)):
    stu_rollnum=user["stu_rollnum"]
    data1=[stu_rollnum]
    result1=dbconnection.one_student_deaitiles(data1)
    if result1==[]:
        return {"status":406,"mas":"this stu_rollnum not exit in the database please give a valid rollnumber"}
    else:
 #data=dbconnection.GetStudent()
        if result1[0]["role"]=="admin":
            data=dbconnection.GetStudent()
            return data
        else:
            return {"status":501,"msg":"you don't have an access to see all the students deatiles because your not admin"}
        


@app.get("/read_library_data")
def get_librarydata(user:user=Depends(validate_token)):
    if user["role"]=="admin":
        data = dbconnection.read_library()
        return data
    else:
        result = user["stu_name"]
        return {"status":2005,"msg":f"you don't have an access to see library data Mr(or)Ms----->{result}"}

@app.post("/insert_library_data")
def insert_librarydata(book_id: int, stu_id: int, issue_date: str, return_date: str|None=None,user:user=Depends(validate_token)):
    if user["role"]=="admin":
        data1=issue_date.replace('"', "'")
        date1=[data1]
        time_period=dbconnection.time_period_update(date1)
        #print("timr",time_period)
        data = [book_id, stu_id, issue_date, return_date,time_period]
        data2 = dbconnection.insert_data_library(data)
        if data2:
            return {"status": 200, "msg": "successfully add the data"}
        else:
            return {"status": 201, "mas": "some thing went to wrong"}
    else:
        result = user["stu_name"]
        return {"status":2005,"msg":f"you don't have an access assigning the books for students Mr(or)Ms------>{result}"}

@app.get("/get_not_return_book")
def not_returnbooks(user:user=Depends(validate_token)):
    #print(user)
    if user["role"]=="admin":
        data = dbconnection.view_notreturn_book()
        return data

    else:
        result = user["stu_name"]
        return {"status":2005,"msg":f"you don't have an access to see who are not returning the books related data Mr(or)Ms-------->{result}"}
    
            

@app.get("/issue_date")
def issue_date_book(issue_date:str,user:user=Depends(validate_token)):
    if user["role"]=="admin":
        data1=issue_date.replace('"', "'")

        data2=[data1]
        data=dbconnection.issue_on_date(data2)
        if data:
            return data
        else:
            return {"status-code":"please enter a valid issue date"}
    else:
        result = user["stu_name"]
        return {"status":2005,"msg":f"you don't have an access to see issue_books_data Mr(or)Ms----->{result}"}

@app.get("/return_date")
def return_date_book(return_date:str,user:user=Depends(validate_token)):
    if user["role"]=="admin":
        data1=return_date.replace('"', "'")
        data2=[data1]
        data=dbconnection.return_in_date(data2)
        if data:
            return data
        else:
            return {"status-code":"please enter a valid return_date"}
    else:
        result = user["stu_name"]
        return {"status":2005,"msg":f"you don't have an access to see returning booksdata Mr(or)Ms----->{result}"}
    
@app.put("/returning_book")
def penalty_money(return_date:str,stu_id:int,bookid:int,user:user=Depends(validate_token)):
    if user["role"]=="admin":
        data20 = [return_date,stu_id,bookid]
        #data20 = [date,stu_id,bookid]
        dbconnection.update_returning_date(data20)
        result=dbconnection.read_stu_library_data(data20)
        time_period=result[0]["time_period"]
        return_date1=return_date.replace('"', "'")
        val=str(time_period)
        time_period1=val.replace('"', "'")
        if time_period1<return_date1:
            date1=[return_date1,time_period1,stu_id,bookid]
            data=dbconnection.difference(date1)
            penality=data[0]
            list1=[penality,stu_id,bookid]
            result =dbconnection.penalty_insert(list1)
            result123 = user["stu_name"]
            if result:
                return {"status":200,"msg":f"you have to pay {penality} rupees penalty for submitting the book delay Mr(or)Ms------->{result123}"}
            

        else:
            return {"status":200,"msg":"thanks for returning the book you need not to pay penalty because you are submitted book with in a time period Mr(or)Ms------->{result123}"}
    else:
        result = user["stu_name"]
        return {"status":2005,"msg":f"you are not an admin Mr(or)Ms----->{result}"}

        

    

        




