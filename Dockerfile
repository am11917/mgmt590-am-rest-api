FROM tensorflow/tensorflow

FROM pytorch/pytorch

COPY requirements.txt . 

RUN pip install -r requirements.txt 

COPY question_answer.py /app/question_answer.py

CMD ["python3", "/app/question_answer.py"]
