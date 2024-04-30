This challenge provides a python script that's obfuscated using [PyArmor](https://github.com/dashingsoft/pyarmor).
If we run the provided script, we are provided with two options:

```
python3 armored_up.py

Welcome to the Project Echo Armored Up server
=============================================
1. Get secret
2. Forgot password
```

If we select option 2, we are provided with some hints about the password: it's more
than 30 characters long, it starts with the letter 'p' and ends with the letter 'e',
and it's not stored as plain text in memory.

If we select option 1, we are asked for the password. If we provide a random password,
we get back the following:

```
Reconstructing plain text password....
Traceback (most recent call last):
  File "<frozen __main__>", line 3, in <module>
  File "<frozen armored_up>", line 81, in <module>
  File "<frozen armored_up>", line 65, in get_secret
ModuleNotFoundError: No module named 'secret'
```

It seems like the program is reconstructing the plaintext password in memory
and then trying to import a module called `secret`, which is not provided.

To leak the password, we can create a fake `secret` module which just sleeps and
[dump the memory](https://gist.githubusercontent.com/Dbof/b9244cfc607cf2d33438826bee6f5056/raw/aa4b75ddb55a58e2007bf12e17daadb0ebebecba/memdump.py)
of the program, which should contain the reconstructed plaintext password.

```
echo -e "import time\ntime.sleep(100)" > secret.py
```

After getting the memory dump, we can grep for strings that start with the letter
'p' and end with the letter 'e' and are more than 30 characters long:

```
strings -n 30 mem.dump | grep "^p.*e$"

posix_spawn_file_actions_addclose
passed as positional arguments to zip().  The i-th element in every tuple
platform dependent, but any encoding supported by Python can be
passing a callable as *opener*. The underlying file descriptor for the file
python: Can't reopen .pyc file
pickler has already seen, so that shared or recursive objects are
protocol is 4. It was introduced in Python 3.4, and is incompatible
protocol is 4. It was introduced in Python 3.4, and is incompatible
protocol is 4. It was introduced in Python 3.4, and is incompatible
partial character in shift sequence
pyexpat version is incompatible
position value cannot be negative
preadv2() arg 2 must be a sequence
pwritev() arg 2 must be a sequence
prefixes directly, as well as with lib/site-packages appended.  The
passed as positional arguments to zip().  The i-th element in every tuple
passing a callable as *opener*. The underlying file descriptor for the file
pr3p4re_f0r_tr0ubl3_and_m4ke_1t_d0uble
pyarmor_runtime_000000.pyarmor_runtime
pyarmor_runtime_000000.pyarmor_runtime
posix_spawn_file_actions_addclose
```

The password is `pr3p4re_f0r_tr0ubl3_and_m4ke_1t_d0uble`, which we can provide
to the remote server and get the flag.
