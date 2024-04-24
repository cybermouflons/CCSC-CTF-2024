# Metadata Matters


**Category**: misc

**Author**: YetAnotherAlt123

## Description

One of our agents has gotten a foothold on an old, isolated workstation. It looks like it might have some important information, but we need superuser privileges to get to it.

We managed to extract the password hash for the root user. We know that the password policy mandates passwords up to 13 characters long, and requires that they have capitals, numbers and letters.

```
root:$6$jM2.hLB7cxxe0Jik$ukjRJ6VORdRKdK0aBkKpjGzgId6OrR0srv.vrNlIj3gC8KTTk9nnf8bubTNUCTKo.he5CwFFs2xV9B1KHKDRt1
```

Cracking a good, long password seems impossible... unless you know something we don't?


