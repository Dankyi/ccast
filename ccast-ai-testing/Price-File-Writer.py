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


async def get_price_history(exchange, coin_index, time_period):

    """

    Connecting to the exchange and getting 720 time periods (minutes, days, etc) of data, and returning these as a list.

    :param exchange: The cryptocurrency exchange object
    :param coin_index: The integer index of the coin
    :param time_period: The exchange grabs 720 points of this time period, e.g., "1m" is 720 minutes, "1d" is 720 days.
    :return: a list of closing prices for the coin inputted, each index is 1 unit of time_period
    """

    candle_stick_data = await exchange.fetch_ohlcv(exchange.symbols[coin_index], time_period)

    price_history = []

    for candle_stick in candle_stick_data:
        price_history.append(candle_stick[3])
        # With Kraken, index [3] is the closing price.

    return price_history


def save_text_file(price_history):

    """

    Saves the price history list to a text file, each line is one price.

    :param price_history: The price history list to write
    :return: void
    """

    price_history_length = len(price_history)

    with open("price.txt", "w+") as txt_file:

        for i in range(price_history_length):

            txt_file.write(str(price_history[i]))

            if i < price_history_length - 1:
                txt_file.write("\n")


async def main():

    """

    The main method of the code, grabs exchange, grabs price history, writes to file, and closes the connection.

    Note that in PyCharm you might get a RuntimeError, this is something to do with PyCharm and doesn't effect anything,
    so ignore it.

    :return:
    """

    print("1. Getting Exchange")

    exchange = await get_exchange()

    print("Gotten Exchange!")

    coin_index = -1
    coin = "BTC/GBP"  # Change this to any coin you want if it's supported by Kraken.
                      # You can do print(exchange.symbols) to see all supported coins.

    print("2. Getting Coin Index")

    if coin in exchange.symbols:
        coin_index = exchange.symbols.index(coin)

    if coin_index > -1:

        print("Gotten Coin Index!")

        time_period = "1m"  # Change this to any time period you want if it's supported by Kraken
                            # I think 1m, 1d, 1y are supported, but 1m is the most useful for us.

        print("3. Getting Price List")

        price_list = await get_price_history(exchange, coin_index, time_period)

        print("Gotten Price List!")

        print("4. Saving To File")

        save_text_file(price_list)

        print("Saved To File!")

    print("5. Closing Connection")

    await exchange.close()


if __name__ == "__main__":
    asyncio.run(main())
    print("Closed Connection!")
