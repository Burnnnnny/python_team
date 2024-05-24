FROM python:3.10-slim

WORKDIR /app

COPY ./app /app

RUN  pip install -r requirements.txt

EXPOSE 30000

CMD [ "python3","app.py" ]