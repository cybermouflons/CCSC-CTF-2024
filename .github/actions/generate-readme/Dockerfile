FROM python:3.8-slim-buster

COPY entrypoint.py /entrypoint.py
COPY README.jinja /README.jinja
COPY challenge_README.jinja /challenge_README.jinja

# Python dependencies
RUN pip install pyyaml jinja2

# File to execute when the docker container starts up (`entrypoint.sh`)
ENTRYPOINT ["python", "/entrypoint.py"]