FROM python:3

WORKDIR /usr/src/app

COPY . .

EXPOSE 8000

RUN chmod +x ./run.sh
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

CMD [ "./run.sh" ]