FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY alerts_bot ./alerts_bot

CMD [ "python", "-m", "alerts_bot" ]
