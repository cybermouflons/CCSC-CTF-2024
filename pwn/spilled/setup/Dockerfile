FROM ubuntu:22.04

RUN apt-get update && apt-get install -y socat gcc-multilib

# set workdir and transfer binary
WORKDIR /root
COPY spilled .
COPY flag.txt .

EXPOSE 1337
CMD ["socat", "-v","TCP-LISTEN:1337,reuseaddr,fork", "EXEC:'/root/spilled'"]
