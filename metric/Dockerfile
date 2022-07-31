FROM python:latest
RUN mkdir -p /usr/src/app_metric
WORKDIR /usr/src/app_metric
COPY . /usr/src/app_metric
RUN pip install -r requirements.txt
CMD ["python","src/metric.py"]