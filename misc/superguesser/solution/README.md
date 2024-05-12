# Superguesser

## Solution

### Part 1

```go
seed := time.Now().Unix()
random := rand.New(rand.NewSource(seed))
randomNumber, maxTries = random.Int63(), 10
```

If we know the seed, we know the random number generated. The Go random number generator will produce the same sequence of numbers for the same seed every time.

The seed in this case is predictable since it's the current time in Unix seconds.

We can take note of the Unix second at the time we connected to the challenge and use that to seed our own Go program locally and print out the `randomNumber` generated.

We also have 10 tries so there's some flexibility to also check subsequent seconds in case of network delays.

### Part 2

```go
seed := time.Now().UnixMilli()
random := rand.New(rand.NewSource(seed))
randomNumber, maxTries = random.Int63(), 50
```

There a thousand milliseconds in a second. Same as Part 1, we can keep note of the current Unix millisecond we connect to the challenge. Due to network delays we'll need the 50 attempts to try subsequent milliseconds. We'll probably also need to run the challenge a few times until we get a bit lucky.

Another approach is to simultaneously connect to the challenge server from 2 clients in the hopes of both clients connecting at the same millisecond. If we achieve that, then we have 50+50 attempts at the same number, so we can "guess" it using [Binary Search](https://en.wikipedia.org/wiki/Binary_search_algorithm) (we only need 63 attempts for a 63-bit number.)

### Part 3

```go
seed := time.Now().UnixNano()
random := rand.New(rand.NewSource(seed))
randomNumber, maxTries = random.Int63(), 100
```

There are a billion nanoseconds in a second. We could still try our luck by spamming attempts but 100 tries are more than enough to perform a [Binary Search](https://en.wikipedia.org/wiki/Binary_search_algorithm) like a pro.
