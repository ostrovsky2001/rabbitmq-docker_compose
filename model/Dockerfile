FROM python:latest
RUN mkdir -p /usr/src/app_model
WORKDIR /usr/src/app_model
COPY . /usr/src/app_model
RUN pip install -r requirements.txt
CMD ["python","src/model.py"]