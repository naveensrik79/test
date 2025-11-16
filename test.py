from fastapi import FastAPI
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor



app = FastAPI()
#pip install psycopg2-binary
db_url= "postgresql://neondb_owner:npg_p2qU1TSJdmgh@ep-rapid-pine-a46m2rrs-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"


class Students(BaseModel):
    id :int
    name : str
    age : int

class StudentUpdate(BaseModel):
    name: str
    age: int

def get_connection_url():
    conn = psycopg2.connect(db_url, cursor_factory=RealDictCursor)
    return conn

def save_student_to_file(data):
    with open("students.txt", "a") as f:
        f.write(f"{data.id}, {data.name}, {data.age}\n")

@app.post("/students")
def create_student(stud:Students):
    save_student_to_file(stud)
    return {"message": "Student data saved successfully"}

@app.post("/students/db/insert")
def store_student_in_db(student: Students):
    conn = get_connection_url()
    cursor = conn.cursor()
    insert_query = "INSERT INTO students (id, name, age) VALUES (%s, %s, %s)"
    cursor.execute(insert_query, (student.id, student.name, student.age))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": f"Sutdent data successfully inserted database successfully"}


@app.post("/students/db/delete")
def delete_student_in_db(student_id: int):
    conn = get_connection_url()
    cursor = conn.cursor()
    delete_query = "DELETE FROM students WHERE id =%s"
    cursor.execute(delete_query, (student_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": f"Student with ID {student_id} deleted successfully"}


@app.post("/students/db/Update")
def update_student_in_db(student_id: int, student: StudentUpdate):
    conn = get_connection_url()
    cursor = conn.cursor()
    update_query = "UPDATE students SET name = %s, age = %s WHERE id =%s"
    cursor.execute(update_query, (student.name,student.age,student_id))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": f"Student with ID {student_id} updated successfully"}


@app.get("/students/db/select")
def select_student_in_db():
    conn = get_connection_url()
    cursor = conn.cursor()
    select_query = "SELECT * FROM students ORDER BY id "
    cursor.execute(select_query)
    result = cursor.fetchall() 
    cursor.close()
    conn.close()
    return {"Students information extrated from DB":result}



@app.get("/students/db/selectid")
def select_student_in_db_id(student_id: int):
    conn = get_connection_url()
    cursor = conn.cursor()
    select_query_id = "SELECT * FROM students WHERE id =%s"
    cursor.execute(select_query_id, (student_id,))
    rows = cursor.fetchone()
    cursor.close()
    conn.close()
    return {"Student information extracted from DB": rows}