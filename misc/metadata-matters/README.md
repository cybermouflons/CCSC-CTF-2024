# Metadata Matters


**Category**: misc

**Author**: YetAnotherAlt123

## Description

One of our agents has gotten a foothold on an old, isolated workstation. It looks like it might have some important information, but we need superuser privileges to get to it.

We managed to extract the password hash for the root user. We know that the password policy mandates passwords that are 10 characters long, and requires that they have capitals, numbers, lowercase letters and symbols.

```
root:$6$yWctB8cp.P4qQJWg$P.EXiq4zC/sbiv2GLFvaZjFwyPFP.SYzslFlWV/WUi3ccJOvGYcuVv1zAWl09FA74/squo.hXzwDPWDrUzl9N1
```

Cracking a good, long password seems impossible... unless you know something we don't?


