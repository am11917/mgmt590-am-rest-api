# ```mgmt590-am-rest-api``` Question Answering API
This API allows you to answer your questions pulling out the information from the contextual information provided as input to the API. This API uses the question and context passed in the body of the request and takes the model as a parameter. The API uses the hugging face transformers model to answer the question and the model used to answer would be dependent on the user

<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary><h2 style="display: inline-block">Table of Contents</h2></summary>
  <ol>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites-installation">Prerequisites and Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgements">Acknowledgements</a></li>
  </ol>
</details>

## Getting Started
To get a local image of the code and running it locally on your machine

### Prerequisites and Installation
To run this application, you'll need the following pre-requisites installed on your machine

| Syntax      | Version | Installation |
| ----------- | ----------- | --------- |
| Python | 3.9.1 or above  | <a href="https://www.python.org/downloads/"> Python </a> |
| Flask   | 2.0.1        | `pip install flask` |
| Transformers | 4.6.1 | `pip install transformers` |
| SQLite | 2.6.0 | `pip install sqlite3` |
| Docker Engine | NA | <a href="https://docs.docker.com/engine/"> Docker </a>|
| Tensor Flow | 2.5.0 | `pip install --upgrade tensorflow` |
| Pytorch | 1.8.1+cpu | `pip install torch` |

