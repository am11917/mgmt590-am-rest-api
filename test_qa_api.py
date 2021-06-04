import pytest
import mock
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
