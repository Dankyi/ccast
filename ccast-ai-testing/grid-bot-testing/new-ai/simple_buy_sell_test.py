import ccxt.async_support as ccxt
from platform import system as operating_system
import asyncio

import middleware_fake_money as middleware


async def main(exchange):

    await exchange.load_markets(True)

    coin_pair = "ETH/BTC"
    coin_pair_id = -1

    if coin_pair in exchange.symbols:
        coin_pair_id = exchange.symbols.index(coin_pair)
    else:
        print("Coin Pair: " + coin_pair + " cannot be found in the exchange!")

    if coin_pair_id > -1:

        exchange_middleware = middleware.Middleware(16)
        coin_pair_split = coin_pair.split("/")

        async def simulate_buy_and_sell(buy_loops):

            current_price = await exchange.fetch_ticker(coin_pair)
            current_price = current_price.__getitem__("last")
            profit_percentage = 1.00005  # 0.005% profit simulation

            balance = exchange_middleware.get_balance()
            print("Starting Balance: "
                  + coin_pair_split[0] + " -> " + str(balance[0])
                  + " | "
                  + coin_pair_split[1] + " -> " + str(balance[1]))

            print()

            for _ in range(buy_loops):

                await exchange_middleware.process_order(exchange, True, coin_pair)  # Do a buy!

                balance = exchange_middleware.get_balance()
                print("Buy: "
                      + coin_pair_split[0] + " -> " + str(balance[0])
                      + " | "
                      + coin_pair_split[1] + " -> " + str(balance[1]))

            print()

            tick = 0
            while tick <= current_price * profit_percentage:  # Actually wait until price goes above threshold

                tick = await exchange.fetch_ticker(coin_pair)
                tick = tick.__getitem__("last")
                difference = abs(tick - (current_price * profit_percentage))

                print("Waiting For: " + str(current_price * profit_percentage)
                      + " | Current Price: " + str(tick)
                      + " | Difference: " + f'{difference:.10f}')

            print()

            await exchange_middleware.process_order(exchange, False, coin_pair)  # Do a sell!

            balance = exchange_middleware.get_balance()
            print("Sell (Ending Balance): "
                  + coin_pair_split[0] + " -> " + str(balance[0])
                  + " | "
                  + coin_pair_split[1] + " -> " + str(balance[1]))

        await simulate_buy_and_sell(3)

    await exchange.close()

if __name__ == "__main__":

    EXCHANGE = ccxt.binance({"verbose": False, "enableRateLimit": True})
    #  For me, I will be using Kraken, but it's slow (fine for long term, which is the intended use), so Binance is good
    #  for testing as it's a lot quicker. (Also good if you just have a Binance account for the real thing)

    if operating_system().upper() == "WINDOWS":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(main(EXCHANGE))
