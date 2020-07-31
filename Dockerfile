FROM python:3.7-slim-buster

ENV LANG C.UTF-8
ENV GUNICORN_CMD_ARGS="--worker-tmp-dir /dev/shm --bind=0.0.0.0:8080 --workers 2 --thread 4 --worker-class gthread --log-file=-"

# add python requirements
COPY ./requirements.txt /app/requirements.txt

# set working directory
WORKDIR /app

# install python requirements
RUN pip3 install --no-cache-dir -r requirements.txt

# add app
COPY . /app

ENTRYPOINT ["gunicorn","wsgi:app"]
