FROM python:3.9-alpine

RUN mkdir /app
COPY ["app.sh", "*.py", "*.txt", "/app"]

EXPOSE 5000

WORKDIR /app

CMD	["/bin/sh", "-x", "app.sh"]