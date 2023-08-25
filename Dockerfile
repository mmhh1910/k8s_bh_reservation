FROM debian:stable
RUN apt-get update -y && apt-get install -y wget curl unzip libgconf-2-4  python3 python3-pip 

WORKDIR /app
RUN mkdir /data

COPY ./requirements.txt ./requirements.txt

RUN pip3 install -r requirements.txt --break-system-packages

COPY . .

CMD ["python3", "bh_reserve.py"]