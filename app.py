from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import os
import dialogflow
from flask import Flask, request, jsonify, render_template
from google.protobuf.json_format import MessageToDict
app = Flask(__name__)

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'your secret key'
Flag=False
# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'zxc'


################Patient Variable##############################################
#--------------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------
# Intialize MySQL
mysql = MySQL(app)


################################## Index ##################################
#--------------------------------------------------------------------------------------------------
@app.route("/")
def index():
        return render_template("index.html")

############################################## Patient Register ##############################################
#-------------------------------------------------------------------------------------------------------
@app.route('/PatientRegister', methods=['GET', 'POST'])
def Patientregister():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'DOB' in request.form  and 'phonenumber' in request.form and 'country' in request.form and 'BloodGroup' in request.form :
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        session['name']=[username]

        email = request.form['email']
        DOB = request.form['DOB']
        phonenumber= request.form['phonenumber']
        country=request.form['country']
        BloodGroup=request.form['BloodGroup']
        Patient=[username,email,DOB,phonenumber,country,BloodGroup]
       

        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email or not DOB or not phonenumber or not country or not BloodGroup:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO accounts VALUES ( %s, %s, %s,%s, %s, %s,%s)', (username, password, email, DOB , phonenumber, country ,BloodGroup))

            mysql.connection.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    return render_template('PatientRegister.html', msg=msg)
#----------------------------------------------------------------------------------------------------------

############################################## Patient Login ##############################################
#-------------------------------------------------------------------------------------------------------
@app.route('/PatientLogin', methods=['GET', 'POST'])
def PatientLogin():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        session['name']=username
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password,))
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            msg= 'Logged in successfully!'
            return redirect("PatientProfile")
            Flag=True
           
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # Show the login form with message (if any)
    return render_template("PatientLogin.html")
  
#----------------------------------------------------------------------------------------------------------

############################################## Patient Login #################################################
@app.route('/PatientProfile', methods=['GET', 'POST'])
def PatientProfile():
    data=session['name']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM accounts WHERE username = %s', (data,))
    account = cursor.fetchone()
    name=account['username']
    email=account['email']
    dob=account['dob']
    phoneno=account['phoneno']
    country=account['country']
    bloodgroup=account['bloodgroup']
    return render_template("PatientProfile.html",name=name,email=email,dob=dob,phoneno=phoneno,country=country,bloodgroup=bloodgroup)

############################################## User display page ##############################################
#----------------------------------------------------------------------------------------------------------


#----------------------------------------------------------------------------------------------------------


if __name__ == "__main__":
    app.run()

