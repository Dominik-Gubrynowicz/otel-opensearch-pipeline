FROM python:3.12

RUN mkdir -p /opt/sensor-mock
WORKDIR /opt/sensor-mock

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "app.py" ]