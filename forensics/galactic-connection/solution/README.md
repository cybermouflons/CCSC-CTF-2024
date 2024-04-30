The challenge provides a pcapng file which contains a capture of a WPA2 handshake
and some aditional traffic. The additional traffic contains an HTTP request trying to
fetch a file at `/usr/share/wordlists/john.lst`, which hints that this wordlist should
be used to crack the WPA2 password.

To do this, we first need to convert the file from pcapng to pcap, which we can do using scapy:
```
from scapy.all import *
scapy_cap = rdpcap('galactic_import.pcapng')
wrpcap("wifi_traffic.pcap",scapy_cap)
```

Now we can crack the password using John the Ripper and aircrack-ng, by providing the john wordlist
and asking John to use its default rules:

```
john --wordlist=/usr/share/wordlists/john.lst --rules --stdout | aircrack-ng -e CCSC -w - wifi_traffic.pcap
```

This reveals the WPA2 password, which we can use to decrypt the traffic and get the flag:
```
airdecap-ng -b 80:69:1A:81:FE:85 -e CCSC -p ChangeMe10 wifi_traffic.pcap
```

In the decrypted traffic we see a request for `wpa2_passwords_are_not_secure.com`,
so the flag is `CCSC{wpa2_passwords_are_not_secure}`.
