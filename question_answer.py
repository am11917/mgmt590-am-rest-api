#importing required libraries for execution
import time
import os
import sqlite3
import psycopg2
from transformers.pipelines import pipeline
from transformers import AutoModelForQuestionAnswering, AutoTokenizer
from flask import Flask
from flask import request
from flask import jsonify


#Creating a list of dictionary of models
models = {}


# Create my flask app
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False


# Define a handler for the / path, which
# returns "Hello World"
@app.route("/")
def hello_world():
    return "<p>Hello, World! The question answering API is healthy and running</p>"


# Define a handler for the /models path, with a GET request
# to load the list of existing models
@app.route("/models", methods=['GET'])
def get_models():
    models_loaded = []
    for m in models['models']:
        models_loaded.append({
            'name': m['name'],
            'tokenizer': m['tokenizer'],
            'model': m['model']
        })

    return jsonify(models_loaded)
 
# Define a handler for the /models path, with PUT request
# to add another hugging face model to the list of existing models
@app.route("/models", methods=['PUT'])
def add_models():    
    data = request.json
    #append the new model in the existing list of models
    
    if not validate_model(data['name']):
        models_rev = []
        for m in models['models']:
            models_rev.append(m)
        models_rev.append({
        "name": data['name'],
        "tokenizer":data['tokenizer'],
        "model":data['model'],
        "pipeline":pipeline('question-answering',
            model=data['model'],
            tokenizer=data['tokenizer'])
        })
        models['models'] = models_rev
    
    models_loaded = []
    
    for m in models['models']:
        models_loaded.append({
            "name": m['name'],
            "tokenizer":m['tokenizer'],
            "model":m['model']
            })
    return jsonify(models_loaded)

# Define a handler for the /models path, with DELETE request
# to delete a hugging face model from the list of existing models
# after accepting model name to be deleted as a mandatory query parameter
@app.route("/models", methods=['DELETE'])
def delete_models():
    #check if model name has been passed as a query parameter
    if 'model' in request.args:
        if str(request.args['model']) != '':
            model_name = str(request.args['model'])
        else:
            return("Error: No Model Name Provided for Delete Method")
    else:
        return("Error: No Model Name Provided for Delete Method")
    
    if request.args.get('model') == models['default']:
        return "Can't delete default model", 400
    
    # Load the provided model
    models_rev = []
    for m in models['models']:
        if m['name'] != request.args.get('model'):
            models_rev.append(m)
    models['models'] = models_rev

    # Get the loaded models
    models_loaded = []
    for m in models['models']:
        models_loaded.append({
            'name': m['name'],
            'tokenizer': m['tokenizer'],
            'model': m['model']
        })

    return jsonify(models_loaded)


# Define a handler for the /answer path with a POST request, which
# processes a JSON payload with a question and context 
# and returns a JSON output with answer using a Hugging
# Face model along with the model name and timestamp
@app.route("/answer", methods=['POST'])
def question_answer():
    
    # Get the request body data
    data = request.json
    # Validate model name if given
    if request.args.get('model') != None:
        if not validate_model(request.args.get('model')):
            return "Model not found", 400
            
    answer, model_name = answer_question(request.args.get('model'), 
            data['question'], data['context'])
    
    # connect to db 
    conn = create_connection(dbconnect)
    
    #check if the table exists 
    #if not then create table before the first execution
    table_check = table_exists(conn)
    
    if table_check == 1 :        
        #create table if table not already existing
        create_table(conn)
        #insert your response to the table
        timestamp = insert_records(conn, data['question'],answer,data['context'],model_name)
    elif table_check == 2 :
        #insert your response to the table
        timestamp = insert_records(conn, data['question'],answer,data['context'],model_name)
    else:
        print("Error in table exist functionality. Please Check")
    
    # Create the output response body.
    out = {
            "timestamp": timestamp,
            "model": model_name,
            "answer": answer,
            "question": data['question'],
            "context": data['context']
          }

    return jsonify(out)


# Define a handler for /answer path with GET request which returns
# recently answered questions.
# Model Name is optional and Start and End timestamp are mandatory parameters
@app.route("/answer", methods=['GET'])
def list_answers():
    
    # connect to db
    conn = create_connection(dbconnect)
    # try and catch for exception handling of mandatory parameters
    try:
        start_timestamp = int(request.args['start'])
    except KeyError:
        print("Please provide start timestamp with the API call")
    # try and catch for exception handling of mandatory parameters
    try:
        end_timestamp = int(request.args['end'])
    except KeyError:
        print("Please provide end timestamp with the API call")
    
    #model is not a mandatory parameter, so handle queries accordingly with or without model parameter
    if 'model' in request.args:
        if str(request.args['model']) != '':
            model_name = str(request.args['model'])
            #if model name provided in query, call function list_records_with_model
            table_check = table_exists(conn)
            if table_check == 2 :
                output = list_records_with_model (conn, model_name, start_timestamp, end_timestamp)
                print(model_name)
            else:
                return ("Error: Table doesn't exist.Please Check")
        else:
            #if model name not provided, call function list_records_without_model
            table_check = table_exists(conn)
            if table_check == 2 :
                output = list_records_without_model (conn, start_timestamp, end_timestamp)
            else:
                return ("Error: Table doesn't exist.Please Check")
    else:
        #if model name not provided, call function list_records_without_model
        table_check = table_exists(conn)
        if table_check == 2 :
            output = list_records_without_model (conn, start_timestamp, end_timestamp)
        else:
            return ("Error: Table doesn't exist.Please Check")
    
    return output


## Common functions used for SQL operations are defined below

# 1. Create a connection to database with database file defined in main function call
def create_connection (dbconnect):
    conn = None
    try:
        conn = psycopg2.connect(dbconnect)
    except Error as e:
        print(e)
    
    return conn

# 2. Check if the table exists in the database - if not then create it
def table_exists (conn):
    cur = conn.cursor()    
    list_of_table = cur.execute(''' select * from sqlite_master where type='table' and name='question_answer' ''').fetchall()
    
    if list_of_table == [] :
        print('Table does not exist')
        return 1
    else:
        print('Table exists')
        return 2

# 3. Function to create table in SQLite Database if not exists
def create_table (conn):
    #create an sql cursor for execution of sql queries
    cur = conn.cursor()
    #create table command
    create_cmd = (''' CREATE TABLE IF NOT EXISTS question_answer (question TEXT(10000),answer TEXT(10000),context TEXT(50000,50000),model TEXT(1000), timestamp DATETIME) ''')
    #executing the command for creating table
    cur.execute(create_cmd)
    #commit the changes in database
    conn.commit()

# 4. Function to insert records in the table
def insert_records (conn, question, answer, context, model_name):
    #create an sql cursor for execution of sql queries    
    cur = conn.cursor()
    #convert unix epoch timestamp into YYYY-MM-DD HH:MM:SS format for inserting into table
    timestamp = round(time.time())
    time_struct = time.localtime(timestamp) # get struct_time
    time_string = time.strftime("%Y-%m-%d %H:%M:%S", time_struct)
    #insert command
    insert_cmd = ('''insert into question_answer(question,answer,context,model,timestamp) values (?,?,?,?,?)''')    
    qa_pair = (question,answer,context,model_name,time_string)
    #execute the insert command
    cur.execute(insert_cmd, qa_pair)
    #commit the changes in database
    conn.commit()
    #return the timestamp of insertion of record in table to show as output
    return timestamp

# 5. Function to return records if model name query parameter (optional) is passed in API request body
def list_records_with_model (conn,model,start_timestamp,end_timestamp):
    #create an sql cursor for execution of sql queries  
    cur = conn.cursor()
    #convert the start and end unix epoch timestamp into date time format for running sql queries
    start_time_struct = time.localtime(start_timestamp) # get struct_time
    start_time_string = time.strftime("%Y-%m-%d %H:%M:%S", start_time_struct)
    
    end_time_struct = time.localtime(end_timestamp) # get struct_time
    end_time_string = time.strftime("%Y-%m-%d %H:%M:%S", end_time_struct)   
    
    #select statement with model as a filter
    list_cmd = (''' select * from question_answer where model=? and timestamp between ? and ?''')
    filters = (model,start_time_string,end_time_string)
    
    #execute the select statement and fetch all records
    records = cur.execute(list_cmd,filters).fetchall()
    
    for row in records:
        print(row)
    
    #converting the fetched records to output in json/list of dictionaries format
    output = []
    for row in records:
        timestamp = round(time.mktime(time.strptime(row[4], "%Y-%m-%d %H:%M:%S")))
        output.append({"timestamp":timestamp, "model": row[3], "answer": row[1], "question":row[0],"context":row[2]})
    
    return jsonify(output)

# 6. Function to return records from sql table if model name query parameter (optional) not passed in API request body
def list_records_without_model (conn,start_timestamp,end_timestamp):
    #create an sql cursor for execution of sql queries  
    cur = conn.cursor()
    #convert the start and end unix epoch timestamp into date time format for running sql queries
    start_time_struct = time.localtime(start_timestamp) # get struct_time
    start_time_string = time.strftime("%Y-%m-%d %H:%M:%S", start_time_struct)
    
    end_time_struct = time.localtime(end_timestamp) # get struct_time
    end_time_string = time.strftime("%Y-%m-%d %H:%M:%S", end_time_struct)
    
    #select statement without model as a filter
    list_cmd = (''' select * from question_answer where timestamp between ? and ?''')
    filters = (start_time_string,end_time_string)
    #execute the select statement and fetch all records
    records = cur.execute(list_cmd,filters).fetchall()
    
    for row in records:
        print(row)
    #converting the fetched records to output in json/list of dictionaries format
    output = []
    for row in records:
        timestamp = round(time.mktime(time.strptime(row[4], "%Y-%m-%d %H:%M:%S")))
        output.append({"timestamp":timestamp, "model": row[3], "answer": row[1], "question":row[0],"context":row[2]})
    
    return jsonify(output)

# 7. Function to answer questions and reduce latency
def answer_question(model_name, question, context):
    
    # Get the right model pipeline
    if model_name == None:
        for m in models['models']:
            if m['name'] == models['default']:
                model_name = m['name']
                hg_comp = m['pipeline']
    else:
        for m in models['models']:
            if m['name'] == model_name:
                hg_comp = m['pipeline']

    # Answer the answer
    answer = hg_comp({'question': question, 'context': context})['answer']

    return answer, model_name

#8. Function to validate the model name
def validate_model(model_name):
    
    # Get the loaded models
    model_names = []
    for m in models['models']:
        model_names.append(m['name'])

    return model_name in model_names

    
# Run if running "python question_answer.py"
if __name__ == '__main__':
    
    
    
    # Initialize our default model.
    models = { 
        "default": "distilled-bert",
        "models": [
            {
                "name": "distilled-bert",
                "tokenizer": "distilbert-base-uncased-distilled-squad",
                "model": "distilbert-base-uncased-distilled-squad",
                "pipeline": pipeline('question-answering', 
                    model="distilbert-base-uncased-distilled-squad", 
                    tokenizer="distilbert-base-uncased-distilled-squad")
            }
        ]
    }
    
    #setting the database connection parameters
    sslmode="sslmode=verify-ca"
    sslrootcert="sslrootcert={}".format(os.environ.get('PG_SSLROOTCERT'))
    sslcert="sslcert={}".format(os.environ.get('PG_SSLCLIENT_CERT'))
    sslkey="sslkey={}".format(os.environ.get('PG_SSL_CLIENT_KEY'))
    hostaddr="hostaddr={}".format(os.environ.get('PG_HOST'))
    port="port=5432"
    user="user={}".format(os.environ.get('PG_USER'))
    dbname="dbname={}".format(os.environ.get('PG_DBNAME'))
    password="password={}".format(os.environ.get('PG_USER_PASSWORD'))
    
    dbconnect = " ".join([
    sslmode,
    sslrootcert,
    sslcert,
    sslkey,
    hostaddr,
    port,
    user,
    password,
    dbname
    ])
    
    # Run our Flask app and start listening for requests!
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)), threaded=True)
