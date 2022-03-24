import ccxt.async_support as ccxt
from time import sleep


"""

This Python file contains all the methods used to access the external exchange, including exception catching and trying
again in-case of a thrown error.

"""


async def load_markets(exchange):

    success = False

    while not success:

        try:

            await exchange.load_markets(True)

            success = True

        except (ccxt.RequestTimeout,
                ccxt.DDoSProtection,
                ccxt.ExchangeNotAvailable,
                ccxt.ExchangeError,
                ccxt.InvalidNonce):

            sleep(1.0)
            # TODO: Log the exception thrown?
            continue


async def fetch_current_price(exchange, coin_pair):

    current_price = 0.0
    success = False

    while not success:

        try:

            current_price = await exchange.fetch_ticker(coin_pair)
            current_price = float(current_price.__getitem__("last"))

            success = True

        except (ccxt.RequestTimeout,
                ccxt.DDoSProtection,
                ccxt.ExchangeNotAvailable,
                ccxt.ExchangeError,
                ccxt.InvalidNonce):

            sleep(1.0)
            #  TODO: Log the exception thrown?
            continue

    return current_price


async def fetch_balance(exchange):

    account_balance = {}
    success = False

    while not success:

        try:

            account_balance = await exchange.fetch_balance()
            account_balance = account_balance["total"]

            success = True

        except (ccxt.RequestTimeout,
                ccxt.DDoSProtection,
                ccxt.ExchangeNotAvailable,
                ccxt.ExchangeError,
                ccxt.InvalidNonce):

            sleep(1.0)
            # TODO: Log the exception thrown?
            continue

    return account_balance


async def create_order(exchange, coin_pair, side, amount):

    success = False

    while not success:

        try:

            await exchange.create_order(coin_pair, "market", side, amount)

            success = True

        except (ccxt.RequestTimeout,
                ccxt.DDoSProtection,
                ccxt.ExchangeNotAvailable,
                ccxt.ExchangeError,
                ccxt.InvalidNonce):

            sleep(1.0)
            # TODO: Log the exception thrown?
            continue
