
FROM ubuntu

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y socat gcc-multilib

# set workdir and transfer binary
WORKDIR /root
COPY tlv .
COPY flag.txt .

RUN chmod 755 tlv

EXPOSE 8080
ENTRYPOINT '/root/tlv'
