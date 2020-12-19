from flask import Flask, render_template, request, redirect
import cx_Oracle
import random

conn=cx_Oracle.connect('c##scot/tiger@//localhost:1521/orcl')
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

    if request.method == "POST":
        user_name = request.form.get('username')
        user_email = request.form.get('email')
        user_number = request.form.get('number')
        user_password = request.form.get("psw")
        #print(user_name, user_email, user_number, user_password)
        k = 0
        name = user_name
        passw = user_password

        if user_name != None and user_email != None and user_number != None and user_password != None:

             flag = True
             while flag == True:
                 user_id = name[0:2] + passw[0:2] + \
                     str(random.randrange(1000, 9999))
                 sql_search = 'Select user_id from application_user'
                 sql_count = 'Select count(user_id) from application_user'
                 cur.execute(sql_search)
                 res = cur.fetchall()
                 cur.execute(sql_count)
                 count = cur.fetchall()
              #   print(count)
                 k = 0

                 for i in range(count[0][0]):
                     if res[i][0] == user_id:
                         k = k+1
                         exit

                 if(k == 0):
                     flag = False

             k = 0
             sql_search = 'Select phone from application_user'
             sql_count = 'Select count(phone) from application_user'
             cur.execute(sql_search)
             search_phone = cur.fetchall()
             cur.execute(sql_count)
             count = cur.fetchall()
             sql_search = 'Select email from application_user'
             cur.execute(sql_search)
             search_email = cur.fetchall()
             #print(search_email)
             for i in range(count[0][0]):
               #  print(search_phone[i][0])
                 if search_email[i][0] == user_email:
                     k = k+1

                 if search_phone[i][0] == user_number:
                     k = k+1
                #     print(k)

                 if k > 0:
                     exit

             if k < 1:
                 sql_insert = """ Insert into application_user(username,email,phone,pass,user_id) values(:user_name,:useremail,:user_number,:user_password,:user_id) """
                 cur.execute(sql_insert, (user_name, user_email,
                             user_number, user_password, user_id))
                 conn.commit()
             else:
               return fail_page()

    return render_template('/Sign_up/signup.html')


@app.route('/signin', methods=['GET', 'POST'])
def signin_page():

        if request.method == "POST":
          user_email = request.form.get('email')
          user_password = request.form.get("psw")
#          print(user_email, user_password)
          if user_email != None and user_password != None:

             k = 0
             j = None
             sql_search = 'Select * from application_user '
             sql_count = 'Select count(*) from application_user'
             cur.execute(sql_search)
             search_res = cur.fetchall()
             cur.execute(sql_count)
             count = cur.fetchall()
            # print(search_res)
             #print(count)
             for i in range(count[0][0]):
                  if search_res[i][1] == user_email and search_res[i][3] == user_password:
                     k = k+1
                     j = i
                     exit
             if k > 0:

                     global login_id
                     login_id = search_res[j][4]
                     print(login_id)
                     return redirect('/homepage')

             else:
                      return render_template('/Sign_in/fail.html')
                  #   exit

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

     if request.method == "POST":
        emer_add = request.form.get('address')
        complain_type = request.form.get('complain')
        detail = request.form.get('detail')
        user_id = login_id
        app_id = None
        status = "Generating"
        complain_id = None
        print(emer_add, complain_type, detail)
        k = 0

        if complain_type != None and detail != None and emer_add != None:

             flag = True
             while flag == True:
                 complain_id = "COM" + user_id[0:2] + \
                     str(random.randrange(1000, 9999))
                 sql_search = 'Select complain_id from complain'
                 sql_count = 'Select count(complain_id) from complain'
                 cur.execute(sql_search)
                 res = cur.fetchall()
                 cur.execute(sql_count)
                 count = cur.fetchall()
                 print(count)
                 k = 0

                 for i in range(count[0][0]):
                     if res[i][0] == complain_id:
                         k = k+1
                         exit

                 if(k == 0):
                     flag = False

             sql_insert = """ Insert into complain(complain_id,status,complain_type,complain_details,user_id,app_id,address)
                              values(:complain_id, :status, :complain_type, :detail, :user_id, :app_id, :emer_add) """
             cur.execute(sql_insert, (complain_id, status,
                             complain_type, detail, user_id, app_id, emer_add))
             conn.commit()
             return render_template('/Sign_in/success.html')
   
     return render_template('/Sign_in/complain.html')


@app.route('/complain_log',methods=['GET', 'POST'])
def status_page():

      print(login_id)
      sql_search = 'Select * from complain'
      cur.execute(sql_search)
      res = cur.fetchall()
      #print(type(login_id))
     # print(type(res[0][4]))
      
      if request.method == "POST":
         complain_id = request.form.get('ab')
         print(complain_id)
      return render_template('/Sign_in/complain_log.html',records=res,verify_id=login_id)

@app.route('/complain_log/<complain_id>')
def display_page(complain_id=None):
     print(login_id)
     sql_search = 'Select * from complain'
     cur.execute(sql_search)
     res = cur.fetchall()
     for record in res:
         if record[0] == complain_id:
             result = record
     #print(type(res[0][4]))
     return render_template('/Sign_in/more_detail.html',record=result)




if __name__ == "__main__":
    app.run(debug=True)

 
        
