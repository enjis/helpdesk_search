FROM ubuntu:18.04

RUN apt-get update && apt-get install -y python3 python3-pip build-essential python3-dev default-jre

# environment variables
ARG db_var
ENV DB_URI=$db_var
ENV SECRET_KEY=abxyz

# setup flask server
WORKDIR /usr/src/app
COPY requirements.txt .
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
COPY . .

CMD ["python3", "src/app.py"]