FROM python:3.10-bullseye

WORKDIR /painter-service

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY painter-service/ .

ENV SECRETS_PATH=/painter-service/

EXPOSE 8082

CMD [ "python", "./service.py" ]