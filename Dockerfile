FROM debian:stable 
LABEL maintainer "Sean Pianka <pianka@eml.cc>"

## For chromedriver installation: curl/wget/libgconf/unzip
RUN apt-get update -y && apt-get install -y wget curl unzip libgconf-2-4
## For project usage: python3/python3-pip/chromium/xvfb
RUN apt-get update -y && apt-get install -y chromium xvfb python3 python3-pip 


# Download, unzip, and install chromedriver
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/


WORKDIR /app

# Copy the source code into the container.
COPY ./requirements.txt ./requirements.txt

RUN pip3 install -r requirements.txt --break-system-packages


ENV DISPLAY=:99
ENV DBUS_SESSION_BUS_ADDRESS=/dev/null


COPY . .
# Run the application.
CMD python3 bh_reserve.py
