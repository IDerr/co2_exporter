FROM python:3.9-alpine
LABEL maintainer="IDerr <ibrahim@derraz.fr>"

WORKDIR /app

COPY . .

RUN pip3 install -r requirements.txt

EXPOSE 9143

CMD ["/app/exporter.py"]