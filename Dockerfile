#syntax=docker/dockerfile:1

FROM python:3.9-slim-buster

WORKDIR /app

# COPY takes 2 parameters: param1 is for what file - param2 is for where to copy to
COPY requirements.txt requirements.txt
# installs dependencies for our application
RUN pip3 install -r requirements.txt
# copies all files from the current directory into the image

COPY src/ .

# update PATH environment variables
ENV CONSUMER_KEY='xxx'
ENV CONSUMER_SECRET_KEY='xxx'
ENV ACCESS_TOKEN='xxx'
ENV ACCESS_TOKEN_SECRET='xxx'

# run commands 
CMD ["python3", "./twitter_streaming.py"]
