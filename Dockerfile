FROM python:3.6.8
MAINTAINER "fapriyanto@alterra.id"
RUN mkdir -p /coffeology_flask
COPY . /coffeology_flask
RUN pip install -r /coffeology_flask/requirements.txt
WORKDIR /coffeology_flask
ENTRYPOINT ["python"]
CMD ["app.py"]
