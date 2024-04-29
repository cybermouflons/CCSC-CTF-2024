# Underground Watch - Part 1

[![Try in PWD](https://raw.githubusercontent.com/play-with-docker/stacks/master/assets/images/button.png)](https://labs.play-with-docker.com/?stack=https://raw.githubusercontent.com/cybermouflons/CCSC-CTF-2023/master/web/underground_watch_part_1/docker-compose.yml)


**Category**: web

**Author**: sAINT_barber

## Description

The Andromeda Initiative's surveillance application has been hacked by OrionTech. They managed to gain access to our server and left a note in the root (`/`) directory. 
We need you to find the vulnerability and report back how they hacked us.



## Run locally

Launch challenge:
```
curl -sSL https://raw.githubusercontent.com/cybermouflons/CCSC-CTF-2023/master/web/underground_watch_part_1/docker-compose.yml | docker compose -f - up -d
```

Shutdown challenge:
```
curl -sSL https://raw.githubusercontent.com/cybermouflons/CCSC-CTF-2023/master/web/underground_watch_part_1/docker-compose.yml | docker compose -f - down
```
