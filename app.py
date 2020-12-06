from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from send_mail import send_mail

# initialize app name
app = Flask(__name__)

# define  debug environment
ENV = "debug"

if ENV == "debug":
    # get database locally
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:1234@localhost/grab_feedback"
else:
    # get database from production heroku cloud
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://mbnvwhvamlexke:5136e126a012cd3396ea8e9c23fe5c0b15180c9bc29e64caa211212735bd052f@ec2-3-210-23-22.compute-1.amazonaws.com:5432/datququ34sfob7"
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

# set db to sqlalchemy
db = SQLAlchemy(app)

# declaring database model
class Feedback(db.Model):    
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key = True)
    customer = db.Column(db.String(200), unique = True)
    driver = db.Column(db.String(200))
    rating = db.Column(db.Integer)
    comments = db.Column(db.Text())

    def __init__(self, customer, driver, rating, comments):
        self.customer = customer
        self.driver = driver
        self.rating = rating
        self.comments = comments

# initializing route to root directory
@app.route('/')

# define function to render the index.html 
def index():
    return render_template('index.html')

# set app route to submit POST method
@app.route('/submit', methods = ['POST'])

def submit():
    if request.method == 'POST':
        customer = request.form['name']
        driver = request.form['driver']    
        rating = request.form['ratings']    
        comments = request.form['comments']
        print(customer, driver, rating, comments)

        # simple input validation
        if customer == '' or driver == '':            
            return render_template('index.html', message = "Please do not leave the required fields blank!")

        if db.session.query(Feedback).filter(Feedback.customer == customer).count() == 0:
            data = Feedback(customer, driver, rating, comments)
            db.session.add(data)
            db.session.commit()

            # sends email
            send_mail(customer, driver, rating, comments)
            return render_template('success.html')    
            print("success")            
        return render_template('index.html', message = "You already submitted a feedback!")


if __name__ == "__main__":
    # app.debug = True
    app.run()
    











