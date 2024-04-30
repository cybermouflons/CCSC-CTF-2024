FROM debian:12

RUN apt-get update && apt-get install -y \
    socat python3 python3-pip

RUN useradd -d /home/ctf/ -m -p ctf -s /bin/bash ctf

WORKDIR /home/ctf

ADD armored_up.py .
ADD secret.py .

RUN chmod 755 ./*

WORKDIR /home/ctf
EXPOSE 1337
CMD ["socat", "-v", "TCP-LISTEN:1337,reuseaddr,fork,su=ctf", "EXEC:'python3 /home/ctf/armored_up.py'"]
