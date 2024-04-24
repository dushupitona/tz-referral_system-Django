FROM python:3.12-alpine

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

COPY anyproj / app/
WORKDIR /app
EXPOSE 8000


RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt