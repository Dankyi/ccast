import ccxt.async_support as ccxt
from time import sleep
from sys import exit as force_kill_ai


"""

This Python file contains all the methods used to access the external exchange, including exception catching and trying
again in-case of a thrown error.

"""


def __log_exception(function, message):

    with open("Connection_Error_Log.txt", "w+") as connection_error_log_file:

        connection_error_log_file.write("Occurred In: " + str(function))
        connection_error_log_file.write("\n\n")
        connection_error_log_file.write("Failure Reason: " + str(message))


async def load_markets(exchange, stop_signal):

    success = False
    logged = False

    while not success:

        try:

            await exchange.load_markets(True)

            success = True

        except (ccxt.RequestTimeout,
                ccxt.DDoSProtection,
                ccxt.ExchangeNotAvailable,
                ccxt.ExchangeError,
                ccxt.InvalidNonce) as Error:

            print("\nError in LOAD MARKETS - Retrying...\nReason: " + str(Error))

            sleep(1.0)

            if not logged:
                __log_exception("Load Markets", Error)
                logged = False

            if stop_signal.is_set():
                force_kill_ai()


async def fetch_current_price(exchange, coin_pair, stop_signal):

    current_price = 0.0

    success = False
    logged = False

    while not success:

        try:

            current_price = await exchange.fetch_ticker(coin_pair)
            current_price = float(current_price.__getitem__("last"))

            success = True

        except (ccxt.RequestTimeout,
                ccxt.DDoSProtection,
                ccxt.ExchangeNotAvailable,
                ccxt.ExchangeError,
                ccxt.InvalidNonce) as Error:

            print("\nError in FETCH CURRENT PRICE - Retrying...\nReason: " + str(Error))

            sleep(1.0)

            if not logged:
                __log_exception("Fetch Current Price", Error)
                logged = False

            if stop_signal.is_set():
                force_kill_ai()

    return current_price


async def fetch_balance(exchange, stop_signal):

    account_balance = {}

    success = False
    logged = False

    while not success:

        try:

            account_balance = await exchange.fetch_balance()
            account_balance = account_balance["total"]

            success = True

        except (ccxt.RequestTimeout,
                ccxt.DDoSProtection,
                ccxt.ExchangeNotAvailable,
                ccxt.ExchangeError,
                ccxt.InvalidNonce) as Error:

            print("\nError in FETCH BALANCE - Retrying...\nReason: " + str(Error))

            sleep(1.0)

            if not logged:
                __log_exception("Fetch Balance", Error)
                logged = False

            if stop_signal.is_set():
                force_kill_ai()

    return account_balance


async def create_order(exchange, coin_pair, side, amount, stop_signal):

    success = False
    logged = False

    while not success:

        try:

            await exchange.create_order(coin_pair, "market", side, amount)

            success = True

        except (ccxt.RequestTimeout,
                ccxt.DDoSProtection,
                ccxt.ExchangeNotAvailable,
                ccxt.ExchangeError,
                ccxt.InvalidNonce) as Error:

            print("\nError in CREATE ORDER - Retrying...\nReason: " + str(Error))

            sleep(1.0)

            if not logged:
                __log_exception("Create Order", Error)
                logged = False

            if stop_signal.is_set():
                force_kill_ai()
