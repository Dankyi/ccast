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

    coin_pair = input("Coin Pair (e.g., ETH/BTC): ")
    coin_pair = coin_pair.upper()
    buy_grid_percentage = float(input("Lower/Buy Grid Percentage: "))
    sell_grid_percentage = float(input("Sell/Profit Percentage: "))

    AI = ai.AIGridBot(EXCHANGE, DUMMY, coin_pair, buy_grid_percentage, sell_grid_percentage)

    print()

    run_time = input("Run Time (e.g., 16M or 8H or 4D): ")

    time_period = run_time[-1].upper()
    run_time = int(run_time[:-1])

    TIME_IN_SECONDS = 60
    SECONDS_PASSED = 0

    if time_period == "M":
        TIME_IN_SECONDS *= run_time
    elif time_period == "H":
        TIME_IN_SECONDS *= 60 * run_time
    elif time_period == "D":
        TIME_IN_SECONDS *= 60 * 24 * run_time
    else:
        print()
        print("Invalid Time Period Given! (M/H/D) == (Minutes/Hours/Days)")
        shutdown()

    if TIME_IN_SECONDS == 0:
        print()
        print("Invalid Time Given! (Must Be At Least 1 MINUTE)")
        shutdown()

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
