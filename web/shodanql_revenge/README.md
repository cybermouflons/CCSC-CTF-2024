# ShodanQL - Revenge

[![Try in PWD](https://raw.githubusercontent.com/play-with-docker/stacks/master/assets/images/button.png)](https://labs.play-with-docker.com/?stack=https://raw.githubusercontent.com/cybermouflons/CCSC-CTF-2024/master/web/shodanql_revenge/docker-compose.yml)


**Category**: web

**Author**: sAINT_barber

## Description

We found this website that seems to list all systems OrionTech as owned.
Can you access the admin page and take the site down for good?



## Run locally

Launch challenge:
```
curl -sSL https://raw.githubusercontent.com/cybermouflons/CCSC-CTF-2024/master/web/shodanql_revenge/docker-compose.yml | docker compose -f - up -d
```

Shutdown challenge:
```
curl -sSL https://raw.githubusercontent.com/cybermouflons/CCSC-CTF-2024/master/web/shodanql_revenge/docker-compose.yml | docker compose -f - down
```
