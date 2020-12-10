from flask import Flask,render_template

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

@app.route('/signup')
def signup_page():
    return render_template('/Sign_up/signup.html')


@app.route('/signin')
def signin_page():
    return render_template('/Sign_in/signin.html')



if __name__ =="__main__":
    app.run(debug=True)