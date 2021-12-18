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

from pyasn1.type.univ import Null


app = Flask(__name__)

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'your secret key'
Flag = False
# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'azymee1'

disease = []


################ Prediction ##############################################
# --------------------------------------------------------------------------------------------------
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


# --------------------------------------------------------------------------------------------------
# Intialize MySQL
mysql = MySQL(app)

#################################Render Chatpage ##################

@app.route("/Chatpage")
def Chatpage():
    return render_template("chat.html")


################################## Index ##################################
# --------------------------------------------------------------------------------------------------
@app.route("/")
def index():
    return render_template("index.html")


############################################## Patient Register ##############################################
# -------------------------------------------------------------------------------------------------------
@app.route('/PatientRegister', methods=['GET', 'POST'])
def Patientregister():
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
    return render_template('PatientRegister.html', msg=msg)


# ----------------------------------------------------------------------------------------------------------

############################################## Patient Login ##############################################
# -------------------------------------------------------------------------------------------------------
@app.route('/PatientLogin', methods=['GET', 'POST'])
def PatientLogin():
    # Output message if something goes wrong...
    msg = ''
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
            msg = 'Logged in successfully!'
            return redirect("PatientProfile")


        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # Show the login form with message (if any)
    return render_template("PatientLogin.html")


# ----------------------------------------------------------------------------------------------------------

############################################## User display page  #################################################
@app.route('/PatientProfile', methods=['GET', 'POST'])
def PatientProfile():
    data = session['name']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM patient WHERE P_Name= %s', (data,))
    account = cursor.fetchone()
    name = account['P_Name']
    email = account['P_Email']
    dob = account['P_DateOfBirth']
    phoneno = account['P_Phone']
    country = account['P_Country']
    bloodgroup = account['P_Bloodgroup']
    return render_template("PatientProfile.html", name=name, email=email, dob=dob, phoneno=phoneno, country=country,
                           bloodgroup=bloodgroup)


############################################## Doctor Register ##############################################
# ----------------------------------------------------------------------------------------------------------

@app.route('/DoctorRegister', methods=['GET', 'POST'])
def DoctorRegister():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'phonenumber' in request.form and 'country' in request.form and 'Day' in request.form and 'Gender' in request.form and 'Timing' in request.form and 'Special' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        session['name'] = [username]
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
            cursor.execute('INSERT INTO doctor VALUES (NUll, %s, %s, %s,%s, %s, %s,%s,%s,NULL,%s)',
                           (username, email, password, Gender, phonenumber, country,Timing,Day,Special))

            mysql.connection.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    return render_template('DoctorRegister.html', msg=msg)

# ----------------------------------------------------------------------------------------------------------
############################################## Doctor Login ##############################################
@app.route('/DoctortLogin', methods=['GET', 'POST'])
def DoctorLogin():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        session['name'] = username
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM doctor WHERE D_Name = %s AND D_Pass = %s', (username, password,))
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            msg = 'Logged in successfully!'
            return redirect("DoctorProfile.html")
           
        

        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # Show the login form with message (if any)
    return render_template("DoctorLogin.html",msg=msg)
# ----------------------------------------------------------------------------------------------------------

############################################## Doctor Profile ##############################################
@app.route('/DoctortProfile', methods=['GET', 'POST'])
def DoctorProfile():
    name = session['name']
    
    return render_template("PatientProfile.html")

############################################## Chat Code  ##############################################

## function for detecting input
def detect_intent_with_parameters(project_id, session_id, query_params, language_code, user_input):
    # making a new client session
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    # getting  user input
    text = user_input
    text_input = dialogflow.types.TextInput(text=text, language_code=language_code)
    #Represents the query input.  An event that specifies which intent to trigger.
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
        i=0
        num = machinelearning(disease)
        x = ("You are suffering from " + num[0])
        disease="Acne"
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM disease WHERE Disease_Name  = %s', (disease,))
        Name = cursor.fetchone()
        print(Name)
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

