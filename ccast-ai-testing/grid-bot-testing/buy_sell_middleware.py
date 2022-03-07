import ccxt.async_support as ccxt
from platform import system as operating_system
import asyncio


async def get_balance(exchange):

    balances = {}

    exchange_balance_dict = await exchange.fetch_balance()
    exchange_balance_dict = exchange_balance_dict["info"]["result"]

    for balance in exchange_balance_dict:

        if float(exchange_balance_dict[balance]) > 0:
            balances[balance] = float(exchange_balance_dict[balance])

    print(balances)  # For debug purposes

    return balances


async def get_order_book(exchange, coin_pair):

    order_book = await exchange.fetch_order_book(coin_pair)

    print("Bids:", order_book["bids"])  # For debug purposes
    print("Asks:", order_book["asks"])  # For debug purposes

    return {"BIDS": order_book["bids"], "ASKS": order_book["asks"]}


async def process_order(exchange, side, coin_pair):

    """

    The "side" of an order refers to a buy or a sell, so I just use a boolean value to represent it.

    True (1) is analogous to "buy"
    False (0) is analogous to "sell"

    I prefer to rename the "symbol" to "coin_pair", but this is the pair of currencies that you want to trade.
    For example, ETH/BTC, or BTC/USDT, et al.

    For BUYING, ETH/BTC means that you are buying an amount of ETH and paying for it with an amount of BTC.
    For SELLING, ETH/BTC means you are selling an amount of ETH and receiving an amount of BTC.

    """

    if side:  # Buy

        pass

    else:  # Sell

        pass


async def main(exchange):

    await get_balance(exchange)
    # await get_order_book(exchange, "ETH/BTC")
    await process_order(exchange, True, "ETH/BTC")
    # await process_order(exchange, False)

    await exchange.close()


if __name__ == "__main__":

    """
    
    This main method won't be here in the finished version of this code as its methods will be called from the AI
    
    """

    API_CREDENTIALS = {"KEY": "", "SECRET": ""}

    with open("my-api-keys.txt", "r") as api_key_file:

        api_keys = api_key_file.readlines()[0].split(",")

        API_CREDENTIALS["KEY"] = api_keys[0]
        API_CREDENTIALS["SECRET"] = api_keys[1]

        api_keys = None

    EXCHANGE = ccxt.kraken({"verbose": False, "enableRateLimit": True,
                            "apiKey": API_CREDENTIALS["KEY"], "secret": API_CREDENTIALS["SECRET"]})

    API_CREDENTIALS = None

    """
    
    The user must generate keys from an exchange of their choice (from what we support). The exchange itself should have
    a tutorial on how to do this.
    
    In the finalised software, the front-end should ask for the API Key and the Secret/Private Key and allow them to
    paste it in, and then those two should be encrypted and stored in the user database.
    
    For the purposes of this test, store your keys in a text file called "my-api-keys.txt" on the same line, separated
    by a comma, like this: apikey,secretkey
    
    If you don't use Kraken (I did), then change ccxt.kraken(..) to whatever exchange you used.
    
    Also, it's important you call the file my-api-keys.txt because I included that name in the .gitignore file, so you
    won't ever be able to accidentally push your secret keys onto GitHub
    
    """

    if operating_system().upper() == "WINDOWS":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(main(EXCHANGE))

