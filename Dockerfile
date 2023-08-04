FROM debian:stable

RUN apt-get update -y && apt-get install -y wget curl unzip libgconf-2-4
RUN apt-get update -y && apt-get install -y chromium xvfb python3 python3-pip 

RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

WORKDIR /app

COPY ./requirements.txt ./requirements.txt

RUN pip3 install -r requirements.txt --break-system-packages

COPY . .

ENV DISPLAY=:99
ENV DBUS_SESSION_BUS_ADDRESS=/dev/null

CMD python3 bh_reserve.py
