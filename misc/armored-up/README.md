# Armored Up

[![Try in PWD](https://raw.githubusercontent.com/play-with-docker/stacks/master/assets/images/button.png)](https://labs.play-with-docker.com/?stack=https://raw.githubusercontent.com/cybermouflons/CCSC-CTF-2023/master/misc/armored-up/docker-compose.yml)


**Category**: misc

**Author**: neo

## Description

You managed to exfiltrate a super secret Project Echo file, but it's really
well protected. Can you figure out the correct password?

Note:
  Python 3.11.2 (default in Debian 12)



## Run locally

Launch challenge:
```
curl -sSL https://raw.githubusercontent.com/cybermouflons/CCSC-CTF-2023/master/misc/armored-up/docker-compose.yml | docker compose -f - up -d
```

Shutdown challenge:
```
curl -sSL https://raw.githubusercontent.com/cybermouflons/CCSC-CTF-2023/master/misc/armored-up/docker-compose.yml | docker compose -f - down
```
