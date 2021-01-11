# Install Python dependencies
FROM python:3.8 as build-python

COPY . /app/icely-annotator/
COPY ./requirements.txt /app/icely-annotator/
WORKDIR /app/icely-annotator
RUN pip install -r requirements.txt

# RUN python standalone.py

EXPOSE 8001
ENV PORT 8001
ENV PYTHONUNBUFFERED 1
ENV PROCESSES 4