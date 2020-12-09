from flask import Flask,render_template

app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template('/home/adilasif/Repos/Emergency Services/User/Front-End/Home/index.html')

if __name__ =="__main__":
    app.run(debug=True)