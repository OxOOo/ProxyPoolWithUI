FROM python:3.7.0

WORKDIR /proxy
RUN pip3 install --upgrade pip
COPY ProxyPoolWithUI ProxyPoolWithUI
RUN pip3 install -r ./ProxyPoolWithUI/requirements.txt

CMD ["python", "./ProxyPoolWithUI/main.py"]
