from time import perf_counter_ns as stopwatch
import matplotlib.pyplot as plt
import ccxt.async_support as ccxt
import asyncio


async def get_exchange():

    exchange = ccxt.binance({"verbose": False, "enableRateLimit": True})
    await exchange.load_markets(True)

    print("Exchange: " + exchange.name)
    print("Rate Limit: " + str(exchange.rateLimit) + "ms")

    return exchange


async def plot_grid(grid, exchange, coin_pair_id):

    async def get_price_history(ex, c_p_id):

        candle_stick_data = await ex.fetch_ohlcv(ex.symbols[c_p_id], "1d")
        price_history = []

        for candle_stick in candle_stick_data:
            price_history.append(candle_stick[3])

        return price_history[-60:]

    fig, ax = plt.subplots()

    y_axis = await get_price_history(exchange, coin_pair_id)
    x_axis = [x for x in range(len(y_axis))]

    ax.plot(x_axis, y_axis)

    ax.set_yticks(grid, minor=False)
    ax.yaxis.grid(True, which="major")

    plt.show()


async def get_current_price(exchange, coin_pair_id):

    current_price = await exchange.fetch_ticker(exchange.symbols[coin_pair_id])
    current_price = current_price.__getitem__("last")

    return current_price


def calculate_grid(current_price):

    stepping_percentage = 0.01  # Approx. 1% per grid, later AI will determine this itself?
    grid_amount = 32  # Later AI will determine this itself based on how much money the user is investing

    stepping = current_price * stepping_percentage

    increment = current_price
    decrement = current_price
    upper_values = []
    lower_values = []

    grid = []

    for _ in range(grid_amount // 2):  # Half lower, half higher, than current price

        increment += stepping
        decrement -= stepping

        upper_values.append(increment)
        lower_values.append(decrement)

    [grid.append(i) for i in reversed(lower_values)]
    [grid.append(i) for i in upper_values]

    return grid


async def main():

    exchange = await get_exchange()

    coin_pair_id = -1
    coin_pair = "ETH/BTC"

    if coin_pair in exchange.symbols:
        coin_pair_id = exchange.symbols.index(coin_pair)
    else:
        print(coin_pair + " not found in exchange!")

    if coin_pair_id > -1:

        current_price = await get_current_price(exchange, coin_pair_id)
        print("Current Price of " + coin_pair + " -> " + str(current_price))

        s_time = stopwatch()
        grid = calculate_grid(current_price)
        e_time = stopwatch() - s_time
        e_time /= 1_000_000

        print("Grid Calculation Time: " + str(e_time) + "ms")
        print(grid)

        await plot_grid(grid, exchange, coin_pair_id)

    await exchange.close()


if __name__ == "__main__":
    asyncio.run(main())
