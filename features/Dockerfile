FROM python:latest
RUN mkdir -p /usr/src/app_features
WORKDIR /usr/src/app_features
COPY . /usr/src/app_features
RUN pip install -r requirements.txt
CMD ["python","src/features.py"]