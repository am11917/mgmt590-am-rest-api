# ```mgmt590-am-rest-api``` Question Answering API
This API allows you to answer your questions pulling out the information from the contextual information provided as input to the API. This API uses the question and context passed in the body of the request and takes the model as a parameter. The API uses the hugging face transformers model to answer the question and the model used to answer would be dependent on the user

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
      <li> <a href="answers-path"> Answers Path </a></li>
    </ul>
  </ol>
</details>

## Getting Started
To get a local image of the code and running it locally on your machine

### Prerequisites and Installation
To run this application, you'll need the following pre-requisites installed on your machine

| Library      | Version | Installation |
| ----------- | ----------- | --------- |
| Python | 3.9.1 or above  | <a href="https://www.python.org/downloads/"> Python </a> |
| Flask   | 2.0.1        | `pip install flask` |
| Transformers | 4.6.1 | `pip install transformers` |
| SQLite | 2.6.0 | `pip install sqlite3` |
| Docker Engine | NA | <a href="https://docs.docker.com/engine/"> Docker </a>|
| Tensor Flow | 2.5.0 | `pip install --upgrade tensorflow` |
| Pytorch | 1.8.1+cpu | `pip install torch` |

## Available Routes for API Requests
There are multiple methods/paths available that provide multiple functionality to list, add or delete transformers models. Request an answer to the questions
using the model and listing recently answered questions.

### Models Path

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
