# SPDX-FileCopyrightText: 2021 Pen-Yuan Hsing
# SPDX-License-Identifier: AGPL-3.0-or-later

# Container image following Heroku recommendations: 
# https://devcenter.heroku.com/articles/container-registry-and-runtime#testing-an-image-locally

FROM python:3.10-slim-bullseye

WORKDIR /opt/app

COPY ./requirements.txt /tmp/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /tmp/requirements.txt \
    && rm /tmp/requirements.txt

COPY ./ /opt/app

# Create and use a non-root user (required by Heroku)
RUN adduser --disabled-password myuser
USER myuser

CMD uvicorn main:app --host 0.0.0.0 --port $PORT