from tokenize import Double
import ccxt.async_support as ccxt
from time import sleep as pause
from getpass import getpass as secret_input
from sys import exit as shutdown
import configparser
import os

from AI_System import ai

if __name__ == "__main__":

    cwd = os.getcwd()
    filename = cwd + "\config.ini"

    if not os.path.exists(filename):
        filename = cwd + "/config.ini" # Try using / instead of \

        if not os.path.exists(filename):
            print("File not found: ", filename)
            quit()

    config = configparser.ConfigParser()
    config.read(filename)

    public_key = config['market_info']['public_key']
    private_key = config['market_info']['private_key']
    DUMMY = bool(config['instance_info']['DUMMY'])

    EXCHANGE = ccxt.ftx({"verbose": False, "enableRateLimit": True, "apiKey": public_key, "secret": private_key})

    coin_pair = config['instance_info']['coin_pair']
    buy_grid_percentage = float(config['instance_info']['buy_grid_percentage'])
    sell_grid_percentage = float(config['instance_info']['sell_grid_percentage'])

    AI = ai.AIGridBot(EXCHANGE, DUMMY, coin_pair, buy_grid_percentage, sell_grid_percentage)

    TIME_IN_SECONDS = int(config['instance_info']['time_in_seconds'])
    SECONDS_PASSED = 0


    INFORMATION = {}
    AI.start()

    while True:

        INFORMATION = AI.get_information()

        balance = INFORMATION["BALANCE"]
        current_price = INFORMATION["CURRENT PRICE"]
        grid_amount = INFORMATION["GRID AMOUNT"]
        alive = INFORMATION["ALIVE"]
        profit = INFORMATION["PROFIT"]

        if SECONDS_PASSED % 5 == 0:

            print()

            print(f"Current Balance ({coin_pair}): {str(balance)}\nCurrent Price ({coin_pair}): {str(current_price)}\n"
                  f"Grid Amount: {str(grid_amount)}\nRunning: {str(alive)}\nProfit: {str(profit)}%\n\n"
                  f"Time Remaining (Seconds): {str(TIME_IN_SECONDS - SECONDS_PASSED)}")

            if alive and balance[0] > 0 and SECONDS_PASSED > TIME_IN_SECONDS:
                print()
                print("Selling Remaining Cryptocurrency Before Stopping!")
                print()

        pause(1.0)
        SECONDS_PASSED += 1

        if SECONDS_PASSED == TIME_IN_SECONDS:
            AI.stop()

        if not alive:
            break

    AI.join()

    INFORMATION = AI.get_information()

    balance = INFORMATION["BALANCE"]
    profit = INFORMATION["PROFIT"]

    print()

    print(f"Final Balance: {str(balance)}\nProfit: {str(profit)}%")
    input()  # Stops console window from closing
