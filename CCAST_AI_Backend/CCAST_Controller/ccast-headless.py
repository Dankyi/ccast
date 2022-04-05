import ccxt.async_support as ccxt
from time import sleep as pause
from getpass import getpass as secret_input
from sys import exit as shutdown

from AI_System import ai

if __name__ == "__main__":

    user_input = input("Real Money or Fake Money? (R/F): ")
    user_input = user_input.upper()

    DUMMY = None

    EXCHANGE = None

    if user_input == "R":

        DUMMY = False

        print()

        public_key = secret_input("API (Public) Key: ")
        private_key = secret_input("API (Secret/Private) Key: ")

        print()

        print("Public Key Length: " + str(len(public_key)))
        print("Secret/Private Key Length: " + str(len(private_key)))

        EXCHANGE = ccxt.ftx({"verbose": False, "enableRateLimit": True, "apiKey": public_key, "secret": private_key})

        public_key = None
        private_key = None

    elif user_input == "F":

        DUMMY = True

        EXCHANGE = ccxt.ftx({"verbose": False, "enableRateLimit": True})

    else:

        print()
        print("Please type either R or F for Real Money or Fake Money respectively!")
        shutdown()

    print()
    input()

