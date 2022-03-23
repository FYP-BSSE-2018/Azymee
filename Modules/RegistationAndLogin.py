from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import os
import dialogflow
from flask import Flask, request, jsonify, render_template
from google.protobuf.json_format import MessageToDict
from sklearn.tree import DecisionTreeClassifier
import  warnings
warnings.filterwarnings('ignore')
import os
from sklearn import datasets, linear_model, metrics
from sklearn.svm import SVC # "Support vector classifier

import numpy as np

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.neighbors import KNeighborsClassifier
from flask_mail import Mail, Message
from pyasn1.type.univ import Null




app = Flask(__name__)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'mariahabib2207@gmail.com'
app.config['MAIL_PASSWORD'] = 'ehebovcogyccpctc'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app) # instantiate the mail class

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'your secret key'
Flag = False
# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'azymee1'



# Intialize MySQL
mysql = MySQL(app)

############-----##################### Patient Login #####################-----##################### 

def PatientLoginx():
     # Output message if something goes wrong...
    a=False
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        session['name'] = username
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM patient WHERE P_Name = %s AND P_Password	 = %s', (username, password,))
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            #
            a=True
            
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
        return a
############-----##################### Patient Register#####################-----##################### 
def Patientregisterx():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'DOB' in request.form and 'phonenumber' in request.form and 'country' in request.form and 'BloodGroup' in request.form and 'Gender' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        session['name'] = [username]
        Gender = ['Gender']
        email = request.form['email']
        DOB = request.form['DOB']
        phonenumber = request.form['phonenumber']
        country = request.form['country']
        BloodGroup = request.form['BloodGroup']
        

        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM patient WHERE P_Name = %s', (username,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email or not DOB or not phonenumber or not country or not BloodGroup or not Gender:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO patient VALUES (NUll, %s, %s, %s,%s, %s, %s,%s,%s,NULL,NULL)',
                           (username, email, password, Gender, phonenumber, BloodGroup, DOB, country))

            mysql.connection.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    return msg


    ########-
def DoctorRegisterx():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'Gender' in request.form and 'password' in request.form and 'email' in request.form and 'phonenumber' in request.form and 'country' in request.form and 'Days' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        session['d_name'] = [username]
        Gender = request.form['Gender']
        email = request.form['email']
        Day = request.form.getlist('Days')
        Day = str(Day)
        Day = Day.replace(",", "")
        Day = Day[1:-1]
        Special = request.form['Special']
        Start_Time = request.form['Start_Time']
        End_Time = request.form['End_Time']
        phonenumber = request.form['phonenumber']
        country = request.form['country']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM doctor WHERE D_Name = %s', (username,))
        account = cursor.fetchone()
        Start_Time = Start_Time.split(":")
        Start_Time = Start_Time[0]
        End_Time = End_Time.split(":")
        End_Time = End_Time[0]
        End_Time = int(End_Time)
        Start_Time = int(Start_Time)
        hours = End_Time - Start_Time
        Slots = hours * 4
        Monday = []
        Tuesday = []
        Wednesday = []
        Thursday = []
        Friday = []
        Saturday = []
        Sunday = []
        if 'Monday' in Day:
            for i in range(Slots):
                Monday.append(0)
        Monday = str(Monday)
        Monday = Monday.replace(",", "")
        Monday = Monday[1:-1]

        if 'Tuesday' in Day:
            for i in range(Slots):
                Tuesday.append(0)
        Tuesday = str(Tuesday)
        Tuesday = Tuesday.replace(",", "")
        Tuesday = Tuesday[1:-1]

        if 'Wednesday' in Day:
            for i in range(Slots):
                Wednesday.append(0)
        Wednesday = str(Wednesday)
        Wednesday = Wednesday.replace(",", "")
        Wednesday = Wednesday[1:-1]
        if 'Thursday' in Day:
            for i in range(Slots):
                Thursday.append(0)
        Thursday = str(Thursday)
        Thursday = Thursday.replace(",", "")
        Thursday = Thursday[1:-1]

        if 'Friday' in Day:
            for i in range(Slots):
                Friday.append(0)
        Friday = str(Friday)
        Friday = Friday.replace(",", "")
        Friday = Friday[1:-1]

        if 'Saturday' in Day:
            for i in range(Slots):
                Saturday.append(0)
        Saturday = str(Saturday)
        Saturday = Saturday.replace(",", "")
        Saturday = Saturday[1:-1]

        if 'Sunday' in Day:
            for i in range(Slots):
                Sunday.append(0)
        Sunday = str(Sunday)
        Sunday = Sunday.replace(",", "")
        Sunday = Sunday[1:-1]
        Day = str(Day)
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email or not phonenumber or not country or not Start_Time or not End_Time or not Gender or not Day:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO doctor VALUES (NULL, %s, %s, %s,%s, %s,%s,%s,%s,%s,%s)',
                           (
                           username, email, password, Gender, phonenumber, country, Day, Special, Start_Time, End_Time))
            cursor.execute('INSERT INTO doctor_days VALUES (%s,%s, %s, %s,%s, %s,%s,%s)',
                           (username, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday))

            mysql.connection.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = "Please fill out the form!"
    return  msg

# ----------------------------------------------------------------------------------------------------------
############################################## Doctor Login ##############################################
from Modules import RegistationAndLogin
@app.route('/DoctortLogin', methods=['GET', 'POST'])
def DoctorLogin():
    msg = ''
    a = RegistationAndLogin.DoctorLoginx()
    if a:
        msg = "logged in"
        return redirect("DoctorProfile")
    if not a:
        msg = "Incorrect Username/ Password"

    return msg
    
############################################################################################
def  DoctorLoginx():
    a=""
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        session['d_name'] = username
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM doctor WHERE D_Name = %s AND D_Pass = %s', (username, password,))
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            a=True
        else:
            a=False
    return a

############################################################################################
def DoctorProfilex(data):
    ID=[]
    Names=[]
    Diseases=[]
    Day=[]
    Timings=[]
    Status=[]
    data = session['d_name']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM doctor WHERE D_Name= %s', (data,))
    account = cursor.fetchone()
    id=account['D_ID']
    no=cursor.execute('SELECT * FROM `appointment` WHERE `D_ID`=%s',(id,))
    appointments=cursor.fetchall()
    print(appointments)
    for i in range(no):
        a=appointments[i]['P_ID']
        Timings.append(appointments[i]['Timing'])
        cursor.execute('SELECT * FROM `patient` WHERE `P_ID`=%s',(a,))
        x=cursor.fetchone()
        Names.append(x['P_Name'])
        Day.append(appointments[i]['Day'])
        Timings.append(appointments[i]['Timing'])
        Status.append(appointments[i]['Status'])
        Diseases.append(x['P_History'])
        ID.append(appointments[i]['A_ID'])
    return  no,Names,Day,Timings,Status,Diseases,ID
#

##############################
def PatientProfilex():
    data = session['name']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM patient WHERE P_Name= %s', (data,))
    account = cursor.fetchone()
    name = account['P_Name']
    id = account['P_ID']
    email = account['P_Email']
    dob = account['P_DateOfBirth']
    phoneno = account['P_Phone']
    country = account['P_Country']
    bloodgroup = account['P_Bloodgroup']

    return  name,email,dob, phoneno, country,bloodgroup
