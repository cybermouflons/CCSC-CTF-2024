# Underground Watch - Part 2

[![Try in PWD](https://raw.githubusercontent.com/play-with-docker/stacks/master/assets/images/button.png)](https://labs.play-with-docker.com/?stack=https://raw.githubusercontent.com/cybermouflons/CCSC-CTF-2023/master/forensics/underground_watch_part_2/docker-compose.yml)


**Category**: forensics

**Author**: sAINT_barber

## Description

We saw the attacker gain access on our surveillance application and execute a few commands, but then, the attacker disappeared, almost like they went through an underground tunnel.. 
We still have the packet capture, if this can help you understand what they did?

Note: Solution to Underground Watch - Part 1 is required to solve this challenge



## Run locally

Launch challenge:
```
curl -sSL https://raw.githubusercontent.com/cybermouflons/CCSC-CTF-2023/master/forensics/underground_watch_part_2/docker-compose.yml | docker compose -f - up -d
```

Shutdown challenge:
```
curl -sSL https://raw.githubusercontent.com/cybermouflons/CCSC-CTF-2023/master/forensics/underground_watch_part_2/docker-compose.yml | docker compose -f - down
```
