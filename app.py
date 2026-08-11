import sqlite3
from flask import Flask, request, make_response, g, redirect, url_for, send_file, session
from flask_cors import CORS
from flask_bcrypt import Bcrypt
import os
from dotenv import load_dotenv

DATABASE="./app.db"

app=Flask(__name__)
app.secret_key=os.getenv("SECRET_KEY")
CORS(app)
bcrypt = Bcrypt(app)

def create_password(password):
    pw_hash = bcrypt.generate_password_hash(password).decode("utf-8")
    print(pw_hash)

def check_password(password,pw_hash):
    return bcrypt.check_password_hash(pw_hash, password)

def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        print("database connection opened")
    db.row_factory = make_dicts
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
        print("database connection closed")

@app.route("/users/<int:user_id>")
def get_user_img(user_id):
    if "user" not in session:
        return make_response("Unauthorized",401)
    file_name="users/"+str(user_id)+".png"
    return send_file(file_name, mimetype="image/png")

@app.get("/students")
def get_students():
    if "user" not in session:
            return make_response("Unauthorized",401)
    with app.app_context():
        query="select * from students"
        cur=get_db().execute(query)
        students=cur.fetchall()
        cur.close()
    resp=make_response(students,200)
    return resp

@app.get("/courses")
def get_courses():
    with app.app_context():
        query="select * from courses"
        cur=get_db().execute(query)
        courses=cur.fetchall()
        cur.close()
    resp=make_response(courses,200)
    return resp

@app.get("/faculty")
def get_faculty():
    with app.app_context():
        query="select * from faculty"
        cur=get_db().execute(query)
        faculty=cur.fetchall()
        cur.close()
    resp=make_response(faculty,200)
    return resp

@app.get("/enrollments")
def get_enrollments():
    if "user" not in session:
            return make_response("Unauthorized",401)
    with app.app_context():
        queries=[
            "create view if not exists [course_info] as select id,title,description,faculty from courses;",
            "create view  if not exists [faculty_info] as select users.id, users.fname, users.lname,users.img_url from users inner join faculty where users.id=faculty.id;",
            "create view if not exists [course_faculty_info] as select [faculty_info].fname as faculty_fname, [faculty_info].lname as faculty_lname, [faculty_info].img_url as faculty_img_url,[course_info].description, [course_info].title, [course_info].id as course_id from [faculty_info] inner join [course_info] where [faculty_info].id=[course_info].faculty;",
            "create view if not exists [student_info] as select users.id, users.fname, users.lname, users.img_url from users inner join students where users.id=students.id;",
            "create view if not exists [enrollment_student_info] as select enrollments.course, [student_info].fname as student_fname, [student_info].lname as student_lname, [student_info].img_url as student_img_url from enrollments inner join [student_info] where enrollments.student=[student_info].id;",
            "select faculty_fname, faculty_lname, faculty_img_url, title, student_fname, student_lname, student_img_url from [course_faculty_info] inner join [enrollment_student_info] where [course_faculty_info].course_id=[enrollment_student_info].course;"
        ]
        for query in queries:
            cur=get_db().execute(query)
        enrollments=cur.fetchall()
        cur.close()
    resp=make_response(enrollments,200)
    return resp

@app.get("/enrollments/<int:student_id>")
def get_enrollment(student_id):
    if "user" not in session:
            return make_response("Unauthorized",401)
    with app.app_context():
        query="create view if not exists [course_info] as select id,title,description from courses;"
        cur=get_db().execute(query)
        query="select title, description from [course_info] inner join enrollments where [course_info].id=enrollments.course and student="+str(student_id)+";"
        cur=get_db().execute(query)
        enrollments=cur.fetchall()
        cur.close()
    resp=make_response(enrollments,200)
    return resp

@app.post("/enrollments")
def create_enrollment():
    if "user" not in session:
            return make_response("Unauthorized",401)
    if not request.json.get('student_id') or not request.json.get('course_id'):
             return make_response("An error has occurred",422)
    course_id=request.json['course_id']
    student_id=request.json['student_id']
    with app.app_context():
        cur=get_db()
        try:
            query="insert into enrollments(student,course) values("+str(student_id)+","+str(course_id)+");"
            cur=get_db().execute(query)
            get_db().commit()
            last_id=cur.lastrowid
            query="select enrollments.id,title, description from [course_info] inner join enrollments where [course_info].id=enrollments.course and enrollments.id="+str(last_id)+";"
            cur=get_db().execute(query)
            latest_enrollment=cur.fetchone()
            resp=make_response(latest_enrollment,201)
            return resp
        except Exception as ex:
            print(ex)
            resp=make_response("An error has occurred",422)
            return resp
        finally:
            cur.close()

@app.post("/login")
def login():
        if "user" in session:
                return make_response(session['user'],201)
        username=request.json["username"]
        with app.app_context():
            query="select * from users where user_name=\""+username+"\";"
            print("Query: "+query)
            cur=get_db().execute(query)
            user=cur.fetchone()
            if not user:
                resp=make_response("User does not exist",401)
                return resp
            password=check_password(request.json["password"],user["password"])
            if not password:
                resp=make_response("Invalid username/password",401)
                return resp
            session['user']=user
            resp=make_response(user,201)
            return resp

@app.delete("/logout")
def logout():
    if 'user' in session:
          session.pop("user",None)
    return make_response("",204)