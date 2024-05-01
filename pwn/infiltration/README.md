# Infiltration

[![Try in PWD](https://raw.githubusercontent.com/play-with-docker/stacks/master/assets/images/button.png)](https://labs.play-with-docker.com/?stack=https://raw.githubusercontent.com/cybermouflons/CCSC-CTF-2024/master/pwn/infiltration/docker-compose.yml)


**Category**: pwn

**Author**: neo

## Description

You finally managed to infiltrate Project Echo's systems, but it looks like they are guarding the secret information pretty well. If only there was a way to dump the secret...



## Run locally

Launch challenge:
```
curl -sSL https://raw.githubusercontent.com/cybermouflons/CCSC-CTF-2024/master/pwn/infiltration/docker-compose.yml | docker compose -f - up -d
```

Shutdown challenge:
```
curl -sSL https://raw.githubusercontent.com/cybermouflons/CCSC-CTF-2024/master/pwn/infiltration/docker-compose.yml | docker compose -f - down
```
