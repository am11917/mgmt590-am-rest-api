import pytest
import mock
from unittest import mock
import psycopg2
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

def test_list_model_incorrect_route(client):
    r = client.get("/model")
    assert 404 == r.status_code
    print("Incorrect Route. Please Check")
    
def test_put_model_route(client):
    modelData = {"name": "bert-tiny",
                 "tokenizer": "mrm8488/bert-tiny-5-finetuned-squadv2",
                 "model": "mrm8488/bert-tiny-5-finetuned-squadv2"}
    r = client.put("/models", json=modelData)
    #mock_response_data=b'[{"name":"distilled-bert","tokenizer":"distilbert-base-uncased-distilled-squad","model":"distilbert-base-uncased-distilled-squad"},{"name": "bert-tiny","tokenizer": "mrm8488/bert-tiny-5-finetuned-squadv2","model": "mrm8488/bert-tiny-5-finetuned-squadv2"}]\n'
    assert 200 == r.status_code
    #assert r.data == mock_response_data

def test_put_model_incorrect_route(client):
    modelData = {"name": "bert-tiny",
                 "tokenizer": "mrm8488/bert-tiny-5-finetuned-squadv2",
                 "model": "mrm8488/bert-tiny-5-finetuned-squadv2"}
    r = client.put("/model", json=modelData)
    #mock_response_data=b'[{"name":"distilled-bert","tokenizer":"distilbert-base-uncased-distilled-squad","model":"distilbert-base-uncased-distilled-squad"},{"name": "bert-tiny","tokenizer": "mrm8488/bert-tiny-5-finetuned-squadv2","model": "mrm8488/bert-tiny-5-finetuned-squadv2"}]\n'
    assert 404 == r.status_code
    #assert r.data == mock_response_data

def test_put_model_incorrect_json(client):
    modelData = {"name": "bert-tiny",
                 "model": "mrm8488/bert-tiny-5-finetuned-squadv2"}
    r = client.put("/models", json=modelData)
    #mock_response_data=b'[{"name":"distilled-bert","tokenizer":"distilbert-base-uncased-distilled-squad","model":"distilbert-base-uncased-distilled-squad"},{"name": "bert-tiny","tokenizer": "mrm8488/bert-tiny-5-finetuned-squadv2","model": "mrm8488/bert-tiny-5-finetuned-squadv2"}]\n'
    assert 200 == r.status_code
    #assert r.data == mock_response_data
    print("Missing parameter in the PUT request")
    
def test_del_model_route(client):
    r = client.delete("/models?model=bert-tiny")
    assert 200 == r.status_code

def test_get_models(client):
    mock_response_data=b'[{"name":"distilled-bert","tokenizer":"distilbert-base-uncased-distilled-squad","model":"distilbert-base-uncased-distilled-squad"}]\n'
    response = client.get('/models')
    assert response.status_code == 200
    assert response.data == mock_response_data

@mock.patch('psycopg2.connect')
def test_list_answers():
        mock_connect().__enter__().cursor().__enter__().fetchall.return_value = [(1622203201, 'bert-tiny', 'bully Leigh-Ann Galloway',  'who did holly matthews play in waterloo rd?',  "She attended the British drama school East 15 in 2005,and left after winning a high-profile role in the BBC drama Waterloo Road, playing the bully Leigh-Ann Galloway.[6] Since that role, Matthews has continued to act in BBC's Doctors, playing Connie Whitfield; in ITV's The Bill playing drug addict Josie Clarke; and she was back in the BBC soap Doctors in 2009, playing Tansy Flack.")]
        mock_connect().__enter__().cursor().__enter__().execute.assert_called_with('SELECT * FROM question_answer WHERE qa_timestamp between %s and %s', (1000000000,5000000000,))
        headers = {'Content-Type': 'application/json'}
        response = client.get("/answer?model=bert-tiny&start=1000000000&end=5000000000", headers=headers)
 
