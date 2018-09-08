from flask import Flask,render_template,request,redirect,url_for,flash,session
import runp
from passlib.hash import sha256_crypt
from flask_mail import Mail,Message
import random
import string
from labsql import *
from functools import wraps

app=Flask(__name__)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT']=465
app.config['MAIL_USERNAME']='in.hodophile@gmail.com'
app.config['MAIL_PASSWORD']='rajatmanish'
app.config['MAIL_USE_TLS']=False
app.config['MAIL_USE_SSL']=True
mail=Mail(app)


app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:mom0511@localhost/groot"
app.config["SQLALCHEMY_BINDS"]={
									"Teachers":"mysql+pymysql://root:mom0511@localhost/teachers",
									"Students":"mysql+pymysql://root:mom0511@localhost/students"
								}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)
db.app=app
#db.create_all()
db1.init_app(app)
db1.app=app
db2.init_app(app)
db2.app=app



def pass_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


@app.route("/")
def home():
    return render_template("home.html")

@app.route("/run",methods=["GET","POST"])
def run():
    extention=request.form["ext"]
    name=request.form["filename"]
    code=request.form["code"]
    file_name=name+"."+extention
    f=open(file_name,"w")
    f.write(code)
    f.close()
    if extention == "java":
        output=runp.run_java(file_name)
        return render_template("output.html",output=output)
    elif extention == "cpp":
        output=runp.run_cpp(file_name)
        return render_template("output.html",output=output)
    elif extention == "c":
        output=runp.run_c(file_name)
        return render_template("output.html",output=output)
    elif extention == "python":
        output=runp.run_python(file_name)
        return render_template("output.html",output=output)
    elif extention == "sql":
        userdb="groot"
        password="mom0511"
        output=runp.run_mysql(code,userdb,password)
        return render_template("output.html",output=output)

@app.route("/login-sign-page")
def login_sign_page():
    return render_template("login.html")

@app.route("/signup-page")
def signup_page():
    return render_template("select.html")

@app.route("/signup-page/Teacher")
def signupTeacher():
    return render_template("sign.html")

@app.route("/signup-page/Student")
def signupStudent():
    return render_template("signStu.html")
@app.route("/run-now")
def run_now():
	return render_template("editor.html")
@app.route("/user/<string:type>/<string:path>")
def user_log(type,path):
	if session['username']!=None:
		client=session['username']
		if type=="Teacher":
			if path=="home":
				user=TeacherDetails.query.filter_by(username=client).all()[0]
				return render_template("teacherdash.html",name=user.teacher_name)
			if path=="createlab":
				return render_template("createlab.html")
			if path=="create-lab":
				name=request.form["name"]
				sec=request.form["sec"]
				sem=request.form["sem"]
				lab=Labs(teacher_id=pass_generator(),subject=pass_generator(),sem=sem,sec=sec,date_created=pass_generator(),lab_url=pass_generator(),ref_no=pass_generator())
				db.session.add(lab)
				db.session.commit()
				return "Lab Created"
		if type=="Student":
			if path=="home":
				user=StudentDetails.query.filter_by(username=client).all()[0]
				return render_template("studentdash.html",name=user.student_name)
			if path=="run-page":
				return render_template("editor.html")

@app.route("/login/<string:type>",methods=["GET","POST"])
def login(type):
    if request.method=="POST":
        uname=request.form["username"]
        passwd=request.form["passwd"]
        if type=="Teacher":
			user=TeachersCredentials.query.filter_by(username=uname).all()
			if len(user)==0:
				flash("No such Teacher Present!!!")
				return redirect(url_for("login_sign_page"))
			if sha256_crypt.verify(passwd,user[0].password):
				session['logged_in']=True
				session['username']=uname
				return redirect("/user/Teacher/home")
			else:
				flash("Wrong Credentials")
				return redirect(url_for("login_sign_page"))
        else:
			user=StudentsCredentials.query.filter_by(username=uname).all()
			if len(user)==0:
				flash("No such Student Present!!!")
				return redirect(url_for("login_sign_page"))
			if sha256_crypt.verify(passwd,user[0].password):
				session['logged_in']=True
				session['username']=uname
				return redirect("/user/Student/home")
    else:
        flash("Not Allowed")
        return redirect(url_for("login_sign_page"))


@app.route("/signup/<string:type>",methods=["GET","POST"])
def signup(type):
    if request.method=="POST":
        if type=="Teacher":
			clgname=request.form["clgname"]
			tecname=request.form["tecname"]
			uname=request.form["username"]
			passwd=pass_generator()
			msg=Message('FROM Onlinelabs',sender='in.hodophile@gmail.com',recipients=[uname])
			msg.body="your password for first login is "+passwd
			mail.send(msg)
			passwd=sha256_crypt.encrypt(passwd)
			insert_techer_cred=TeachersCredentials(username=uname,password=passwd)
			db.session.add(insert_techer_cred)
			db.session.commit()
			user=TeachersCredentials.query.filter_by(username=uname).all()[0]
			insert_techer_detail=TeacherDetails(teacher_id=user.teacher_id,username=user.username,teacher_name=tecname,college_id=clgname.split("-")[-1])
			db1.session.add(insert_techer_detail)
			db1.session.commit()
			flash("Password for first login sent to your mail!!!")
			return redirect(url_for("login_sign_page"))
        if type=="Student":
			clgname=request.form["clgname"]
			stuname=request.form["stuname"]
			uname=request.form["username"]
			course=request.form["course"]
			sem=request.form["sem"]
			section=request.form["sec"]
			rollno=request.form["roll"]
			branch=request.form["branch"]
			passwd=pass_generator()
			msg=Message('FROM Onlinelabs',sender='in.hodophile@gmail.com',recipients=[uname])
			msg.body="your password for first login is "+passwd
			mail.send(msg)
			passwd=sha256_crypt.encrypt(passwd)
			insert_stu_cred=StudentsCredentials(username=uname,password=passwd)
			db.session.add(insert_stu_cred)
			db.session.commit()
			user=StudentsCredentials().query.all()[0]
			insert_stu_detail=StudentDetails(student_id=user.student_id,username=user.username,student_name=stuname,college_id=clgname.split("-")[-1],course=course,sem=sem,sec=section,rollno=rollno)
			db2.session.add(insert_stu_detail)
			db2.session.commit()
			flash("Password for first login sent to your mail!!!")
			return redirect(url_for("login_sign_page"))



def login_required(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return f(*args, **kwargs)
		else:
			return redirect(url_for('home'))
	return wrap



@app.route("/logout")
@login_required
def logout():
	try:
		client_email=session['username']
		session.pop('username',None)
		return redirect(url_for("main"))
	except:
		flash("ALREADY LOGGED OUT")
		return redirect(url_for("home"))

app.secret_key = "this is nothing but a secret key"
if __name__ == '__main__':
    app.run(debug="true",port=8000 )
