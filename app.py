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


################################---- Prediction ----################################
def machinelearning(disease):
    ##Reading data set and seperating independent and dependent variables
    data = pd.read_csv("Testing.csv")
    df = pd.DataFrame(data)
    cols = df.columns
    cols = cols[:-1]
    x = df[cols]
    y = df['prognosis']
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.33, random_state=42)
    # Decision Tree ....Calling Classifier and Fitting data for training
    dt = DecisionTreeClassifier()
    dt.fit(x_train, y_train)
    ## SVM
    classifier = SVC(kernel='linear', random_state=0)
    classifier.fit(x_train, y_train)
    # Random Forest
    rf = RandomForestClassifier(n_estimators=100, criterion='gini', max_depth=6,
                                max_features='auto', random_state=0)
    rf.fit(x_train, y_train)
    # knn
    knnclf = KNeighborsClassifier()
    # Fitting K-NN to the Training set
    knnClassifier = KNeighborsClassifier(n_neighbors=2)
    knnClassifier.fit(x_train, y_train)
    # To create a dictionary from two sequences, use the dict() and zip() so it creates dictionary of symptoms and indices
    indices = [i for i in range(132)]
    symptoms = df.columns.values[:-1]
    dictionary = dict(zip(symptoms, indices))

    # Functions

    def dosomething(symptom):
        # Getting values from user input
        user_input_symptoms = symptom
        user_input_label = [0 for i in range(132)]
        for i in user_input_symptoms:
            idx = dictionary[i]
            user_input_label[idx] = 1
        # Creating np array
        user_input_label = np.array(user_input_label)
        # Changing 1D array to 2D array
        user_input_label = user_input_label.reshape((-1, 1)).transpose()

        # Predicting values
        DecisionTree = dt.predict(user_input_label)

        RandomForest = rf.predict(user_input_label)

        y_pred = knnClassifier.predict(user_input_label)

        SVM = classifier.predict(user_input_label)
        return (DecisionTree, RandomForest, y_pred, SVM)

    ### Predicting Diseases
    prediction = (dosomething(disease))
    print("DecisionTree : ", prediction[0])
    print("Random Forest : ", prediction[1])
    print("KNN : ", prediction[2])

    print("SVM: ", prediction[3])

    def most_frequent(prediction):
        counter = 0
        num = prediction[0]

        for i in prediction:
            curr_frequency = prediction.count(i)
            if (curr_frequency > counter):
                counter = curr_frequency
                num = i

        return num

    num = most_frequent(prediction)
    return num


################################----Render Chatpage ----################################

@app.route("/Chatpage")
def Chatpage():
    return render_template("chat.html")


################################---- Index ----################################
@app.route("/")
def index():
    return render_template("index.html")


################################---- Patient Register ----################################
@app.route('/PatientRegister', methods=['GET', 'POST'])
def Patientregister():
    msg = RegistationAndLogin.Patientregisterx()
    return render_template('PatientRegister.html', msg=msg)


################################---- Patient Login ----################################

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


##############################################---- User display page ---- #################################################
@app.route('/PatientProfile', methods=['GET', 'POST'])
def PatientProfile():
    data = session['name']
    name,email,dob, phoneno, country,bloodgroup=RegistationAndLogin.PatientProfilex()
    return render_template("PatientProfile.html", name=name, email=email, dob=dob, phoneno=phoneno, country=country,
                           bloodgroup=bloodgroup)


###################################---User display page --- #########################################
@app.route('/P_App', methods=['GET', 'POST'])
def P_App():
  
    data = session['name']
    no,Names, Special,Day,Timing,Status,Diseases,ID=appointx.Patient(data)
    return render_template("PatientAppointments.html",no=no,Names=Names, Special=Special,Day=Day,Timing=Timing,Status=Status,Diseases=Diseases,ID=ID)


###################################---User display page --- #########################################
@app.route('/DoctorRegister', methods=['GET', 'POST'])
def DoctorRegister():
   # msg = ''
    msg = RegistationAndLogin.DoctorRegisterx()
    return render_template('DoctorRegister.html', msg=msg)


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

    return render_template("DoctorLogin.html", msg=msg)

############################################## Doctor Profile ##############################################
# ----------------------------------------------------------------------------------------------------------

@app.route('/DoctorProfile', methods=['GET', 'POST'])
def DoctorProfile():
    name = session['d_name']
    appointments, lis, no=RegistationAndLogin.DoctorProfilex(name)
    if no==0:
        return "You dont have any appointments"
    else:
        return render_template("DoctorProfile.html", appointments=appointments, lis=lis, no=no)
######################################################################################
@app.route("/Reject/<int:id>")
def Reject(id):
    a=appointx.Rejectx(id)
    return redirect('/DoctorProfile')

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
    
          
    
@app.route('/New', methods=['GET', 'POST'])
def New():

    doc,timing,specialization,day,a,no=appointx.Newx()       
    return render_template ('New.html',doc=doc,timing=timing,specialization=specialization,day=day,a=a,no=no)
    
          
@app.route("/Select/<doc>")
def Select(doc):
    a=appointx.Selectx(doc)
    flash("Your appointment has been added")
    return redirect("/P_App")
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


@app.route('/chat', methods=["Post"])
def chat():
    ## Empty list for disease
    disease = []
    # get input message from form
    input_text = request.form['message']

    # Google Authentication
    GOOGLE_AUTHENTICATION_FILE_NAME = "azymee-aeuj-070e0a104a03.json"
    current_directory = os.path.dirname(os.path.realpath(__file__))
    path = os.path.join(current_directory, GOOGLE_AUTHENTICATION_FILE_NAME)
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = path
    GOOGLE_PROJECT_ID = "azymee-aeuj"
    session_id = "83874360073"
    context_short_name = "does_not_matter"
    context_name = "projects/" + GOOGLE_PROJECT_ID + "/agent/sessions/" + session_id + "/contexts/" + context_short_name.lower()

    # Generated protocol buffer code.
    # https://googleapis.dev/python/protobuf/latest/google/protobuf/struct_pb2.html
    parameters = dialogflow.types.struct_pb2.Struct()
    context_1 = dialogflow.types.context_pb2.Context(
        name=context_name,
        lifespan_count=2,
        parameters=parameters
    )

    query_params_1 = {"contexts": [context_1]}

    language_code = 'en'

    response = detect_intent_with_parameters(
        project_id=GOOGLE_PROJECT_ID,
        session_id=session_id,
        query_params=query_params_1,
        language_code=language_code,
        user_input=input_text
    )
    result = MessageToDict(response)

    if result['queryResult']['intent']['displayName'] == "Stop-Symptoms":
        i = 0
        num = machinelearning(disease)
        x = ("You are suffering from " + num[0])
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM disease WHERE Disease_Name  = %s', (disease,))
        response = {"message": x}


    elif 'symptoms' in result['queryResult']['parameters']:
        disease.append(result['queryResult']['parameters']['symptoms'])
        response = {"message": result['queryResult']['fulfillmentText'], "payload": None}



    else:
        response = {"message": result['queryResult']['fulfillmentText'], "payload": None}

    # response =
    return jsonify(response)


if __name__ == "__main__":
    app.run()
