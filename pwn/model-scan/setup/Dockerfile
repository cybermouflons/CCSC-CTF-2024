FROM ubuntu

RUN apt-get update && apt-get install -y \
    socat python3 python3-pip

RUN useradd -d /home/ctf/ -m -p ctf -s /bin/bash ctf

WORKDIR /home/ctf

ADD model_scan.py .
ADD flag.txt .
ADD add_unsafe.patch .

RUN chmod 755 ./*
RUN pip3 install picklescan==0.0.15
RUN pip3 install torch==2.2.2 torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

WORKDIR /usr/local/lib/python3.10/dist-packages/picklescan
RUN echo "from .scanner import *" >> __init__.py
RUN patch scanner.py /home/ctf/add_unsafe.patch

WORKDIR /home/ctf
EXPOSE 1337
CMD ["socat", "-v", "TCP-LISTEN:1337,reuseaddr,fork,su=ctf", "EXEC:'python3 /home/ctf/model_scan.py'"]
