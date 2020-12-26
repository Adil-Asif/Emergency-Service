from flask import Flask, render_template, request, redirect
import cx_Oracle
import random

conn=cx_Oracle.connect('SYSTEM/password@//localhost:1521/xe')
cur = conn.cursor()

app = Flask(__name__)


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
        app_man_name = request.form.get('username')
        app_man_email = request.form.get('email')
        app_man_number = request.form.get('number')
        app_man_password = request.form.get("psw")
        #print(user_name, user_email, user_number, user_password)
       
        name = app_man_name
        passw = app_man_password

         #checks if data entered is not null
        if app_man_name != None and app_man_email != None and app_man_number != None and app_man_password != None:
             #assigns a unique user id checks from database to make sure id is not already present
             flag = True
             while flag == True:
                 app_man_id = name[0:2] + passw[0:2] + \
                     str(random.randrange(1000, 9999))
                 sql_count = 'Select count(app_id) from application_manager where app_id = :app_man_id'
                 cur.execute(sql_count, [app_man_id])
                 count = cur.fetchall()
                 #print(count)

                 if(count[0][0] == 0):
                     flag = False

             #verifies if email address and mobile is unique
             sql_search = 'Select count(phone) from application_manager where phone = :app_man_number'
             cur.execute(sql_search,[app_man_number])
             count_phone = cur.fetchall()
             sql_search = 'Select count(email) from application_manager where email = :app_man_email'
             cur.execute(sql_search,[app_man_email])
             count_email = cur.fetchall()
             
             
             if count_email[0][0] == 0 and count_phone[0][0] == 0 :
                 sql_insert = """ Insert into application_manager(username,email,phone,pass,app_id) values(:app_man_name,:app_man_email,:app_man_number,:app_man_password,:app_man_id) """
                 cur.execute(sql_insert, (app_man_name, app_man_email,
                             app_man_number, app_man_password, app_man_id))
                 conn.commit()
             else:
               return fail_page()

    return render_template('/Sign_up/signup.html')


@app.route('/signin', methods=['GET', 'POST'])
def signin_page():
        
        #reads data from signup form
        
        if request.method == "POST":
          app_man_email = request.form.get('email')
          app_man_password = request.form.get("psw")
          #print(app_man_email, app_man_password)
          if app_man_email != None and app_man_password != None:

             sql_search = 'Select * from application_manager where email = :app_man_email and pass = :app_man_password'
             sql_count = 'Select count(*) from application_manager where email = :app_man_email and pass = :app_man_password'
             cur.execute(sql_search,[app_man_email, app_man_password])
             search_res = cur.fetchall()
             cur.execute(sql_count,[app_man_email, app_man_password])
             count = cur.fetchall()
             #print(search_res)
             print(count)
             #checks if email and passwords match

             if count[0][0] > 0:

                 global app_id
                 app_id = search_res[0][4]
                 print(app_id)
                 return redirect('/homepage')

             else:
                 return render_template('/Sign_in/fail.html')
                 #   exit

        return render_template('/Sign_in/signin.html')


@app.route('/homepage')
def home_page():
     print(app_id)
     return render_template('/Sign_in/index.html')


@app.route('/police')
def police_page():
    print(app_id)
    return render_template('/Sign_in/police.html')


@app.route('/ambulance')
def ambulance_page():
    print(app_id)
    return render_template('/Sign_in/amb.html')


@app.route('/firebrgd')
def firebrgd_page():
    print(app_id)
    return render_template('/Sign_in/firebrgd.html')

#function which displays solved complaints
@app.route('/solved',methods=['GET', 'POST'])
def status_solved():

      print(app_id)
      sql_search = """select * from complain where status='Suspended' or status='Fake' or status='Completed'"""
 
      cur.execute(sql_search)
      res = cur.fetchall()
      #print(type(login_id))
      #print(type(res[0][4]))
      #print(res)
      
      return render_template('/Sign_in/Solved_complains.html',records=res)


#function which displays new complaints
@app.route('/new',methods=['GET', 'POST'])
def status_new():

      print(app_id)
      sql_search = 'Select * from complain where status = :gen'
      cur.execute(sql_search,['Generating'])
      res = cur.fetchall()
      #print(type(login_id))
      #print(type(res[0][4]))
      #print(res)
      return render_template('/Sign_in/New_complains.html',records=res)

#function which displays pending complaints
@app.route('/pending',methods=['GET', 'POST'])
def status_pending():

      print(app_id)
      sql_search = """select * from complain where status <> 'Generating' and status<> 'Completed' and status<> 'Fake' and status<> 'Suspended'"""

      cur.execute(sql_search)
      res = cur.fetchall()
      #print(type(login_id))
      #print(type(res[0][4]))
      #print(res)
      return render_template('/Sign_in/inter_complains.html',records=res)

#function which displays all complaints
@app.route('/complain_log',methods=['GET', 'POST'])
def status_page():

      print(app_id)
      sql_search = 'Select * from complain'
      cur.execute(sql_search)
      res = cur.fetchall()
      #print(type(login_id))
      #print(type(res[0][4]))
      
      return render_template('/Sign_in/complain_log.html',records=res)



#function which displays complaint details
@app.route('/complain_log/<complain_id>')
def display_page(complain_id=None):
     #print(app_man_id)
     sql_search = 'Select * from complain where complain_id = :complain_id'
     cur.execute(sql_search, [complain_id])
     res = cur.fetchall()
     #print(res)
     return render_template('/Sign_in/more_detail.html',record=res[0])


#updates the complaints
@app.route('/complain_log/more_details/<complain_id>', methods=['GET', 'POST'])
def checking(complain_id):
    print("we are checking" + complain_id)
    if request.method == "POST":
       
        new_update=request.form.get('updated')
        #print(new_update)
        if new_update!= None:
            sql_search = """update complain set status=:updated where complain_id = :complainid"""
            cur.execute(sql_search,[new_update,complain_id])
            conn.commit()
            return redirect('/complain_log')
    else:
        sql_search1 = """ select * from complain inner join application_user on application_user.user_id=complain.user_id where complain.complain_id=:complainid"""
        cur.execute(sql_search1,[complain_id])
        res=cur.fetchone()
        #print(res)
        sql_search1 = "update complain SET app_id = :app_id where complain_id = :complain_id"
        cur.execute(sql_search1,[app_id,complain_id])
        conn.commit()
        return render_template("/Sign_in/Update_complain.html",record=res)
    
    
    #return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)

 
        
