FROM python:3.10-alpine

WORKDIR /opt/app

COPY ./requirements.txt /tmp/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /tmp/requirements.txt && \
    rm /tmp/requirements.txt

ADD ./oshminer /opt/app

# Create and use a non-root user (required by Heroku)
RUN adduser -D myuser
USER myuser

CMD uvicorn main:app --host 0.0.0.0 --port $PORT