# Solution

## Part 1

Decode inject.bin into Ducky Script using https://github.com/dagonis/Mallard

```bash
python mallard/__main__.py -f inject.bin
```

We also get pastebin URL: https://pastebin.com/raw/bLfwPMuM

<details>
    <summary>Reveal Flag</summary>
    CCSC{Dis4bling_USBs_D03s_n0t_Dis4ble_HID}
</details>

## Part 2

View pastebin and see that the following tool was run on the victim: [TinkererShell.py](https://github.com/4n4nk3/TinkererShell)

After browsing the code, it can be determined that the reverse shell is using a symmetric hard-coded key and AES EAX.Mode. Thankfully the tool has encrypt / decrypt functions and the transmission is in JSON format (encrypted).

So we can pull the JSON lines from the pcap file and feed them into the decryption functions to see the reverse shell comms. 

On one line we see that the attacker has cat'd a file called flag.txt which is the flag for part2

The [aes.py](./aes.py) file provides the extracted encrypt / decrypt functions with the extracted encrypted traffic so you can just run it to see the decrypted values.

<details>
    <summary>Reveal Flag</summary>
    CCSC{part2-N1ce_One-Decrypting_Th3_C0mms}
</details>

## Part 3

From the PCAP we can also see that an attacker has uploaded a large file which is a base64-encoded ELF file.
After decrypting and decoding the file locally, we start debugging the ELF file. 

This has been encoded using the Shikata Ga Nai polymorphic encoder so it makes static analysis extremely hard. 

After some dynamic analysis and allowing the program to decode itself, we get to a point where the program checks the user's gid and exits if it does not match `0xdeadbeef`. This can be bypassed directly from a debugger or creating a new group.

Secondly, we see that 4 qwords are pushed onto the stack but appear to be garbage.

Thirdly, we see that the program asks for 8 bytes of input and uses the first 4 bytes as a xor key. This key is xored with every QWORD previously pushed onto the stack, one by one. However, the result is still garbage.

At this point, it can be deduced that the 4 QWORDS pushed onto the stack are the flag and the first 4 bytes are `CCSC`, a known plaintext. If we take these bytes and xor them with the first DWORD pushed onto the stack, we get the actual xor key `0x13371337`. We can then modify the program or extract the bytes and xor offline to get the final flag.

<details>
    <summary>Reveal Flag</summary>
    CCSC{It-C4nn0t_Be_Helpd_Push_On}
</details>