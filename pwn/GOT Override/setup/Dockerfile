
FROM ubuntu

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y socat gcc-multilib

# set workdir and transfer binary
WORKDIR /root
COPY got-override .
COPY ld-linux-x86-64.so.2 .
COPY flag.txt .
COPY libc.so.6 .

RUN chmod 755 got-override
RUN chmod 755 ld-linux-x86-64.so.2
RUN chmod 755 libc.so.6

EXPOSE 1337
CMD ["socat", "-v","TCP-LISTEN:1337,reuseaddr,fork,su=root", "EXEC:'/root/got-override'"]
