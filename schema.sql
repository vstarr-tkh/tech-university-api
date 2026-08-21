CREATE TABLE users(
id integer primary key,
fname varchar,
lname varchar,
img_url varchar
, password varchar, user_name varchar);
CREATE TABLE courses(
id integer primary key,
title varchar,
description varchar,
faculty integer,
foreign key(faculty) references faculty(id)
);
CREATE TABLE faculty(
id integer primary key,
bio  text,
foreign key(id) references users(id)
);
CREATE TABLE students(
id integer primary key,
gpa  real,
grade_level varchar,
foreign key(id) references users(id)
);
CREATE VIEW [faculty-info] as select users.fname, users.lname,user.img_url from users inner join faculty;
CREATE VIEW [faculty_info] as select users.id, users.fname, users.lname,users.img_url from users inner join faculty where users.id=faculty.id
/* faculty_info(id,fname,lname,img_url) */;
CREATE VIEW [course_info] as select id,title,description,faculty from courses
/* course_info(id,title,description,faculty) */;
CREATE VIEW [course_faculty_info] as select [faculty_info].fname as faculty_fname, [faculty_info].lname as faculty_lname, [faculty_info].img_url as faculty_img_url,[course_info].description, [course_info].title, [course_info].id as course_id from [faculty_info] inner join [course_info] where [faculty_info].id=[course_info].faculty
/* course_faculty_info(faculty_fname,faculty_lname,faculty_img_url,description,title,course_id) */;
CREATE VIEW [student_info] as select users.id, users.fname, users.lname, users.img_url from users inner join students where users.id=students.id
/* student_info(id,fname,lname,img_url) */;
CREATE VIEW [enrollment_student_info] as select enrollments.course, [student_info].fname as student_fname, [student_info].lname as student_lname, [student_info].img_url as student_img_url from enrollments inner join [student_info] where enrollments.student=[student_info].id
/* enrollment_student_info(course,student_fname,student_lname,student_img_url) */;
CREATE TABLE enrollments(
id integer primary key,
student integer,
course integer,
foreign key(student) references students(id),
foreign key(course) references courses(id),
unique(student,course)
);
CREATE UNIQUE INDEX unique_username on users(user_name);