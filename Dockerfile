FROM python:3.6.12-alpine3.12

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . . 

RUN crontab crontab

CMD ["crond", "-f"]