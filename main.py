from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def test():
    return {"message": "API is running successfully"}


@app.get("/navee/test")
def test1():
    return {"message": "i am student of sudhanshu"}


students = {"1":"akash","2":"rohit","3":"sachin"}


@app.get("/students")
def test1():
    return students

@app.get("/students/{stud_id}")
def student_serach(stud_id):
    return {"id":stud_id, "name":students[stud_id]}



@app.get("/add_student")
def add_student(stud_id:int, name:str):
    students[stud_id] = name
    return students


@app.post("/add_student_diff")
def add_studetn_diff():
    students['new_id'] = "new_name"
    return students

from pydantic import BaseModel

class newdata(BaseModel):
    stud_id:int
    name:str

@app.post("/add_student_new_value")
def add_detudet_new_value(newdata:newdata):
    students[newdata.stud_id] = newdata.name
    return students
