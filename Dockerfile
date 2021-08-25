# FROM python:3.9-slim

# RUN pip install pipenv

# ENV SRC_DIR /usr/local/src/containers-first-steps

# WORKDIR ${SRC_DIR}

# COPY Pipfile Pipfile.lock ${SRC_DIR}/

# RUN pipenv install --system --clear

# COPY ./ ${SRC_DIR}/

# WORKDIR ${SRC_DIR}/src/webapp

# CMD ["flask", "run", "-h", "0.0.0.0"]

#FROM python:slim-buster
FROM flaskbase:latest
COPY . /app
WORKDIR /app
#RUN python -m pip install --upgrade pip
#RUN apt-get -y update && apt-get -y install python3-dev default-libmysqlclient-dev build-essential
RUN pip install -r requirements.txt
RUN pip install gunicorn
#RUN gunicorn -w 2 -b 0.0.0.0:5000 app:app
# RUN apk add mysql-client
#RUN pip3 install mysqlclient
EXPOSE 5000
#CMD flask run --host=0.0.0.0
CMD ["gunicorn" , "-w", "2", "-b", "0.0.0.0:5000", "app:app"]

# CMD ["nginx", "-g", "daemon off;"]