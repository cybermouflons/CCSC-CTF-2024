The password is the flag. This means that the attacker knows the beginning and the end, and the only part of the password that they actually need to guess is the middle. The middle being only 7 characters means that it's straightforward to crack on a relatively modern cpu/gpu.

Start up hashcat, give it the right mask, and get the flag.

`
hashcat -m 1800 pw -a 3 "CCSC{?a?a?a?a?a?a?a}"
`

Flag: CCSC{M4skFtW}
