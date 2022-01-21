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
    msg=''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'phonenumber' in request.form and 'country' in request.form and 'Day' in request.form and 'Gender' in request.form and 'Timing' in request.form and 'Special' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        session['d_name'] = [username]
        Gender = ['Gender']
        email = request.form['email']
        Special=request.form['Special']
       
        phonenumber = request.form['phonenumber']
        country = request.form['country']
        Timing=request.form['Timing']
        Day=request.form['Day']
       

        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM doctor WHERE D_Name = %s', (username,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email or not phonenumber or not country or not Timing or not Gender or not Day:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO doctor VALUES (NULL, %s, %s, %s,%s, %s, %s,%s,%s,%s,NULL)',
                           (username, email, password, Gender, phonenumber, country,Timing,Day,Special))

            mysql.connection.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = "Please fill out the form!"
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
def DoctorProfilex(name):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT D_ID FROM doctor WHERE D_Name= %s', (name,))
    D_ID = cursor.fetchone()
    D_ID = D_ID['D_ID']
    no = cursor.execute('SELECT * FROM `appointment` WHERE `D_ID`=%s', (D_ID,))
    if no == 0:
        return "You don't have any appointments"
    else:
        appointments = cursor.fetchall()
        lis = []
        for i in range(no):
            x = appointments[i]['P_ID']
            no = cursor.execute('SELECT * FROM `patient` WHERE `P_ID`=%s', (x,))
            a = cursor.fetchone()
            lis.append(a)

        return  appointments,lis,no

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
