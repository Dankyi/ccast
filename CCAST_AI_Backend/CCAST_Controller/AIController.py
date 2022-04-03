from AI_System import ai
from order_middleware import *
import ccxt.async_support as ccxt
import time

class AiController:
        
    activeMiddleware = {}

    def __init__(self):
        return

    def grid_amount(self):
        return self.GRID_AMOUNT

    def search_Active_By_ID(self, id):
        return self.activeMiddleware[id] != None               


    def makeAIInstance(self, dummy, key, secret, coin):
        
        #TODO Pass a variable for each of the values defined.

        lower_percentage = 0.0005
        profit_percentage = 0.001

        EXCHANGE = ccxt.ftx({"verbose": False, "enableRateLimit": True, "apiKey": key, "secret": secret})
        AI = ai.AIGridBot(EXCHANGE, dummy, coin, lower_percentage, profit_percentage)  # Dummy  True = Fake, False = Real
        return AI
        
    def add_Pair(self, id, dummy, key, secret, coin):
        
        self.activeMiddleware[id] = AIPairs(id, self.makeAIInstance(dummy, key, secret, coin))       
        print("Current number of Instances: ", len(self.activeMiddleware))
        self.activeMiddleware[id].start()
        print("Started AI")
        return

    def remove_Pair(self, id):
        if id in self.activeMiddleware:  
            self.activeMiddleware[id].stop()
            print("Stopping AI")
            del self.activeMiddleware[id]        
            print("Removed pair with ID:", id)
            print("Current number of Instances: ", len(self.activeMiddleware))
            
        return
        

    def status(self, id):
        
        if id in self.activeMiddleware:  

            ai = self.activeMiddleware[id]
            live = ai.get_type()
            if (live):
                return 'Live'
            else:
                return 'Dummy'
        else:
            return 'Idle'

    async def info(self, id):

        if id in self.activeMiddleware:
            return self.activeMiddleware[id].get_information()

        return 0

class AIPairs:

    def __init__(self, id, ai):
        self.id = id
        self.ai = ai
        print("Created new pair with ID: ", id)

    def get_information(self):        
        return self.ai.get_information()

    def start(self):
        self.ai.start()

    def stop(self):
        self.ai.stop()