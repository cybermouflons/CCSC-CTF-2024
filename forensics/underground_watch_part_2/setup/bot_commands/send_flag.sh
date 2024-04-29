#!/bin/bash
host=172.23.0.2

echo "Sending flag..."
# Attacker uses tunnel to send requests to the internal port 12345
curl --tlsv1.2 --tls-max 1.2 -d "x=Now i can hack in private!" https://$host:31337 -k
sleep 1

curl --tlsv1.2 --tls-max 1.2 -d "x=Since i am using HTTPS nobody can read the requests through this tunnel! MUAHAHAHA" https://$host:31337 -k
sleep 1

curl --tlsv1.2 --tls-max 1.2 -d "x=I can even send secrets through here like this flag, CCSC{tuNn3L1n9_w17H_iMP3rf3c7_f0rw4rd_53cr3Cy}" https://$host:31337 -k
sleep 1

curl --tlsv1.2 --tls-max 1.2 -d "x=I think i should delete the certificate file after I've finished!" https://$host:31337 -k
sleep 1
echo "Done..."
