# Spilled

[![Try in PWD](https://raw.githubusercontent.com/play-with-docker/stacks/master/assets/images/button.png)](https://labs.play-with-docker.com/?stack=https://raw.githubusercontent.com/cybermouflons/CCSC-CTF-2024/master/pwn/spilled/docker-compose.yml)


**Category**: pwn

**Author**: neo + s3nn

## Description

Project Echo is training a new AI model, trying to make it the best C developer.
It's still learning how to read input though, and it's spilling it all over the buffers...



## Run locally

Launch challenge:
```
curl -sSL https://raw.githubusercontent.com/cybermouflons/CCSC-CTF-2024/master/pwn/spilled/docker-compose.yml | docker compose -f - up -d
```

Shutdown challenge:
```
curl -sSL https://raw.githubusercontent.com/cybermouflons/CCSC-CTF-2024/master/pwn/spilled/docker-compose.yml | docker compose -f - down
```
