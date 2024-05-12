# Arcane Runes

## Solution

### Finding the `/spell` page

Can be found in the HTML source code or by clicking the tiny margin on the right of the homepage.

### Bypassing the IP Address allowlist

The allowed IP addresses are all reserved as [TEST-NET](https://en.wikipedia.org/wiki/Reserved_IP_addresses) so getting one of those addresses shouldn't be feasible. However since the code looks for the client IP address in the `X-Forwarded-For` header, we can spoof it by adding any IP address we want e.g. `curl $CHALLENGE_URL -H 'X-Forwarded-For: 233.252.0.0'`

### Obfuscation

This is how the payload was obfuscated, the task here is to reverse the obfuscation.

We can do that in a few ways, as long as we identify that the obfuscated code is valid Javascript -- this is a Web challenge after all.

One approach would be to copy-paste the obfuscated code in a browser's dev console and step through it via the debugger. The debugger should desplay the readable Javascript code. We'll have to do this one more time for the obfuscated flag piece since it was obfuscated twice.

👉 [Flag Payload](https://aem1k.com/transliterate.js/#%7B%22alphabet%22%3A%22iIloOyYzZpPq%22%2C%22code%22%3A%22console.debug%28%5C%22CCSC%7Bmyst1cal_cosplAI_0r_wAIst3_of_tAIm3%7D%5C%22%29%22%7D)

```
console.debug("CCSC{myst1cal_cosplAI_0r_wAIst3_of_tAIm3}")
```

👇

```javascript
i=+![];I=+!i;l=I+I;o=l+I;O=l*l;y=o+l;Y=l*o;z=O+o;[Z,p,P,q,ii,iY,iy,iz,iO,iI,iy,iz,il,iy,iO,iz,io,iz,iO,iy,iY,iO,iz,iy,iY,iz]=(iZ='\\"')+!!iZ+!iZ+iZ.iZ+{};ip=iz+iO+il+iI+P+q+ii+iz+P+iO+q,ip=ip[ip][ip],iP=iy+iO+io+il,iq=q+iY+P+ii+q+il+" ";ip(ip(iq+p+ip(iq+[..."ZIOoZIyzZIyYZIYoZIyzZIyOZIOyZyYZIOOZIOyZIOlZIYyZIOzZyiZOlZIioZIioZIloZIioZIzoZIyyZIzIZIYoZIYOZYIZIOoZIOIZIyOZIozZIOoZIyzZIYoZIYiZIyOZIiIZIIIZIozZYiZIYlZIozZIYzZIiIZIIIZIYoZIYOZYoZIozZIyzZIOYZIozZIYOZIiIZIIIZIyyZYoZIzyZOlZyI"][iP]`+`)`+p)`)``
```

👉 [Final Payload](https://aem1k.com/transliterate.js/#%7B%22alphabet%22%3A%22%u16A6%u16A2%u16A0%u16BB%u16C9%u16CA%u16C7%u16DF%u16DE%u16E6%u16E5%u16DD%u16DC%u16E0%u16D7%u16B1%u16BE%22%2C%22code%22%3A%22//%20well%20met%5Cnconst%20a%20%3D%20%5C%22you%20are%20on%20the%20right%20path%5C%22%3B%5Cnconst%20b%20%3D%20%5C%22keep%20steady%5C%22%3B%5Cnconst%20c%20%3D%20%5C%22you%20can%20feel%20its%20aura%5C%22%5Cnconst%20d%20%3D%20%5C%22it%27s%20glowing%5C%22%3B%5Cnconst%20e%20%3D%20%5C%22one%20last%20step%5C%22%3B%5Cnconst%20f%20%3D%20%27i%3D+%21%5B%5D%3BI%3D+%21i%3Bl%3DI+I%3Bo%3Dl+I%3BO%3Dl*l%3By%3Do+l%3BY%3Dl*o%3Bz%3DO+o%3B%5BZ%2Cp%2CP%2Cq%2Cii%2CiY%2Ciy%2Ciz%2CiO%2CiI%2Ciy%2Ciz%2Cil%2Ciy%2CiO%2Ciz%2Cio%2Ciz%2CiO%2Ciy%2CiY%2CiO%2Ciz%2Ciy%2CiY%2Ciz%5D%3D%28iZ%3D%5C%5C%27%5C%5C%5C%5C%5C%5C%5C%5C%5C%22%5C%5C%27%29+%21%21iZ+%21iZ+iZ.iZ+%7B%7D%3Bip%3Diz+iO+il+iI+P+q+ii+iz+P+iO+q%2Cip%3Dip%5Bip%5D%5Bip%5D%2CiP%3Diy+iO+io+il%2Ciq%3Dq+iY+P+ii+q+il+%5C%22%20%5C%22%3Bip%28ip%28iq+p+ip%28iq+%5B...%5C%22ZIOoZIyzZIyYZIYoZIyzZIyOZIOyZyYZIOOZIOyZIOlZIYyZIOzZyiZOlZIioZIioZIloZIioZIzoZIyyZIzIZIYoZIYOZYIZIOoZIOIZIyOZIozZIOoZIyzZIYoZIYiZIyOZIiIZIIIZIozZYiZIYlZIozZIYzZIiIZIIIZIYoZIYOZYoZIozZIyzZIOYZIozZIYOZIiIZIIIZIyyZYoZIzyZOlZyI%5C%22%5D%5BiP%5D%60+%60%29%60%60+p%29%60%60%29%60%60%27%3B%22%7D)

```javascript
// well met
const a = "you are on the right path";
const b = "keep steady";
const c = "you can feel its aura";
const d = "it's glowing";
const e = "one last step";
const f =
  'i=+![];I=+!i;l=I+I;o=l+I;O=l*l;y=o+l;Y=l*o;z=O+o;[Z,p,P,q,ii,iY,iy,iz,iO,iI,iy,iz,il,iy,iO,iz,io,iz,iO,iy,iY,iO,iz,iy,iY,iz]=(iZ=\'\\\\"\')+!!iZ+!iZ+iZ.iZ+{};ip=iz+iO+il+iI+P+q+ii+iz+P+iO+q,ip=ip[ip][ip],iP=iy+iO+io+il,iq=q+iY+P+ii+q+il+" ";ip(ip(iq+p+ip(iq+[..."ZIOoZIyzZIyYZIYoZIyzZIyOZIOyZyYZIOOZIOyZIOlZIYyZIOzZyiZOlZIioZIioZIloZIioZIzoZIyyZIzIZIYoZIYOZYIZIOoZIOIZIyOZIozZIOoZIyzZIYoZIYiZIyOZIiIZIIIZIozZYiZIYlZIozZIYzZIiIZIIIZIYoZIYOZYoZIozZIyzZIOYZIozZIYOZIiIZIIIZIyyZYoZIzyZOlZyI"][iP]`+`)`+p)`)``';
```

👇

```javascript
ᚦ=+![];ᚢ=+!ᚦ;ᚠ=ᚢ+ᚢ;ᚻ=ᚠ+ᚢ;ᛉ=ᚠ*ᚠ;ᛊ=ᚻ+ᚠ;ᛇ=ᚠ*ᚻ;ᛟ=ᛉ+ᚻ;[ᛞ,ᛦ,ᛥ,ᛝ,ᛜ,ᚦᚢ,ᚦᚦ,ᚦᚠ,ᚾ,ᛠ,ᚦᚦ,ᚦᚠ,ᛗ,ᚦᚦ,ᚾ,ᚦᚠ,ᚱ,ᚦᚠ,ᚾ,ᚦᚦ,ᚦᚢ,ᚾ,ᚦᚠ,ᚦᚦ,ᚦᚢ,ᚦᚠ]=(ᚦᚻ='\\"')+!!ᚦᚻ+!ᚦᚻ+ᚦᚻ.ᚦᚻ+{};ᚦᛉ=ᚦᚠ+ᚾ+ᛗ+ᛠ+ᛥ+ᛝ+ᛜ+ᚦᚠ+ᛥ+ᚾ+ᛝ,ᚦᛉ=ᚦᛉ[ᚦᛉ][ᚦᛉ],ᚦᛊ=ᚦᚦ+ᚾ+ᚱ+ᛗ,ᚦᛇ=ᛝ+ᚦᚢ+ᛥ+ᛜ+ᛝ+ᛗ+" ";ᚦᛉ(ᚦᛉ(ᚦᛇ+ᛦ+ᚦᛉ(ᚦᛇ+[..."ᛞᛊᛟᛞᛊᛟᛞᛉᚦᛞᚢᛇᛟᛞᚢᛉᛊᛞᚢᛊᛉᛞᚢᛊᛉᛞᛉᚦᛞᚢᛊᛊᛞᚢᛉᛊᛞᚢᛇᛉᛞᚢᚠᛞᚢᛉᚻᛞᚢᛊᛟᛞᚢᛊᛇᛞᚢᛇᚻᛞᚢᛇᛉᛞᛉᚦᛞᚢᛉᚢᛞᛉᚦᛞᛟᛊᛞᛉᚦᛞᛉᚠᛞᚢᛟᚢᛞᚢᛊᛟᛞᚢᛇᛊᛞᛉᚦᛞᚢᛉᚢᛞᚢᛇᚠᛞᚢᛉᛊᛞᛉᚦᛞᚢᛊᛟᛞᚢᛊᛇᛞᛉᚦᛞᚢᛇᛉᛞᚢᛊᚦᛞᚢᛉᛊᛞᛉᚦᛞᚢᛇᚠᛞᚢᛊᚢᛞᚢᛉᛟᛞᚢᛊᚦᛞᚢᛇᛉᛞᛉᚦᛞᚢᛇᚦᛞᚢᛉᚢᛞᚢᛇᛉᛞᚢᛊᚦᛞᛉᚠᛞᛟᚻᛞᚢᚠᛞᚢᛉᚻᛞᚢᛊᛟᛞᚢᛊᛇᛞᚢᛇᚻᛞᚢᛇᛉᛞᛉᚦᛞᚢᛉᚠᛞᛉᚦᛞᛟᛊᛞᛉᚦᛞᛉᚠᛞᚢᛊᚻᛞᚢᛉᛊᛞᚢᛉᛊᛞᚢᛇᚦᛞᛉᚦᛞᚢᛇᚻᛞᚢᛇᛉᛞᚢᛉᛊᛞᚢᛉᚢᛞᚢᛉᛉᛞᚢᛟᚢᛞᛉᚠᛞᛟᚻᛞᚢᚠᛞᚢᛉᚻᛞᚢᛊᛟᛞᚢᛊᛇᛞᚢᛇᚻᛞᚢᛇᛉᛞᛉᚦᛞᚢᛉᚻᛞᛉᚦᛞᛟᛊᛞᛉᚦᛞᛉᚠᛞᚢᛟᚢᛞᚢᛊᛟᛞᚢᛇᛊᛞᛉᚦᛞᚢᛉᚻᛞᚢᛉᚢᛞᚢᛊᛇᛞᛉᚦᛞᚢᛉᛇᛞᚢᛉᛊᛞᚢᛉᛊᛞᚢᛊᛉᛞᛉᚦᛞᚢᛊᚢᛞᚢᛇᛉᛞᚢᛇᚻᛞᛉᚦᛞᚢᛉᚢᛞᚢᛇᛊᛞᚢᛇᚠᛞᚢᛉᚢᛞᛉᚠᛞᚢᚠᛞᚢᛉᚻᛞᚢᛊᛟᛞᚢᛊᛇᛞᚢᛇᚻᛞᚢᛇᛉᛞᛉᚦᛞᚢᛉᛉᛞᛉᚦᛞᛟᛊᛞᛉᚦᛞᛉᚠᛞᚢᛊᚢᛞᚢᛇᛉᛞᛉᛟᛞᚢᛇᚻᛞᛉᚦᛞᚢᛉᛟᛞᚢᛊᛉᛞᚢᛊᛟᛞᚢᛇᛟᛞᚢᛊᚢᛞᚢᛊᛇᛞᚢᛉᛟᛞᛉᚠᛞᛟᚻᛞᚢᚠᛞᚢᛉᚻᛞᚢᛊᛟᛞᚢᛊᛇᛞᚢᛇᚻᛞᚢᛇᛉᛞᛉᚦᛞᚢᛉᛊᛞᛉᚦᛞᛟᛊᛞᛉᚦᛞᛉᚠᛞᚢᛊᛟᛞᚢᛊᛇᛞᚢᛉᛊᛞᛉᚦᛞᚢᛊᛉᛞᚢᛉᚢᛞᚢᛇᚻᛞᚢᛇᛉᛞᛉᚦᛞᚢᛇᚻᛞᚢᛇᛉᛞᚢᛉᛊᛞᚢᛇᚦᛞᛉᚠᛞᛟᚻᛞᚢᚠᛞᚢᛉᚻᛞᚢᛊᛟᛞᚢᛊᛇᛞᚢᛇᚻᛞᚢᛇᛉᛞᛉᚦᛞᚢᛉᛇᛞᛉᚦᛞᛟᛊᛞᛉᚦᛞᛉᛟᛞᚢᛊᚢᛞᛟᛊᛞᛊᚻᛞᛉᚢᛞᚢᚻᚻᛞᚢᚻᛊᛞᛟᚻᛞᚢᚢᚢᛞᛟᛊᛞᛊᚻᛞᛉᚢᛞᚢᛊᚢᛞᛟᚻᛞᚢᛊᛉᛞᛟᛊᛞᚢᚢᚢᛞᛊᚻᛞᚢᚢᚢᛞᛟᚻᛞᚢᛊᛟᛞᛟᛊᛞᚢᛊᛉᛞᛊᚻᛞᚢᚢᚢᛞᛟᚻᛞᚢᚢᛟᛞᛟᛊᛞᚢᛊᛉᛞᛊᚠᛞᚢᛊᛉᛞᛟᚻᛞᚢᛟᚢᛞᛟᛊᛞᚢᛊᛟᛞᛊᚻᛞᚢᛊᛉᛞᛟᚻᛞᚢᚻᚢᛞᛟᛊᛞᚢᛊᛉᛞᛊᚠᛞᚢᛊᛟᛞᛟᚻᛞᚢᛟᚠᛞᛟᛊᛞᚢᚢᛟᛞᛊᚻᛞᚢᛊᛟᛞᛟᚻᛞᚢᚻᚻᛞᚢᚻᚠᛞᛊᛉᛞᚢᛇᚦᛞᛊᛉᛞᚢᚠᚦᛞᛊᛉᛞᚢᛇᚢᛞᛊᛉᛞᚢᛊᚢᛞᚢᛊᚢᛞᛊᛉᛞᚢᛊᚢᛞᚢᚻᚢᛞᛊᛉᛞᚢᛊᚢᛞᚢᛟᚢᛞᛊᛉᛞᚢᛊᚢᛞᚢᛟᚠᛞᛊᛉᛞᚢᛊᚢᛞᚢᚢᛟᛞᛊᛉᛞᚢᛊᚢᛞᚢᚢᚢᛞᛊᛉᛞᚢᛊᚢᛞᚢᛟᚢᛞᛊᛉᛞᚢᛊᚢᛞᚢᛟᚠᛞᛊᛉᛞᚢᛊᚢᛞᚢᛊᛉᛞᛊᛉᛞᚢᛊᚢᛞᚢᛟᚢᛞᛊᛉᛞᚢᛊᚢᛞᚢᚢᛟᛞᛊᛉᛞᚢᛊᚢᛞᚢᛟᚠᛞᛊᛉᛞᚢᛊᚢᛞᚢᛊᛟᛞᛊᛉᛞᚢᛊᚢᛞᚢᛟᚠᛞᛊᛉᛞᚢᛊᚢᛞᚢᚢᛟᛞᛊᛉᛞᚢᛊᚢᛞᚢᛟᚢᛞᛊᛉᛞᚢᛊᚢᛞᚢᚻᚢᛞᛊᛉᛞᚢᛊᚢᛞᚢᚢᛟᛞᛊᛉᛞᚢᛊᚢᛞᚢᛟᚠᛞᛊᛉᛞᚢᛊᚢᛞᚢᛟᚢᛞᛊᛉᛞᚢᛊᚢᛞᚢᚻᚢᛞᛊᛉᛞᚢᛊᚢᛞᚢᛟᚠᛞᚢᚻᛊᛞᛟᛊᛞᛊᚦᛞᚢᛊᚢᛞᚢᚻᚠᛞᛟᛊᛞᚢᚻᛉᛞᛉᛟᛞᚢᚻᛉᛞᚢᚻᛉᛞᚢᚻᛉᛞᚢᚻᛉᛞᛉᚠᛞᚢᚻᛉᛞᛉᛟᛞᛊᚢᛞᛊᚻᛞᛉᚢᛞᛉᚢᛞᚢᛊᚢᛞᚢᚻᚠᛞᛊᚻᛞᛉᚢᛞᚢᛊᚢᛞᚢᚻᚠᛞᛊᚻᛞᚢᛊᚢᛞᚢᚻᚠᛞᛊᛇᛞᚢᛊᚢᛞᚢᚻᚠᛞᛊᚻᛞᚢᛟᚻᛞᚢᛟᛊᛞᛟᚻᛞᚢᛊᚢᛞᚢᛇᚦᛞᛟᛊᛞᚢᛊᚢᛞᚢᛟᚠᛞᛊᚻᛞᚢᛊᚢᛞᚢᚢᛟᛞᛊᚻᛞᚢᛊᚢᛞᚢᛊᛉᛞᛊᚻᛞᚢᛊᚢᛞᚢᚢᚢᛞᛊᚻᛞᚢᚠᚦᛞᛊᚻᛞᚢᛇᚢᛞᛊᚻᛞᚢᛊᚢᛞᚢᛊᚢᛞᛊᚻᛞᚢᛊᚢᛞᚢᛟᚠᛞᛊᚻᛞᚢᚠᚦᛞᛊᚻᛞᚢᛊᚢᛞᚢᚢᛟᛞᛊᚻᛞᚢᛇᚢᛞᛊᛉᛞᚢᛊᚢᛞᚢᛇᚦᛞᛟᛊᛞᚢᛊᚢᛞᚢᛇᚦᛞᚢᚻᚻᛞᚢᛊᚢᛞᚢᛇᚦᛞᚢᚻᛊᛞᚢᚻᚻᛞᚢᛊᚢᛞᚢᛇᚦᛞᚢᚻᛊᛞᛊᛉᛞᚢᛊᚢᛞᚢᚠᚦᛞᛟᛊᛞᚢᛊᚢᛞᚢᛟᚢᛞᛊᚻᛞᚢᛊᚢᛞᚢᚢᛟᛞᛊᚻᛞᚢᛊᚢᛞᚢᛊᛟᛞᛊᚻᛞᚢᛊᚢᛞᚢᛊᛉᛞᛊᛉᛞᚢᛊᚢᛞᚢᛇᚢᛞᛟᛊᛞᚢᛇᚢᛞᛊᚻᛞᚢᛊᚢᛞᚢᚻᚢᛞᛊᚻᛞᚢᚠᚦᛞᛊᚻᛞᚢᛊᚢᛞᚢᛊᚢᛞᛊᚻᛞᚢᛇᚢᛞᛊᚻᛞᚢᛊᚢᛞᚢᛊᛉᛞᛊᚻᛞᛉᚠᛞᛉᚦᛞᛉᚠᛞᛟᚻᛞᚢᛊᚢᛞᚢᛇᚦᛞᛊᚦᛞᚢᛊᚢᛞᚢᛇᚦᛞᛊᚦᛞᚢᛊᚢᛞᚢᛇᚢᛞᛊᚻᛞᚢᛇᚦᛞᛊᚻᛞᚢᛊᚢᛞᚢᛇᚦᛞᛊᚦᛞᚢᛊᚢᛞᚢᛇᚢᛞᛊᚻᛞᚢᚻᚻᛞᛊᛇᛞᛊᛇᛞᛊᛇᛞᛉᚠᛞᚢᚻᚠᛞᚢᚢᚢᛞᚢᚢᛟᛞᚢᛊᛟᛞᚢᚻᚠᛞᚢᚢᚢᛞᚢᛟᚢᛞᚢᛟᚠᛞᚢᚻᚠᛞᚢᚢᚢᛞᚢᛟᚢᛞᚢᚻᚢᛞᚢᚻᚠᛞᚢᚢᚢᛞᚢᚻᚢᛞᚢᛊᛟᛞᚢᚻᚠᛞᚢᚢᚢᛞᚢᛟᚢᛞᚢᛟᚠᛞᚢᚻᚠᛞᚢᚢᚢᛞᚢᛟᚢᛞᚢᚢᛟᛞᚢᚻᚠᛞᚢᚢᚢᛞᚢᚢᛟᛞᚢᛟᚢᛞᚢᚻᚠᛞᚢᛟᚢᛞᚢᚻᚢᛞᚢᚻᚠᛞᚢᚢᚢᛞᚢᚢᛟᛞᚢᚢᛟᛞᚢᚻᚠᛞᚢᚢᚢᛞᚢᚢᛟᛞᚢᛟᚢᛞᚢᚻᚠᛞᚢᚢᚢᛞᚢᚢᛟᛞᚢᛊᛉᛞᚢᚻᚠᛞᚢᚢᚢᛞᚢᚻᚢᛞᚢᛟᚢᛞᚢᚻᚠᛞᚢᚢᚢᛞᚢᚢᛟᛞᚢᛟᚠᛞᚢᚻᚠᛞᚢᛟᚢᛞᚢᛊᚢᛞᚢᚻᚠᛞᚢᚢᛟᛞᚢᛊᛉᛞᚢᚻᚠᛞᚢᚢᚢᛞᚢᛊᚢᛞᚢᛊᛟᛞᚢᚻᚠᛞᚢᚢᚢᛞᚢᛊᚢᛞᚢᛊᛟᛞᚢᚻᚠᛞᚢᚢᚢᛞᚢᛊᛉᛞᚢᛊᛟᛞᚢᚻᚠᛞᚢᚢᚢᛞᚢᛊᚢᛞᚢᛊᛟᛞᚢᚻᚠᛞᚢᚢᚢᛞᚢᛟᚠᛞᚢᛊᛟᛞᚢᚻᚠᛞᚢᚢᚢᛞᚢᛟᚢᛞᚢᛟᚢᛞᚢᚻᚠᛞᚢᚢᚢᛞᚢᛟᚠᛞᚢᚢᚢᛞᚢᚻᚠᛞᚢᚢᚢᛞᚢᚻᚢᛞᚢᛊᛟᛞᚢᚻᚠᛞᚢᚢᚢᛞᚢᚻᚢᛞᚢᚢᛟᛞᚢᚻᚠᛞᚢᚻᚢᛞᚢᚢᚢᛞᚢᚻᚠᛞᚢᚢᚢᛞᚢᚢᛟᛞᚢᛊᛟᛞᚢᚻᚠᛞᚢᚢᚢᛞᚢᚢᛟᛞᚢᚢᚢᛞᚢᚻᚠᛞᚢᚢᚢᛞᚢᛟᚢᛞᚢᚢᛟᛞᚢᚻᚠᛞᚢᚢᚢᛞᚢᛊᛟᛞᚢᛟᚠᛞᚢᚻᚠᛞᚢᚢᚢᛞᚢᚢᛟᛞᚢᛊᛟᛞᚢᚻᚠᛞᚢᚢᚢᛞᚢᛟᚢᛞᚢᛟᚠᛞᚢᚻᚠᛞᚢᚢᚢᛞᚢᚻᚢᛞᚢᛊᛟᛞᚢᚻᚠᛞᚢᚢᚢᛞᚢᚻᚢᛞᚢᛊᚢᛞᚢᚻᚠᛞᚢᚢᚢᛞᚢᛟᚢᛞᚢᚢᛟᛞᚢᚻᚠᛞᚢᚢᚢᛞᚢᛊᚢᛞᚢᚢᚢᛞᚢᚻᚠᛞᚢᚢᚢᛞᚢᚢᚢᛞᚢᚢᚢᛞᚢᚻᚠᛞᚢᚢᚢᛞᚢᛊᛟᛞᚢᛟᚠᛞᚢᚻᚠᛞᚢᚻᚢᛞᚢᛊᚢᛞᚢᚻᚠᛞᚢᚢᚢᛞᚢᚻᚢᛞᚢᛊᛉᛞᚢᚻᚠᛞᚢᚢᚢᛞᚢᛊᛟᛞᚢᛟᚠᛞᚢᚻᚠᛞᚢᚢᚢᛞᚢᚻᚢᛞᚢᛟᚠᛞᚢᚻᚠᛞᚢᚢᚢᛞᚢᛊᚢᛞᚢᚢᚢᛞᚢᚻᚠᛞᚢᚢᚢᛞᚢᚢᚢᛞᚢᚢᚢᛞᚢᚻᚠᛞᚢᚢᚢᛞᚢᚻᚢᛞᚢᛊᛟᛞᚢᚻᚠᛞᚢᚢᚢᛞᚢᚻᚢᛞᚢᚢᛟᛞᚢᚻᚠᛞᚢᚻᚢᛞᚢᛊᛟᛞᚢᚻᚠᛞᚢᚢᚢᛞᚢᛊᛟᛞᚢᛟᚠᛞᚢᚻᚠᛞᚢᚢᚢᛞᚢᛟᚢᛞᚢᛟᚠᛞᚢᚻᚠᛞᚢᚢᚢᛞᚢᚢᛟᛞᚢᚻᚢᛞᚢᚻᚠᛞᚢᚢᚢᛞᚢᛊᛟᛞᚢᛟᚠᛞᚢᚻᚠᛞᚢᚢᚢᛞᚢᚻᚢᛞᚢᚢᛟᛞᚢᚻᚠᛞᚢᚢᚢᛞᚢᛊᚢᛞᚢᚢᚢᛞᚢᚻᚠᛞᚢᚢᚢᛞᚢᚢᚢᛞᚢᚢᚢᛞᚢᚻᚠᛞᚢᚢᚢᛞᚢᛟᚢᛞᚢᛟᚢᛞᚢᚻᚠᛞᚢᚻᚢᛞᚢᛊᛟᛞᚢᚻᚠᛞᚢᚢᚢᛞᚢᛟᚠᛞᚢᛟᚢᛞᚢᚻᚠᛞᚢᚢᛟᛞᚢᛊᛉᛞᚢᚻᚠᛞᚢᛟᚢᛞᚢᚢᚢᛞᛉᚠᛞᚢᚻᛊᛞᚢᚻᚻᛞᚢᛊᚢᛞᚢᚠᚦᛞᚢᚻᛊᛞᚢᛉᚦᛞᛊᚻᛞᚢᛉᚦᛞᛊᚢᛞᚢᛉᚦᛞᚢᛉᚦᛞᛊᚻᛞᚢᛇᚦᛞᛊᚢᛞᚢᛉᚦᛞᚢᛉᚦᛞᛊᚢᛞᚢᛉᚦᛞᚢᛉᚦᛞᛉᛟᛞᛟᚻ"][ᚦᛊ]`+`)`+ᛦ)`)``
```
