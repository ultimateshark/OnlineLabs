import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()
db1=SQLAlchemy()  #Teachers
db2=SQLAlchemy()  #Students

class StudentsCredentials(db.Model):
	__tablename__="studentscredentials"
	student_id=db.Column(db.Integer,primary_key=True)
	username=db.Column(db.String(200),nullable=False)
	password=db.Column(db.String(200),nullable=False)

class TeachersCredentials(db.Model):
	__tablename__="teacherscredentials"
	teacher_id=db.Column(db.Integer,primary_key=True)
	username=db.Column(db.String(200),nullable=False)
	password=db.Column(db.String(200),nullable=False)

class College(db.Model):
	__tablename__="college"
	college_id=db.Column(db.String(20),primary_key=True)
	college_name=db.Column(db.String(50),nullable=False)

class Labs(db.Model):
	__tablename__="labs"
	lab_id=db.Column(db.Integer,primary_key=True)
	teacher_id=db.Column(db.String(20),nullable=False)
	subject=db.Column(db.String(20))
	sem=db.Column(db.String(5),nullable=False)
	sec=db.Column(db.String(5),nullable=False)
	date_created=db.Column(db.String(20),nullable=False)
	lab_url=db.Column(db.String(100),nullable=False)
	ref_no=db.Column(db.String(20),nullable=False)



class TeacherDetails(db1.Model):
	__bind_key__="Teachers"
	__tablename__="teacher_details"
	teacher_id=db1.Column(db1.Integer,primary_key=True)
	username=db1.Column(db1.String(200),nullable=False)
	teacher_name=db1.Column(db1.String(50),nullable=False)
	college_id=db1.Column(db1.String(20),nullable=False)

class TeacherId(db1.Model):
	__bind_key__="Teachers"
	__tablename__="teacherid"
	id=db1.Column(db1.Integer,primary_key=True)
	lab_id=db1.Column(db1.Integer)
	ref_no=db1.Column(db1.String(20),nullable=False)



class StudentDetails(db2.Model):
	__bind_key__="Students"
	__tablename__="student_details"
	student_id=db2.Column(db2.Integer,primary_key=True)
	username=db2.Column(db2.String(200),nullable=False)
	student_name=db2.Column(db2.String(50),nullable=False)
	college_id=db2.Column(db2.String(20),nullable=False)
	course=db2.Column(db2.String(20),nullable=False)
	sem=db2.Column(db2.String(5),nullable=False)
	sec=db2.Column(db2.String(5),nullable=False)
	rollno=db2.Column(db2.String(20),nullable=False)

class StudentId(db2.Model):
	__bind_key__="Students"
	__tablename__="studentid"
	id=db2.Column(db2.Integer,primary_key=True)
	lab_id=db2.Column(db2.String(20),nullable=False)
	expno=db2.Column(db2.String(20))
	problem=db2.Column(db2.String(500))
	submitted=db2.Column(db2.Boolean,default=False)
	checked=db2.Column(db2.Boolean,default=False)
	solution_filename=db2.Column(db2.String(50))

class StudentReg(db2.Model):
	__bind_key__="Students"
	__tablename__="studentreg"
	id=db2.Column(db2.Integer,primary_key=True)
	student_id=db2.Column(db2.String(20))
	lab_id=db2.Column(db2.String(20))
