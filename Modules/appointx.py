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

############## Patient app details #############
def Patient(data):
    ID=[]
    Names=[]
    Special=[]
    Diseases=[]
    Day=[]
    Timing=[]
    Status=[]
    data = session['name']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM patient WHERE P_Name= %s', (data,))
    account = cursor.fetchone()
    id=account['P_ID']

    no=cursor.execute('SELECT * FROM `appointment` WHERE `P_ID`=%s',(id,))

    appointments=cursor.fetchall()
   
    for i in range(no):
        a=appointments[i]['D_ID']
        cursor.execute('SELECT * FROM `doctor` WHERE `D_ID`=%s',(a,))
        x=cursor.fetchone()
        Names.append(x['D_Name'])
        Special.append(x['Specialization'])
        Day.append(x['D_Day'])
        Timing.append(x['D_Timing'])
        Status.append(appointments[i]['Status'])
        Diseases.append(account['P_History'])
        ID.append(appointments[i]['A_ID'])
   
    return  no,Names, Special,Day,Timing,Status,Diseases,ID

######################################################
def Rejectx(id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    status = "Active"
    cursor.execute("UPDATE `appointment` SET `Status` = %s WHERE `appointment`.`A_ID` = %s", (status, id,))
    mysql.connection.commit()
    patient = cursor.execute("SELECT * FROM `appointment` WHERE `A_ID`=%s ", (id,))
    cursor.execute("SELECT * FROM `patient` WHERE `P_ID`=%s ", (patient,))
    patientDetails = cursor.fetchone()

    msg = Message(
        'Hello ' + patientDetails['P_Name'], sender='mariahabib2207@gmail.com', recipients=[patientDetails['P_Email']])
    msg.body = "Your appointment has been cancelled"
    mail.send(msg)
    a="Appointment has been rejected"
    return  a

#################################################
def Confirmx(id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    status = "Confirmed"
    cursor.execute("UPDATE appointment SET Status =%s WHERE appointment.A_ID = %s", (status, id,))
    mysql.connection.commit()
    patient = cursor.execute("SELECT * FROM `appointment` WHERE `A_ID`=%s ", (id,))
    cursor.execute("SELECT * FROM `patient` WHERE `P_ID`=%s ", (patient,))
    patientDetails = cursor.fetchone()

    msg = Message(
        'Hello ' + patientDetails['P_Name'], sender='mariahabib2207@gmail.com',
        recipients=[patientDetails['P_Email']])
    msg.body = "Your appointment has been Confirmed"
    mail.send(msg)
    a="Appointment confirmed"
    return a

#################################################
def Deletex(id,data):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("DELETE FROM `appointment` WHERE A_ID=%s",(id,))
    mysql.connection.commit()
    cursor.execute("SELECT * FROM `patient` WHERE `P_Name`=%s ", (data,))
    patientDetails = cursor.fetchone()

    msg = Message(
        'Hello ' + patientDetails['P_Name'], sender='mariahabib2207@gmail.com', recipients=[patientDetails['P_Email']])
    msg.body = "Your appointment has been Deleted"
    mail.send(msg)
    a="Appointment has been Deleted"
    return a

#################################################
def Newx():
    d=Null
    doc=[]
    timing=[]
    specialization=[]
    day=[]
    a=-1
    no=0
    if request.method == "POST":
            a=1
            disease = request.form['Disease']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT `Doctor_Specialization` FROM `disease` WHERE `Disease_Name` = %s", (disease,))
            Specialization=cursor.fetchone()
            Specialization=Specialization['Doctor_Specialization']
            no=cursor.execute("SELECT * FROM `doctor` WHERE `Specialization`=%s", (Specialization,))
            d=cursor.fetchall()
            print(d)
            for i in range (no):
                doc.append(d[i]['D_Name'])
                timing.append(d[i]['D_Timing'])
                specialization.append(d[i]['Specialization'])
                day.append(d[i]['D_Day'])
    return doc,timing,specialization,day,a,no
    
          
      
#########################
def Selectx(doc):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    Status="Active"
    cursor.execute("SELECT * FROM `doctor` WHERE `D_name`=%s ", (doc,))
    doctor = cursor.fetchone()
    data = session['name']
    cursor.execute("SELECT `P_ID` FROM `patient` WHERE `P_Name`=%s ", (data,))
    Patient = cursor.fetchone()
    cursor.execute('INSERT INTO appointment VALUES (NULL, %s, %s, %s,%s, %s)',(Patient['P_ID'],doctor['D_ID'],doctor['D_Timing'],doctor['D_Day'],Status,))            
    mysql.connection.commit()
    a=True
    return a
      