"""

Author: Zac King (U1758957)

This Python file connects to the Kraken exchange and gets the last 720 minutes of price data
for a coin (default is BTC/GBP). It then writes it to a text file, which you can then use
in the AI testing.

The purpose of it is to not have to connect to the exchanges every single time you run the
AI files, as it takes a while for connections to be created and destroyed.

It is purely for testing purposes.

"""

import ccxt.async_support as ccxt
import asyncio


async def get_exchange():

    """
    Connecting to an exchange and returning the object.

    "verbose": False -> Don't print out all the HTTPS connection info etc.
    "enableRateLimit" : True -> Respect the ping limit of the exchange, if you poll it too fast
                                then they will ban your IP, this command prevents that possibility.

    :return: the exchange object
    """

    exchange = ccxt.kraken({"verbose": False, "enableRateLimit": True})
    await exchange.load_markets(True)

    return exchange
