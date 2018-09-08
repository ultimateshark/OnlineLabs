import subprocess
import MySQLdb
def run_java(file_name):
    subprocess.call(["javac",file_name])
    a=subprocess.check_output(["java",str(file_name.split(".")[0])])
    return a
def run_cpp(file_name):
    subprocess.call(["g++",file_name])
    a=subprocess.check_output("./a.out")
    return a
def run_c(file_name):
    subprocess.call(["gcc",file_name])
    a=subprocess.check_output("./a.out")
    return a
def run_python(file_name):
    #subprocess.call(["python",file_name])
    a=subprocess.check_output(["python",file_name])
    return a
def run_mysql(code,userdb,password):
    conn=MySQLdb.connect(db="groot",passwd="mom0511",host="localhost",user="root")
    c=conn.cursor()
    data=c.execute(code)
    data=c.fetchall()
    return str(data)
