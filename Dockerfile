FROM python:3.7.0

WORKDIR /proxy

ADD . /proxy
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

CMD ["python", "main.py"]
