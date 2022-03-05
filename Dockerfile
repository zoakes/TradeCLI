FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

## Consider parsing env vars for the various IP, PW, USER of SQL ?

#ENV PASSWORD = '<test_password>' #DONT use, replace this check.
#ENV SQL_IP = '' #DONT use... replace this check (hard to remember)

#ENV SQL_USER = '' #Solely rely on this
#ENV SQL_PASSWORD = '' #and THIS ?

CMD ["python3","main.py"]

# BUILD with docker build --tag trade-cli
# RUN with docker run -t -i trade-cli
# OR (Focus solely on ip, password (of SQL!))
# RUN w envs: docker run -i -t -e SQL_IP='sqlip' -e SQL_PASSWORD='sqlpw' trade-cli

#OR .env file...3
# docker run --env-file ./envfilename -i -t trade-cli