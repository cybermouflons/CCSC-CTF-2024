## Drone Army Solution

The point of the challenge is to reverse engineer ARM (aarch64) assembly program.

If not jumped straight to reverse engineering, participants can optionally compile and run the program to get a better understanding of how it works. On execution they will notice that the program accepts user input and returns "Success!" or "Try again..." messages.
One can assume that on succesfull input of the flag the program execution leads to the success message. However executing the program is not mandatory. 

Upon inspecting the source code, participants should notice the data section which contains some seemingly random bytes. It would make sense to assume that these bytes have  something to do with the flag.

During the reversing process participants should familiarise themselves with the ARM assembly instructions.

In the first section of the program we can see line 19 loads the number 29 to the x4 register which is compared to the length of the input from the read system call (x3).

If that's true the execution continues and byte with value 0x65 is loaded to register x3. Then the program enters a loop of 28 iterations (we see x5 = 0 compared to the length of the input (x3) which should be 29 at that point) and each byte from user input is loaded to the w6 register and xored with the previous character (w4 starts with 0x65 in this case). 
This continues for all 29 bytes. In summaryu the program implements a simple XOR encryption where a rolling window of 2 characters are taken from the bytes defined in the data section and XORED together to make up the flag, which is checked against the user input. 

Alternatively, players can take the bytes from the data section and get the XOR input differential (even without the leading 0x65 bytes) and they will get the flag. 

Here is a PoC script to decrypt that using python:
```python
data = [0x65] + [0x26, 0x65, 0x36, 0x75, 0xe, 0x3a, 0x48, 0x5, 0x7c, 0x23, 0x13, 0x75, 0x2a, 0x72, 0x42, 0x30, 0x43, 0x1c, 0x4e, 0x7d, 0xb, 0x38, 0x4a, 0x7f, 0x1a, 0x5e, 0x7f, 0x5e, 0x23]
print("".join(chr(a^b) for a,b in zip(data, data[1:])))
```