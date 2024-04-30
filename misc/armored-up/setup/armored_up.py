pwd = [
    112,
    114,
    51,
    112,
    52,
    114,
    101,
    95,
    102,
    48,
    114,
    95,
    116,
    114,
    48,
    117,
    98,
    108,
    51,
    95,
    97,
    110,
    100,
    95,
    109,
    52,
    107,
    101,
    95,
    49,
    116,
    95,
    100,
    48,
    117,
    98,
    108,
    101,
]


def banner():
    print("Welcome to the Project Echo Armored Up server")
    print("=============================================")


def menu():
    print("1. Get secret")
    print("2. Forgot password")


def forgot_pass():
    print(" - It's more than 30 chars (uncrackable)")
    print(" - p***...***e")
    print(" - I made sure I didn't store it as plain text in the program :)")


def get_secret():
    x = input("Password: ")

    print("Reconstructing plain text password....")
    correct = "".join([chr(x) for x in pwd])

    import secret

    if x == correct:
        print(f"That's correct! Flag: {secret.flag}")
    else:
        print("Wrong password")


if __name__ == "__main__":

    banner()

    while True:
        menu()
        inp = input("> ")
        if inp == "1":
            get_secret()
        elif inp == "2":
            forgot_pass()
        else:
            print("No such choice")
