import ccxt.async_support as ccxt
import asyncio


async def buy():
    pass


async def sell():
    pass


if __name__ == "__main__":

    """
    
    This main method won't be here in the finished version of this code as its methods will be called from the AI
    
    """

    API_CREDENTIALS = {"KEY": "", "SECRET": ""}

    with open("my-api-keys.txt", "r") as api_key_file:

        api_keys = api_key_file.readlines()[0].split(",")
        API_CREDENTIALS["KEY"] = api_keys[0]
        API_CREDENTIALS["SECRET"] = api_keys[1]

    """
    
    The user must generate keys from an exchange of their choice (from what we support). The exchange itself should have
    a tutorial on how to do this.
    
    In the finalised software, the front-end should ask for the API Key and the Secret/Private Key and allow them to
    paste it in, and then those two should be encrypted and stored in the user database.
    
    For the purposes of this test, store your keys in a text file called "my-api-keys.txt" on the same line, separated
    by a comma, like this: key1,key2
    
    """

    pass
