import pytest
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

def test_get_models():
    response = app.test_client().get('/models')

    # mock_response_data = {
    #     "name": "distilled-bert",
    #     "tokenizer": "distilbert-base-uncased-distilled-squad",
    #     "model": "distilbert-base-uncased-distilled-squad"
    # }
    mock_response_data=b'[{"name":"distilled-bert","tokenizer":"distilbert-base-uncased-distilled-squad","model":"distilbert-base-uncased-distilled-squad"}]\n'
    #result = json.dumps(mock_response_data)
    response = app.test_client().get('/models')
    assert response.status_code == 200
    assert response.data == mock_response_data
