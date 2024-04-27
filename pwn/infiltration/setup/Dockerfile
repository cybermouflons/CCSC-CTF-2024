FROM ubuntu:22.04

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y apt-utils xinetd iproute2 socat qemu-system-x86 ssh xxd netcat python3 python3-pip tar

RUN pip3 install gdown

WORKDIR /root

RUN gdown 1HqQfiKfTLs9Kci1-AGuCF5x2mhwWdirk
RUN tar xf image.tar.gz

ADD bzImage .
ADD bullseye.id_rsa .
RUN chmod 600 bullseye.id_rsa

ADD landlock.h .
ADD infiltration.c .
ADD Makefile .
ADD entrypoint.sh .

EXPOSE 1337
CMD ["/root/entrypoint.sh"]
