FROM python:3.8

COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

WORKDIR /code
COPY . .

CMD ["uvicorn", "proj3:app", "--host", "0.0.0.0", "--port", "9000", "--reload"]