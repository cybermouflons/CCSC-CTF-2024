FROM python:3.10.2-alpine

RUN apk add --no-cache gcc musl-dev gmp-dev

RUN addgroup -S ctf && adduser -S ctf -G ctf
RUN mkdir /app
WORKDIR /app

COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY secret.py/ /app/
COPY server.py/ /app/

RUN chown ctf -R /app
RUN chmod a+x /app/server.py

EXPOSE 1337

USER ctf
CMD ["/app/server.py"]
