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
        email = request.form['email']
        DOB = request.form['DOB']
        phonenumber= request.form['phonenumber']
        country=request.form['country']
        BloodGroup=request.form['BloodGroup']

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
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password,))
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            msg= 'Logged in successfully!'
            Flag=True
           
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # Show the login form with message (if any)
    return render_template('PatientLogin.html', msg=msg)
#----------------------------------------------------------------------------------------------------------

############################################## code for chat ##############################################
#----------------------------------------------------------------------------------------------------------

def detect_intent_with_parameters(project_id, session_id, query_params, language_code, user_input):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    text = user_input
    text_input = dialogflow.types.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.types.QueryInput(text=text_input)
    response = session_client.detect_intent(session=session, query_input=query_input, query_params=query_params)
    return response


@app.route('/', methods=["Post"])
def chat():
    input_text = request.form['message']

    GOOGLE_AUTHENTICATION_FILE_NAME = "azymee-maeo-ce9345a45db1.json"
    current_directory = os.path.dirname(os.path.realpath(__file__))
    path = os.path.join(current_directory, GOOGLE_AUTHENTICATION_FILE_NAME)
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = path

    GOOGLE_PROJECT_ID = "azymee-maeo"
    session_id = "783028618508"
    context_short_name = "does_not_matter"

    context_name = "projects/" + GOOGLE_PROJECT_ID + "/agent/sessions/" + session_id + "/contexts/" + context_short_name.lower()

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

    if len(result['queryResult']['fulfillmentMessages']) == 2:
        response = {"message": result['queryResult']['fulfillmentText'],
                    "payload": result['queryResult']['fulfillmentMessages'][1]['payload']}
        x= result['queryResult']['fulfillmentText']
        return jsonify(response)

    else:
        response = {"message": result['queryResult']['fulfillmentText'], "payload": None}
    # response = {"message": result['queryResult']['fulfillmentText'], "payload": None}
        return jsonify(response)
    
#----------------------------------------------------------------------------------------------------------


if __name__ == "__main__":
    app.run()

