FROM python:3.11.0a6-bullseye
ADD . /code
COPY ./requirements.txt /code/requirements.txt
WORKDIR /code
ENV PYTHONUNBUFFERED 0
RUN apt-get update
RUN apt-get install -y
RUN pip install -r requirements.txt
ENTRYPOINT [ "python" ]

CMD [ "app.py" ]
