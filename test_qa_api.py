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
    
def test_list_answers():
    questionData = {"question": "who did holly matthews play in waterloo rd?",
                    "context": "She attended the British drama school East 15 in 2005,and left after winning a high-profile role in the BBC drama Waterloo Road, playing the bully Leigh-Ann Galloway.[6] Since that role, Matthews has continued to act in BBC's Doctors, playing Connie Whitfield; in ITV's The Bill playing drug addict Josie Clarke; and she was back in the BBC soap Doctors in 2009, playing Tansy Flack."}
    headers = {'Content-Type': 'application/json'} 
    url2 = "?model=bert-tiny"
    with mock.patch('psycopg2.connect') as mocksql: 
        mocksql.connect().cursor().fetchall.return_value = [(1622203201, 'bert-tiny', 'bully Leigh-Ann Galloway',  'who did holly matthews play in waterloo rd?',  "She attended the British drama school East 15 in 2005,and left after winning a high-profile role in the BBC drama Waterloo Road, playing the bully Leigh-Ann Galloway.[6] Since that role, Matthews has continued to act in BBC's Doctors, playing Connie Whitfield; in ITV's The Bill playing drug addict Josie Clarke; and she was back in the BBC soap Doctors in 2009, playing Tansy Flack.")] 
        response = client.post(url2, headers=headers, json=questionData)
