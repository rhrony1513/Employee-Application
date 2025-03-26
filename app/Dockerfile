FROM ubuntu:20.04
RUN apt-get update -y && apt-get upgrade -y
COPY . /app
WORKDIR /app
RUN set -xe \
    && apt-get install -y python3-pip \
    mysql-client \
    netcat \
    iputils-ping
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
EXPOSE 81
ENTRYPOINT [ "python3" ]
CMD [ "app.py" ]