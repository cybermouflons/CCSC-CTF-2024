FROM python:3.10-alpine

RUN apk update
RUN apk add socat gcc libc-dev libffi-dev

WORKDIR /chall

COPY . .

RUN pip install poetry
RUN poetry install

EXPOSE 13373

CMD ["socat", "-T60", "TCP-LISTEN:13373,reuseaddr,fork,su=root", "EXEC:python3 challenge.py"]