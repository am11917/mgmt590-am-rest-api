# ```mgmt590-am-rest-api``` 
# Question Answering API
This API allows you to answer your questions pulling out the information from the contextual information provided as input to the API. This API uses the question and context passed in the body of the request and takes the model as a parameter. The API uses the hugging face transformers model to answer the question and the model used to answer would be dependent on the user.

V1 - Release Date - 05/27/2021
- Basic REST API deployed on cloud
- Storing question answers information in SQLite Database
- Called through Postman
- Automated deployment to cloud through Github Actions

V2 - Release Date - 06/03/2021
- Automated deployment through github actions with unit test cases to validate the routes
- Connection to persistent PostgreSQL database in Google Cloud SQL
- Web App built with Streamlit to provide UI to the REST API and communicate with end user through Web App
- Dependency on SQLite will be removed and Psycopg, Pytest has been added
- Added unit test cases file in the repo

<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary><h2 style="display: inline-block">Table of Contents</h2></summary>
  <ol>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites-and-installation">Prerequisites & Installation</a></li>
      </ul>
    </li>
    <li> <a href ="#available-routes-for-api-requests"> Available Routes for API Requests </a></li>
    <ul> <li> <a href="#models-path"> Models Path </a></li>
      <li> <a href="#answers-path"> Answers Path </a></li>
    </ul>
    <li><a href=#Build> Build API Locally </a> </li>
  </ol>
</details>


## Getting Started
The API has been deployed on cloud and it can be invoked using the URL provided and passing the required available routes or methods defined in second section. Another way to run the API and test the functionality would be to get a local image of the code and run it on your local machine which would require the installation of the dependent libraries described in the next section for successful execution of the API.

_**API URL - (Publically Available on Cloud)**_
 ```
      Base URL: https://mgmt590-am-rest-api-wbv4eowlaa-uc.a.run.app
 ```

### Prerequisites and Installation
To run this application, you'll need the following pre-requisites installed on your machine

| Library      | Version | Installation |
| ----------- | ----------- | --------- |
| Python | 3.9.1 or above  | <a href="https://www.python.org/downloads/"> Python </a> |
| Flask   | 2.0.1        | `pip install flask` |
| Transformers | 4.6.1 | `pip install transformers` |
| Psycopg2 | 2.68.6 | `pip install psycopg2-binary` |
| Docker Engine | NA | <a href="https://docs.docker.com/engine/"> Docker </a>|
| Tensor Flow | 2.5.0 | `pip install --upgrade tensorflow` |
| Pytorch | 1.8.1+cpu | `pip install torch` |
| Pytest | 6.2.2 | `pip install pytest`|

## Available Routes for API Requests
There are multiple methods/paths available that provide multiple functionality to list, add or delete transformers models. Request an answer to the questions
using the model and listing recently answered questions.

### Models Path
We are listing the available methods for all the model based handlers

| S.No.     |Allowed Methods        | Path | Description | Request Body   |Example API Call   |
|-----------|-----------|-----------|-----------|-----------|-----------|
|1.  | GET | /models| List the models available <br> for answering the question | Not Required | 1. Local Machine: http://localhost:port#/models <br><br> 2. Cloud API: Local Machine: https://<api_url>:port#/models | 

*Sample Output*
  ```
  [
{
"name": "distilled-bert",
"tokenizer": "distilbert-base-uncased-distilled-squad",
"model": "distilbert-base-uncased-distilled-squad"
},
{
"name": "deepset-roberta",
"tokenizer": "deepset/roberta-base-squad2",
"model": "deepset/roberta-base-squad2"
}
]
  ```
| S.No.     |Allowed Methods        | Path | Description | Request Body   |Example API Call   |
|-----------|-----------|-----------|-----------|-----------|-----------|
|2.  | PUT | /models| Add the model using PUT request with parameters passed as part of the body of the request | See Below | 1. Local Machine: http://localhost:port#/models <br><br> 2. Cloud API: Local Machine: https://<api_url>:port#/models | 

*Request Body*
  ```
  {
"name": "bert-tiny",
"tokenizer": "mrm8488/bert-tiny-5-finetuned-squadv2",
"model": "mrm8488/bert-tiny-5-finetuned-squadv2"
  }
  ```
 *Sample Output*
  ```
  [
{
"name": "distilled-bert",
"tokenizer": "distilbert-base-uncased-distilled-squad",
"model": "distilbert-base-uncased-distilled-squad"
},
{
"name": "deepset-roberta",
"tokenizer": "deepset/roberta-base-squad2",
"model": "deepset/roberta-base-squad2"
},
{
"name": "bert-tiny",
"tokenizer": "mrm8488/bert-tiny-5-finetuned-squadv2",
"model": "mrm8488/bert-tiny-5-finetuned-squadv2"
}
]
  ```
| S.No.     |Allowed Methods        | Path | Description | Request Body   |Example API Call   |
|-----------|-----------|-----------|-----------|-----------|-----------|
|3.  | DELETE | /models?model=<model_name>| Delete the model from the list of available models with the model name passed as the query parameter| Not Required | 1. Local Machine: http://localhost:port#/models?model=bert-tiny <br><br> 2. Cloud API: Local Machine: https://<api_url>:port#/models?model=bert-tiny |

*Sample Output*
  ```
  [
{
"name": "distilled-bert",
"tokenizer": "distilbert-base-uncased-distilled-squad",
"model": "distilbert-base-uncased-distilled-squad"
},
{
"name": "deepset-roberta",
"tokenizer": "deepset/roberta-base-squad2",
"model": "deepset/roberta-base-squad2"
}
]
```
### Answers Path
We are listing the available methods for all the answer based handlers

| S.No.     |Allowed Methods        | Path | Description | Request Body   |Example API Call   | Comments|
|-----------|-----------|-----------|-----------|-----------|-----------|-----------|
|1.  | POST | /answer?model=<model_name> | Answer the question using the context provided as part of the request body and the model passed as query parameter of the API call | See Below | 1. Local Machine: http://localhost:port#/answer?model=distilled-bert <br><br> 2. Cloud API: Local Machine: https://<api_url>:port#/answer?model=distilled-bert | ?model=<model_name> is an optional parameter and if not provided, default model would be used to answer the question. Default Model is - **Distilled Bert**

*Sample API Call*
```
http://0.0.0.0:8080/answer?model=deepset-roberta
```
*Request Body*
 ```
 {
    "question":"what is the widest highway in north america",
    "context":"King's Highway 401, commonly referred to as Highway 401 and also known by its official name as the Macdonald–Cartier Freeway or colloquially as the four-oh-one,[3] is a controlled-access400-series highway in the Canadian province of Ontario. It stretches 828.0 kilometres (514.5 mi) from Windsor in the west to the Ontario–Quebec border in the east. The part of Highway 401 that passes through Toronto is North America's busiest highway,[4][5] and one of the widest.[6][7] Together with Quebec Autoroute 20, it forms the road transportation backbone of the Quebec City–Windsor Corridor, along which over half of Canada's population resides and is also a Core Route in the National Highway System of Canada. The route is maintained by the Ministry of Transportation of Ontario (MTO) and patrolled by the Ontario Provincial Police. The speed limit is 100 km/h (62 mph) throughout its length, unless posted otherwise."
}
 ```

*Sample Output*
```
{
    "timestamp": 1622129035,
    "model": "deepset-roberta",
    "answer": "Highway 401",
    "question": "what is the widest highway in north america",
    "context": "King's Highway 401, commonly referred to as Highway 401 and also known by its official name as the Macdonald–Cartier Freeway or colloquially as the four-oh-one,[3] is a controlled-access400-series highway in the Canadian province of Ontario. It stretches 828.0 kilometres (514.5 mi) from Windsor in the west to the Ontario–Quebec border in the east. The part of Highway 401 that passes through Toronto is North America's busiest highway,[4][5] and one of the widest.[6][7] Together with Quebec Autoroute 20, it forms the road transportation backbone of the Quebec City–Windsor Corridor, along which over half of Canada's population resides and is also a Core Route in the National Highway System of Canada. The route is maintained by the Ministry of Transportation of Ontario (MTO) and patrolled by the Ontario Provincial Police. The speed limit is 100 km/h (62 mph) throughout its length, unless posted otherwise."
}
```

| S.No.     |Allowed Methods        | Path | Description | Request Body   |Example API Call   | Comments|
|-----------|-----------|-----------|-----------|-----------|-----------|-----------|
|2.  | GET | /answer?model=<model_name>&start=<start_timestamp>&end=<end_timestamp> | List the recently answered questions fetching records answered between start and end timestamp for model passed as query parameter of the API call | Not Required | 1. Local Machine: http://localhost:port#/answer?model=distilled-bert&start=1671890210&end=1689190210 <br><br> 2. Cloud API: Local Machine: https://<api_url>:port#/answer?model=distilled-bert&start=1671890210&end=1689190210 | ?model=<model_name> is an optional parameter and if not provided, answers for all models answered between start and end timestamp would be retrieved.

*Sample API Call*
```
http://0.0.0.0:8080/answer?model=deepset-roberta&start=1571890210&end=1689190210
or
http://0.0.0.0:8080/start=1571890210&end=1689190210

```
*Sample Output*
```
[
    {
        "timestamp": 1621995854,
        "model": "deepset-roberta",
        "answer": "Nick Cannon Show",
        "question": "who is the announcer on americas got talent",
        "context": "Nicholas Scott Nick Cannon (born October 8, 1980)[1] is an American rapper, actor, comedian, director, screenwriter, film producer, entrepreneur, record producer, radio and television personality. On television, Cannon began as a teenager on All That before going on to host The Nick Cannon Show, Wild 'N Out, and America's Got Talent. He acted in the films Drumline, Love Don't Cost a Thing, and Roll Bounce. As a rapper he released his debut self-titled album in 2003 with the hit single Gigolo, a collaboration with singer R. Kelly. In 2007 he played the role of the fictional footballer TJ Harper in the film Goal II: Living the Dream. In 2006, Cannon recorded the singles Dime Piece and My Wife for the planned album Stages, which was never released. Cannon married American R&B/pop singer, Mariah Carey in 2008. He filed for divorce in December 2014, after six years of marriage. The divorce was finalized in 2016."
    },
    {
        "timestamp": 1621996168,
        "model": "deepset-roberta",
        "answer": "Highway 401",
        "question": "what is the widest highway in north america",
        "context": "King's Highway 401, commonly referred to as Highway 401 and also known by its official name as the Macdonald–Cartier Freeway or colloquially as the four-oh-one,[3] is a controlled-access400-series highway in the Canadian province of Ontario. It stretches 828.0 kilometres (514.5 mi) from Windsor in the west to the Ontario–Quebec border in the east. The part of Highway 401 that passes through Toronto is North America's busiest highway,[4][5] and one of the widest.[6][7] Together with Quebec Autoroute 20, it forms the road transportation backbone of the Quebec City–Windsor Corridor, along which over half of Canada's population resides and is also a Core Route in the National Highway System of Canada. The route is maintained by the Ministry of Transportation of Ontario (MTO) and patrolled by the Ontario Provincial Police. The speed limit is 100 km/h (62 mph) throughout its length, unless posted otherwise."
 }
]
```
or
```
[
    {
        "timestamp": 1621995854,
        "model": "deepset-roberta",
        "answer": "Nick Cannon Show",
        "question": "who is the announcer on americas got talent",
        "context": "Nicholas Scott Nick Cannon (born October 8, 1980)[1] is an American rapper, actor, comedian, director, screenwriter, film producer, entrepreneur, record producer, radio and television personality. On television, Cannon began as a teenager on All That before going on to host The Nick Cannon Show, Wild 'N Out, and America's Got Talent. He acted in the films Drumline, Love Don't Cost a Thing, and Roll Bounce. As a rapper he released his debut self-titled album in 2003 with the hit single Gigolo, a collaboration with singer R. Kelly. In 2007 he played the role of the fictional footballer TJ Harper in the film Goal II: Living the Dream. In 2006, Cannon recorded the singles Dime Piece and My Wife for the planned album Stages, which was never released. Cannon married American R&B/pop singer, Mariah Carey in 2008. He filed for divorce in December 2014, after six years of marriage. The divorce was finalized in 2016."
    },
    {
        "timestamp": 1621995996,
        "model": "distilled-bert",
        "answer": "Cold Mountain Penitentiary",
        "question": "what was the prison called in the green mile",
        "context": "In 1935, Paul supervises officers Brutus Howell, Dean Stanton, Harry Terwilliger, and Percy Wetmore at Cold Mountain Penitentiary. Paul is suffering from a severe bladder infection and receives John Coffey, a physically imposing but mentally challenged black man, into his custody. John had been sentenced to death after being convicted of raping and murdering two white girls. One of the other inmates is a Native-American named Arlen Bitterbuck, who is charged with murder and is the first to be executed. Percy demonstrates a severe sadistic streak, but, as the nephew of Louisiana's First Lady, he is beyond reproach. He is particularly abusive with inmate Eduard Delacroix; he breaks Del's fingers with his baton, steps on a pet mouse named Mr. Jingles, which Del had adopted, repeatedly calls him by a gay slur, and ultimately sabotages his execution by failing to soak the sponge used to conduct electricity to Del's head; Del dies screaming in pain."
    },
    {
        "timestamp": 1621996168,
        "model": "deepset-roberta",
        "answer": "Highway 401",
        "question": "what is the widest highway in north america",
        "context": "King's Highway 401, commonly referred to as Highway 401 and also known by its official name as the Macdonald–Cartier Freeway or colloquially as the four-oh-one,[3] is a controlled-access400-series highway in the Canadian province of Ontario. It stretches 828.0 kilometres (514.5 mi) from Windsor in the west to the Ontario–Quebec border in the east. The part of Highway 401 that passes through Toronto is North America's busiest highway,[4][5] and one of the widest.[6][7] Together with Quebec Autoroute 20, it forms the road transportation backbone of the Quebec City–Windsor Corridor, along which over half of Canada's population resides and is also a Core Route in the National Highway System of Canada. The route is maintained by the Ministry of Transportation of Ontario (MTO) and patrolled by the Ontario Provincial Police. The speed limit is 100 km/h (62 mph) throughout its length, unless posted otherwise."
    }
 ]
```

## Build
There are two ways to deploy the API on your local machine:
<li> <b> Deployment with Flask: </b></li>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1. To deploy the app on your local machine through flask, we just need to run the python file

``` 
>>> python question_answer.py 
```
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2. This will deploy your app on your local machine. Post successful deployment of the code
```
 * Serving Flask app 'question_answer' (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on all addresses.
   WARNING: This is a development server. Do not use it in a production deployment.
 * Running on http://0.0.0.0:8080/ (Press CTRL+C to quit)
```
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;3. You can access the API through sending requests through Postman. (Download Postman from here - [Link](https://www.postman.com/downloads/))
*Sample Call*
```
GET http://0.0.0.0:8080/models
```
*Sample Screen*
![image](https://user-images.githubusercontent.com/69768815/119890464-df7a2d80-bf05-11eb-8066-9a0d1f9a6b52.png)

<li> <b> Container Deployment through Docker: </b> </li>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1. To deploy the app on your local machine through docker, we need a docker file ,given we already have the application file created, that
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  would be the recipe for docker to build the application </br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2. In the dockerfile, we will add the required dependency of tensorflow and pytorch to run the transformers model. </br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;3. Once the dockerfile is created, we add the dependencies to be installed in the docker image in the requirements.txt </br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;4. After you add the dependencies in requirements.txt; you'll run it when the docker container would be published and deployed </br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;5. We'll copy the application in the app folder and run the application once the docker image was deployed </br> </br>

*Sample Requirements.txt*
```
flask == 2.0.1
transformers == 4.6.1
psycopg2-binary
pytest==6.2.2
```
*Sample Dockerfile*
````
FROM tensorflow/tensorflow
FROM pytorch/pytorch

ADD requirements.txt .

RUN pip install -r requirements.txt

COPY <test_case_file>.py /app/<test_case_file>.py
COPY <app-name>.py /app/<app-name>.py

CMD ['python','/app/<aap-name>.py']

````
*Building the Docker Image in the Active Directory/Folder*
```
sudo docker build -t <image-name> . 
```

*Running the Docker Image - with ports defined for communication between local machine and docker image* 
```
sudo docker run -it -p 8080:8080 <image-name> /app/<aap-name>.py
```
