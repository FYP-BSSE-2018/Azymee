from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import datetime

import os
import dialogflow
from flask import Flask, request, jsonify, render_template,flash
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
    Timings=[]
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
        Timings.append(appointments[i]['Timing'])
        cursor.execute('SELECT * FROM `doctor` WHERE `D_ID`=%s',(a,))
        x=cursor.fetchone()
        Names.append(x['D_Name'])
        Special.append(x['Specialization'])
        Day.append(appointments[i]['Day'])
        Status.append(appointments[i]['Status'])
        Diseases.append(account['P_History'])
        ID.append(appointments[i]['A_ID'])
    return  no,Names, Special,Day,Timings,Status,Diseases,ID

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
    a=-1
    x=1
    no=0
    d=0
    if request.method == "POST":
        disease = request.form['Disease']
        a=0
        print(disease)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT `Doctor_Specialization` FROM `disease` WHERE `Disease_Name` = %s", (disease,))
        Specialization = cursor.fetchone()
        if Specialization==None:
            x=0
        else:
            Specialization = Specialization['Doctor_Specialization']
            no = cursor.execute("SELECT * FROM `doctor` WHERE `Specialization`=%s", (Specialization,))
            d = cursor.fetchall()  # d = Doctor Details
    return no ,d,a,x
    
          
      
#########################
def SelectSlotx(Doctor,Day,data,value):
    min=1
    hours=0
    value=int(value)+1
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
  
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    no= cursor.execute("SELECT * FROM `doctor_days` WHERE `D_Name`=%s", (Doctor,))
    days = cursor.fetchone()
    column=str(Day)
    Day=days[str(Day)]
    nc="1"
    tmp = list(Day)
    tmp[value] = nc
    Day = "".join(tmp)
    cursor.execute(f"UPDATE doctor_days  SET {column} =%s WHERE D_Name = %s", (Day,Doctor,))
    mysql.connection.commit()
    flash('You appointment has been shared with doctor ')
    Status="Active"
    cursor.execute("SELECT * FROM `doctor` WHERE `D_name`=%s ", (Doctor,))
    doctor = cursor.fetchone()
    hours=int(doctor['Start_Time'])
    min=15*(value-1)
   

    SelectedDay=session["Selected_Day"]

    min=15*(value-1)
    if min>60:
     while min>60:
        hours=hours+1
        min=min-60
    seconds=0
  
    ime=datetime.time(hours, min, seconds)
    str(ime)
    flash('You appointment has been shared with doctor')
   
    cursor.execute("SELECT `P_ID` FROM `patient` WHERE `P_Name`=%s ", (data,))
    Patient = cursor.fetchone()
    cursor.execute('INSERT INTO appointment VALUES (NULL, %s, %s, %s,%s, %s)',(Patient['P_ID'],doctor['D_ID'],ime,SelectedDay,Status,))            
    mysql.connection.commit()
    a=True
    return a
   
   
def SelectDayx(Log,value):
    a=value
    a=a.split(":")
    Day=a[0]
    
    Doctor=a[1]
    session["Selected_Day"]=Day
    session['Selected_Doctor']=Doctor
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    no= cursor.execute("SELECT * FROM `doctor_days` WHERE `D_Name`=%s", (Doctor,))
    days = cursor.fetchone()
    Day=days[str(Day)]
    Day=str(Day.replace(" ", ''))
    Day=list(Day)
    no=len(Day)
    no=int(no/2)
    cursor.execute("SELECT * FROM `doctor` WHERE `D_Name`=%s", (Doctor,))
    Doctor_Detail=cursor.fetchone()
    return Day,Doctor_Detail,no