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
def  chatx():
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