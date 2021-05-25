FROM tensorflow/tensorflow

COPY requirements.txt . 

RUN pip install -r requirements.txt 

COPY answers.py /app/answers.py

CMD ["python3", "/app/answers.py"]
