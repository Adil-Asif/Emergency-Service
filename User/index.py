from flask import Flask, render_template, request, redirect
from flask_mail import Mail, Message
import cx_Oracle
import random

conn=cx_Oracle.connect('SYSTEM/password@//localhost:1521/xe')
cur = conn.cursor()

app = Flask(__name__)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'username'
app.config['MAIL_PASSWORD'] = 'password'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)





@app.route('/fail')
def fail_page():
    return render_template('/Sign_up/fail.html')


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


@app.route('/signup', methods=['GET', 'POST'])
def signup_page():
    
    #reads data from signup form
    if request.method == "POST":
        user_name = request.form.get('username')
        user_email = request.form.get('email')
        user_number = request.form.get('number')
        user_password = request.form.get("psw")
        status = "Not Verified"
        print(user_name, user_email, user_number, user_password)
        
        name = user_name
        passw = user_password
        
        #checks if data entered is not null
        if user_name != None and user_email != None and user_number != None and user_password != None:
             #assigns a unique user id checks from database to make sure id is not already present
             flag = True
             while flag == True:
                 user_id = name[0:2] + passw[0:2] + \
                     str(random.randrange(1000, 9999))
                 sql_search = 'Select count(user_id) from application_user where user_id = :user_id'
                 cur.execute(sql_search,[user_id])
                 count_id = cur.fetchall()
                 
                 if count_id[0][0] == 0:
                     flag = False

             #verifies if email address and mobile is unique
             sql_count = 'Select count(phone) from application_user where phone = :user_number'
             cur.execute(sql_count,[user_number])
             count_number = cur.fetchall()
             sql_search = 'Select count(email) from application_user where email = :user_email'
             cur.execute(sql_search,[user_email])
             count_email = cur.fetchall()
             #print(count_email[0][0])
             #print(count_number[0][0])
             

             if count_email[0][0] == 0 and count_number[0][0] == 0:
                 
                 sql_insert = """ Insert into application_user(username,email,phone,pass,user_id,status) values(:user_name,:useremail,:user_number,:user_password,:user_id,:status) """
                 cur.execute(sql_insert, (user_name, user_email,
                             user_number, user_password, user_id, status))
                 conn.commit()
                 
                 global otp
                 otp = random.randrange(100000,999999)
                 msg = Message('Email Verification for Emergency Services Account', sender = 'Emergency Services Application', recipients = [user_email])
                 msg.body = "Thank You for Signing Up for emergency service please use this OTP to verify your account: " + str(otp)
                 mail.send(msg)
                  
                 url = "/verifyemail/" + user_email
                 return redirect(url)
                 
             else:
               return fail_page()

    return render_template('/Sign_up/signup.html')


@app.route('/signin', methods=['GET', 'POST'])
def signin_page():
         
        #reads data from signin form
        
        if request.method == "POST":
          user_email = request.form.get('email')
          user_password = request.form.get("psw")
          #print(user_email, user_password)
          if user_email != None and user_password != None:

             sql_search = 'Select * from application_user where email = :user_email and pass = :user_password'
             sql_count = 'Select count(*) from application_user where email = :user_email and pass = :user_password'
             cur.execute(sql_search,[user_email,user_password])
             search_res = cur.fetchall()
             cur.execute(sql_count,[user_email,user_password])
             count = cur.fetchall()
             #print(search_res)
             #print(count)
             #checks if email and passwords match
             if count[0][0] > 0:
                     if search_res[0][5] != 'Not Verified':
                         global login_id
                         login_id = search_res[0][4]
                         print(login_id)
                         return redirect('/homepage')
                     else:
                             return render_template('/Sign_up/reg.html')
              
             else:
                     return render_template('/Sign_in/fail.html')
                     # exit


        return render_template('/Sign_in/signin.html')


@app.route('/homepage')
def home_page():
     print(login_id)
     return render_template('/Sign_in/index.html')


@app.route('/police')
def police_page():
    print(login_id)
    return render_template('/Sign_in/police.html')


@app.route('/ambulance')
def ambulance_page():
    print(login_id)
    return render_template('/Sign_in/amb.html')


@app.route('/firebrgd')
def firebrgd_page():
    print(login_id)
    return render_template('/Sign_in/firebrgd.html')


@app.route('/complain', methods=['GET', 'POST'])
def complain_page():
       
       #reads input from complaint form
     if request.method == "POST":
        emer_add = request.form.get('address')
        complain_type = request.form.get('complain')
        detail = request.form.get('detail')
        user_id = login_id
        app_id = None
        status = "Generating"
        complain_id = None
        #print(emer_add, complain_type, detail)
       
       #checks if any input is not null
        if complain_type != None and detail != None and emer_add != None:
             #generate unique complain id
             flag = True
             while flag == True:
                 complain_id = "COM" + user_id[0:2] + \
                     str(random.randrange(1000, 9999))
                 sql_count = 'Select count(complain_id) from complain where complain_id = :complain_id'
                 cur.execute(sql_count,[complain_id])
                 count = cur.fetchall()
                 #print(count)
                 
                 if count[0][0] == 0:
                     flag = False
                #stores input in database
             sql_insert = """ Insert into complain(complain_id,status,complain_type,complain_details,user_id,app_id,address)
                              values(:complain_id, :status, :complain_type, :detail, :user_id, :app_id, :emer_add) """
             cur.execute(sql_insert, (complain_id, status,
                             complain_type, detail, user_id, app_id, emer_add))
             conn.commit()
             return render_template('/Sign_in/success.html')
   
     return render_template('/Sign_in/complain.html')


@app.route('/registered',methods=['GET', 'POST'])
def registered_page():
     #show complaints in that are not yet processed
      print(login_id)
      sql_search = 'Select * from complain where user_id = :login_id'
      cur.execute(sql_search,[login_id])
      res = cur.fetchall()
      #print(type(login_id))
      #print(res)

      return render_template('/Sign_in/registered.html',records=res,verify_id=login_id)

@app.route('/registered/<complain_id>')
def registered_display_page(complain_id=None):
     #shows complaint details
     sql_search = """ select complain.complain_id, complain.app_id,  complain.complain_type, complain.status, complain.complain_details, complain.address, application_user.username
                      from complain inner join application_user on application_user.user_id = complain.user_id
                      where complain_id= :complain_id """
     cur.execute(sql_search,[complain_id])
     res = cur.fetchall()
     
     return render_template('/Sign_in/more_detail.html',record=res[0])

@app.route('/processing',methods=['GET', 'POST'])
def processing_page():
      #show complaints in that are in processing stage
      print(login_id)
      sql_search = 'Select * from complain where user_id = :login_id'
      cur.execute(sql_search,[login_id])
      res = cur.fetchall()
      #print(type(login_id))
      print(res)

      return render_template('/Sign_in/processing.html',records=res,verify_id=login_id)

@app.route('/processing/<complain_id>')
def processing_display_page(complain_id=None):
     #displays complaint details
     sql_search = """ select complain.complain_id, complain.app_id,  complain.complain_type, complain.status, complain.complain_details, complain.address, application_user.username
                      from complain inner join application_user on application_user.user_id = complain.user_id
                      where complain_id= :complain_id """
     cur.execute(sql_search,[complain_id])
     res = cur.fetchall()


     if res[0][1] != None:
         sql_search = """ select application_manager.username
                      from complain inner join application_manager on application_manager.app_id = complain.app_id
                      where complain_id= :complain_id """
     
         cur.execute(sql_search,[complain_id])
         res2 = cur.fetchall()
         print(res2)

     return render_template('/Sign_in/more_detail.html',record=res[0], app_name=res2[0][0] )


@app.route('/solved',methods=['GET', 'POST'])
def solved_page():
      #show complaints in that are solved
      print(login_id)
      sql_search = 'Select * from complain where user_id = :login_id'
      cur.execute(sql_search,[login_id])
      res = cur.fetchall()
      #print(type(login_id))
      print(res)

      return render_template('/Sign_in/solved.html',records=res,verify_id=login_id)

@app.route('/solved/<complain_id>')
def solved_display_page(complain_id=None):
      #displays complain details
     sql_search = """ select complain.complain_id, complain.app_id,  complain.complain_type, complain.status, complain.complain_details, complain.address, application_user.username
                      from complain inner join application_user on application_user.user_id = complain.user_id
                      where complain_id= :complain_id """
     cur.execute(sql_search,[complain_id])
     res = cur.fetchall()
     
     if res[0][1] != None:
         sql_search = """ select application_manager.username
                      from complain inner join application_manager on application_manager.app_id = complain.app_id
                      where complain_id= :complain_id """
     
         cur.execute(sql_search,[complain_id])
         res2 = cur.fetchall()
         print(res2)

     return render_template('/Sign_in/more_detail.html',record=res[0], app_name=res2[0][0] )


@app.route('/verifyemail/<user_email>',methods=['GET', 'POST'])
def verify_email_page(user_email=None):
     if request.method == "POST":
          user_otp = request.form.get('otp')
          print(otp)
          print(type(user_otp))
          #print(user_email, user_password)
          
          if user_otp == str(otp):
                 msg = Message('Emergency Services Account Registered', sender = 'Emergency Services Application', recipients = [user_email])
                 msg.body = "Thank You for choosing Emergency Service. We are happy to serve you"
                 mail.send(msg)
                 veri = 'verified'
                 sql_search = """update application_user set status=:veri where email = :user_email"""
                 cur.execute(sql_search,[veri,user_email])
                 conn.commit()
                 return render_template('/Sign_up/success.html')
               
          else:
                 sql_search = "DELETE From application_user where email = :user_email"
                 cur.execute(sql_search,[user_email])
                 conn.commit()
                 return render_template('/Sign_up/verify.html')
     
     return render_template('/Sign_up/otp.html',user_email = user_email)



             

if __name__ == "__main__":
    app.run(debug=True)

 
        
