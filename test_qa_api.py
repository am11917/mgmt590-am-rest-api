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

def test_post_wo_answer_route(client):
    questionData = {"question": "who did holly matthews play in waterloo rd?",
                    "context": "She attended the British drama school East 15 in 2005,and left after winning a high-profile role in the BBC drama Waterloo Road, playing the bully Leigh-Ann Galloway.[6] Since that role, Matthews has continued to act in BBC's Doctors, playing Connie Whitfield; in ITV's The Bill playing drug addict Josie Clarke; and she was back in the BBC soap Doctors in 2009, playing Tansy Flack."}
    r = client.post("/answer", json=questionData)
    assert 200 == r.status_code

def test_post_w_answer_route(client):
    questionData = {"question": "who did holly matthews play in waterloo rd?",
                    "context": "She attended the British drama school East 15 in 2005,and left after winning a high-profile role in the BBC drama Waterloo Road, playing the bully Leigh-Ann Galloway.[6] Since that role, Matthews has continued to act in BBC's Doctors, playing Connie Whitfield; in ITV's The Bill playing drug addict Josie Clarke; and she was back in the BBC soap Doctors in 2009, playing Tansy Flack."}
    r = client.post("/answer?model=distilled-bert", json=questionData)
    assert 200 == r.status_code
    
def test_list_answer_route_with_model(client):
    r = client.post("/answer?model=distilled-bert&start=1000000000&end=5000000000")
    assert 200 == r.status_code
 
def test_list_answer_route_without_model(client):
    r = client.post("/answer?start=1000000000&end=5000000000")
    assert 200 == r.status_code
