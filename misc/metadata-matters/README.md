# Metadata Matters


**Category**: misc

**Author**: YetAnotherAlt123

## Description

One of our agents has gotten a foothold on an old, isolated workstation. It looks like it might have some important information, but we need superuser privileges to get to it.

We managed to extract the password hash for the root user. We know that the password policy mandates passwords that are 12 characters long, and requires that they have capitals, numbers, lowercase letters and symbols.

```
root:$6$hJRNE3mUrOwPQcEd$5JE.VZyAKwFlIY448NOcmzDQX.3dGAr0aUn7ogkw97pU/qcT0l6PN5M2YA32E4Km.5bmQE1jh7cHfbRUieZ0g1
```

Cracking a good, long password seems impossible... unless you know something we don't?


