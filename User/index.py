from flask import Flask,render_template,request
import cx_Oracle
import random

conn = cx_Oracle.connect('SYSTEM/178951@//localhost:1521/xe')
cur = conn.cursor()

app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template('/Home/index.html')

@app.route('/amb')
def amb_page():
    return render_template('/Home/amb.html')

@app.route('/firbrgd')
def fire_page():
    return render_template('/Home/firebrgd.html')

@app.route('/pol')
def pol_page():
    return render_template('/Home/police.html')

@app.route('/signup', methods=['GET','POST'])
def signup_page():
    
     if [request.method == "POST"]:
         user_name = request.form.get('username')
         user_email = request.form.get('email')
         user_number = request.form.get('number')
         user_password = request.form.get("psw")
         print(user_number) 
         user_id =  random.randrange(1000) 
         
         if(user_name!=None and user_email!=None and user_number!=None and user_password!=None):
              sql_insert = """ Insert into application_user(username,email,phone,pass,user_id) values(:user_name,:useremail,:user_number,:user_password,:user_id) """
              cur.execute(sql_insert,(user_name,user_email,user_number,user_password,user_id))
              conn.commit()   
      
     return render_template('/Sign_up/signup.html')


@app.route('/signin',methods=['GET', 'POST'])
def signin_page():
    return render_template('/Sign_in/signin.html')



if __name__ =="__main__":
    app.run(debug=True)