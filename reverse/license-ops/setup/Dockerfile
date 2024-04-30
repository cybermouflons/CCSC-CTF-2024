
FROM ubuntu

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y socat gcc-multilib

# set workdir and transfer binary
WORKDIR /root
COPY license .
COPY flag.txt .

# execute permissions
RUN chmod 755 license

EXPOSE 1337
CMD ["socat", "-v","TCP-LISTEN:1337,reuseaddr,fork,su=root", "EXEC:'/root/license'"]
