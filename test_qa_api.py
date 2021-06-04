import pytest
import mock
import sqlite3
import time
from question_answer import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_health(client):
    r = client.get("/")
    assert 200 == r.status_code
    
def test_list_model_route(client):
    r = client.get("/models")
    assert 200 == r.status_code
    
def test_put_model_route(client):
    modelData = {"name": "bert-tiny",
                 "tokenizer": "mrm8488/bert-tiny-5-finetuned-squadv2",
                 "model": "mrm8488/bert-tiny-5-finetuned-squadv2"}
    r = client.put("/models", json=modelData)
    assert 200 == r.status_code

def test_del_model_route(client):
    r = client.delete("/models?model=bert-tiny")
    assert 200 == r.status_code

def test_get_models(client):
    response = client.get("/models")

    # mock_response_data = {
    #     "name": "distilled-bert",
    #     "tokenizer": "distilbert-base-uncased-distilled-squad",
    #     "model": "distilbert-base-uncased-distilled-squad"
    # }
    mock_response_data=b'[{"name":"distilled-bert","tokenizer":"distilbert-base-uncased-distilled-squad","model":"distilbert-base-uncased-distilled-squad"}]\n'
    #result = json.dumps(mock_response_data)
    response = client.get('/models')
    assert response.status_code == 200
    assert response.data == mock_response_data


def test_postAnswer(client):
    # Test /answer POST
    payload = {
        "question": "What is the capital city of Indiana?",
        "context": "Indianapolis, colloquially known as Indy, is the state capital and most-populous city of the U.S. state of Indiana and the seat of Marion County. According to 2019 estimates from the U.S. Census Bureau, the consolidated population of Indianapolis and Marion County was 886,220."
    }
    headers = {
        'Content-Type': 'application/json'
    }
    model_string = ['?model=distilled-bert', '']
    for m in model_string:
        r = client.post("/answer" + m, json=payload, headers=headers)
        assert 200 == r.status_code

if __name__ == '__main__':
    timestamp = int(time.time())
    # Connect to database
    conn = sqlite3.connect("test_db.db")
    # Create a cursor
    c = conn.cursor()
    # Create a table
    c.execute("""CREATE TABLE IF NOT EXISTS answers (
                timestamp DateTime, model varchar(100), answer varchar(500), question varchar(500), context varchar(500)
        )""")
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    print(c.fetchall())
    # commit and close
    conn.commit()
    conn.close()
