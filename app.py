import datetime

from pydoc import doc
from tokenize import Special
from flask import Flask, render_template, request, redirect, url_for, session,flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
import dialogflow
from flask import Flask, request, jsonify, render_template
from google.protobuf.json_format import MessageToDict
from sklearn.tree import DecisionTreeClassifier
import warnings
import re
from sqlalchemy import String
warnings.filterwarnings('ignore')
import os
from sklearn import datasets, linear_model, metrics
from sklearn.svm import SVC  # "Support vector classifier
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.neighbors import KNeighborsClassifier
from flask_mail import Mail, Message
from pyasn1.type.univ import Null
from Modules import RegistationAndLogin
from Modules import appointx
app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'mariahabib2207@gmail.com'
app.config['MAIL_PASSWORD'] = 'ehebovcogyccpctc'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)  # instantiate the mail class

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
disease = []



################################---- Index and Contact Page  ----################################
# ----------------------------------------------------------------------------------------------------------

@app.route("/")
def index():
    return render_template("index.html")
@app.route("/contact")
def contact():
    return render_template("contact.html")
@app.route("/LoginRegister")
def loginRegister():
    return render_template("loginRegister.html")


################################----Render Chatpage ----################################
# ----------------------------------------------------------------------------------------------------------

@app.route("/Chatpage")
def Chatpage():
    return render_template("chat.html")


################################---- Patient Register And Login ----################################
# ----------------------------------------------------------------------------------------------------------

@app.route('/PatientRegister', methods=['GET', 'POST'])
def Patientregister():
    msg = RegistationAndLogin.Patientregisterx()
    return render_template('PatientRegister.html', msg=msg)


@app.route('/PatientLogin', methods=['GET', 'POST'])
def PatientLogin():
    msg = ''
    a = RegistationAndLogin.PatientLoginx()
    if a == True:
        msg = 'Logged in successfully!'
        return redirect("PatientProfile")
    if a == False:
        msg = 'Incorrect username/password!'

    return render_template("PatientLogin.html", msg=msg)


################################----  Doctor Register And Login ----################################
# ----------------------------------------------------------------------------------------------------------


@app.route('/DoctorLogin', methods=['GET', 'POST'])
def DoctorLogin():
    msg = ''
    a = RegistationAndLogin.DoctorLoginx()
    if a == True:
        msg = 'Logged in successfully!'
        return redirect("DoctorProfile")
    if a == False:
        msg = 'Incorrect username/password!'

    return render_template("DoctorLogin.html", msg=msg)

@app.route('/DoctorRegister', methods=['GET', 'POST'])
def DoctorRegister():
    msg = ''
    msg = RegistationAndLogin.DoctorRegisterx()
    return render_template("DoctorRegister.html", msg=msg)


##############################################---- User display page ---- #################################################
# ----------------------------------------------------------------------------------------------------------

@app.route('/PatientProfile', methods=['GET', 'POST'])
def PatientProfile():
    data = session['name']
    name,email,dob, phoneno, country,bloodgroup=RegistationAndLogin.PatientProfilex()
    return render_template("PatientProfile.html", name=name, email=email, dob=dob, phoneno=phoneno, country=country,
                           bloodgroup=bloodgroup)


###################################---User Appointment page --- #########################################
# ----------------------------------------------------------------------------------------------------------
@app.route('/P_App', methods=['GET', 'POST'])
def P_App():
    data=session['name']
    no,Names, Special,Day,Timing,Status,Diseases,ID= appointx.Patient(data)
    return render_template('PatientAppointments.html',no=no,Names=Names, Special=Special,Day=Day,Timing=Timing,Status=Status,Diseases=Diseases,ID=ID)
  
   


############################################## Doctor Profile ##############################################
# ----------------------------------------------------------------------------------------------------------

@app.route('/DoctorProfile', methods=['GET', 'POST'])
def DoctorProfile():
    data=session['d_name']
    no,Names,Day,Timings,Status,Diseases,ID=RegistationAndLogin.DoctorProfilex(data)
    return render_template('DoctorProfile.html',no=no,Names=Names,Day=Day,Timing=Timings,Status=Status,Diseases=Diseases,ID=ID)

############################################## Appointments Actions ##############################################
# ----------------------------------------------------------------------------------------------------------


@app.route("/Confirm/<int:id>")
def Confirm(id):
    a=appointx.Confirmx(id)
    return redirect('/DoctorProfile')


@app.route("/Delete/<int:id>")
def Delete(id):
    data = session['name']
    a=appointx.Deletex(id,data)
    flash('Appointment Deleted')
    return redirect("/P_App")

############################################## Add new Appointments ##############################################
# ----------------------------------------------------------------------------------------------------------

@app.route('/New', methods=['GET','POST'])
def New():
    no ,d,a,x=appointx.Newx()
    return render_template('NewAppointment.html' ,no=no ,d=d,a=a,x=x)

@app.route('/SelectSlot/<value>' )
def SelectSlot(value):
    Doctor=session['Selected_Doctor']
    Day=session["Selected_Day"]
    data = session['name']
    a=appointx.SelectSlotx(Doctor,Day,data,value)
    flash('You appointment has been shared with doctor')
    return render_template("Thankyou.html")
  

@app.route('/SelectDay/<value>' )
def SelectDay(value):
    session['log'] = 1
    Log = session['log']
    Day,Doctor_Detail,no=appointx.SelectDayx(Log,value)
    
    return render_template('New_Stage2.html', Day=Day,Doctor_Detail=Doctor_Detail,no=no)
###############################################################################
      


      

            

 

            

   
    
    
# ----------------------------------------------------------------------------------------------------------

############################################## Chat Code  ##############################################

## function for detecting input
def detect_intent_with_parameters(project_id, session_id, query_params, language_code, user_input):
    # making a new client session
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    # getting  user input
    text = user_input
    text_input = dialogflow.types.TextInput(text=text, language_code=language_code)
    # Represents the query input.  An event that specifies which intent to trigger.
    query_input = dialogflow.types.QueryInput(text=text_input)
    # Detect response with parameters
    response = session_client.detect_intent(session=session, query_input=query_input, query_params=query_params)
    return response




if __name__ == "__main__":
    app.run()
