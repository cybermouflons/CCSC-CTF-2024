The admin portal is vulnerable to a side channel attack; there is a small delay after every character in the password is checked.

Then, the player is able to exploit CVE-2024-32005 (https://cvefeed.io/vuln/detail/CVE-2024-32005#!) to read local files. The player is expected to find and read app.py, and figure out their next steps.

In order to perform the SSRF to obtain the flag, the user needs to make a request to /FLAG, intercept and drop that request, navigate to /login, login and intercept the redirect, drop that request again and manually browse to /super_secret_status_page to perform the CSRF and get the flag.

