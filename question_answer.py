#importing required libraries for execution
import time
import os
import stat
import psycopg2
import datetime
from datetime import timezone
from transformers.pipelines import pipeline
from transformers import AutoModelForQuestionAnswering, AutoTokenizer
from flask import Flask
from flask import request
from flask import jsonify
import pandas as pd
from werkzeug.utils import secure_filename
from google.cloud import storage
import base64
import logging

# Create a variable that will hold our models in memory
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

#setting gcs creds for access to bucket
filecontents = os.environ.get('GCS_CREDS')
decoded_creds = base64.b64decode(filecontents)
with open('/app/creds.json', 'wb') as f:
    f.write(decoded_creds)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = '/app/creds.json'

#getting bucket details
bucket_name = os.environ.get('STORAGE_BUCKET')
storage_client = storage.Client()
bucket = storage_client.get_bucket(bucket_name)

def create_app(models, conn):
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
    
    @app.route("/upload", methods = ['POST'])
    def upload_file():
        if 'file' not in request.files:
            return('No file Provided')
        file = request.files['file']
        if file and allowed_file(file.filename):
            
            dataFrame = pd.read_csv(file)
            timestamp = int(time.time())
            fileName = 'question_context'+'_'+str(timestamp)+'.csv'
            csvFile = dataFrame.to_csv(fileName, index=False)
            response = uploadOneFile(bucket,fileName)
        return jsonify({"status":"File Uploaded Successfully","status code":200})
    
    return app


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
    cur.execute(''' select * from information_schema.tables where table_name='question_answer' ''')
    list_of_table = cur.fetchall()
    
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
    create_cmd = (''' CREATE TABLE IF NOT EXISTS question_answer (question varchar(10000),answer varchar(10000),context varchar(500000),model varchar(1000), qa_timestamp timestamp) ''')
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
    insert_cmd = ('''insert into question_answer(question,answer,context,model,qa_timestamp) values (%s,%s,%s,%s,%s)''')    
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
    list_cmd = (''' select * from question_answer where model=%s and qa_timestamp between %s and %s''')
    filters = (model,start_time_string,end_time_string)
    
    #execute the select statement and fetch all records
    cur.execute(list_cmd,filters)
    records = cur.fetchall()
    
    for row in records:
        print(row)
    
    #converting the fetched records to output in json/list of dictionaries format
    output = []
    for row in records:
        timestamp = round(row[4].replace(tzinfo=timezone.utc).timestamp())
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
    list_cmd = (''' select * from question_answer where qa_timestamp between %s and %s''')
    filters = (start_time_string,end_time_string)
    #execute the select statement and fetch all records
    cur.execute(list_cmd,filters)
    records = cur.fetchall()
    
    for row in records:
        print(row)
    #converting the fetched records to output in json/list of dictionaries format
    output = []
    for row in records:
        timestamp = round(row[4].replace(tzinfo=timezone.utc).timestamp())
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

#9. function to check the file extension
ALLOWED_EXTENSIONS = {'csv'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#10. function to upload file
def uploadOneFile(bucket,filename):
    logging.info('Inside File Uploads')
    
    try:
        blob = bucket.blob(filename)
        response = blob.upload_from_filename(filename)
        
    except Exception as ex:
        logging.error("Exception occurred while trying to upload files " , ex)
    return response

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
    if not os.path.exists('.ssl'):
        os.makedirs('.ssl')
    
    filecontents = os.environ.get('PG_SSLROOTCERT').replace("@", "=")
    with open('.ssl/server-ca.pem', 'w') as f:
        f.write(filecontents)

    filecontents = os.environ.get('PG_SSLCLIENT_CERT').replace("@", "=")
    with open('.ssl/client-cert.pem', 'w') as f:
        f.write(filecontents)

    filecontents = os.environ.get('PG_SSL_CLIENT_KEY')
    with open('.ssl/client-key.pem', 'w') as f:
        f.write(filecontents)

    os.chmod(".ssl/server-ca.pem", 0o600)
    os.chmod(".ssl/client-cert.pem", 0o600)
    os.chmod(".ssl/client-key.pem", 0o600)
    hostaddr="hostaddr={}".format(os.environ.get('PG_HOST'))
    port="port=5432"
    user="user={}".format(os.environ.get('PG_USER'))
    dbname="dbname={}".format(os.environ.get('PG_DBNAME'))
    password="password={}".format(os.environ.get('PG_USER_PASSWORD'))
    
    sslrootcert="sslrootcert=.ssl/server-ca.pem"
    sslcert="sslcert=.ssl/client-cert.pem"
    sslkey="sslkey=.ssl/client-key.pem"
    
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
    
    # connect to db
    conn = create_connection(dbconnect)
        
    #Create the flask app
    app = create_app(models, conn)
    # Run our Flask app and start listening for requests!
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)), threaded=True)
