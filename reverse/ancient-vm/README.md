# Ancient VM

[![Try in PWD](https://raw.githubusercontent.com/play-with-docker/stacks/master/assets/images/button.png)](https://labs.play-with-docker.com/?stack=https://raw.githubusercontent.com/cybermouflons/CCSC-CTF-2023/master/reverse/ancient-vm/docker-compose.yml)


**Category**: reverse

**Author**: neo

## Description

An Andromeda hacker was able to extract an ancient, rusty VM that belongs to Project Echo,
but he couldn't get the file that contains the secret information. Do you think
you can recover it?



## Run locally

Launch challenge:
```
curl -sSL https://raw.githubusercontent.com/cybermouflons/CCSC-CTF-2023/master/reverse/ancient-vm/docker-compose.yml | docker compose -f - up -d
```

Shutdown challenge:
```
curl -sSL https://raw.githubusercontent.com/cybermouflons/CCSC-CTF-2023/master/reverse/ancient-vm/docker-compose.yml | docker compose -f - down
```
