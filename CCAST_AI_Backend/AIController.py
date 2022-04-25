import os
from AI_System import ai
from order_middleware import *
import ccxt.async_support as ccxt
import configparser
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

    def makeAIInstance(self, dummy, key, secret):

        cwd = os.getcwd()
        filename = cwd + "\config.ini"

        if not os.path.exists(filename):
            filename = cwd + "/config.ini" # Try using / instead of \

            if not os.path.exists(filename):
                print("File not found: ", filename)
                quit()
        

        config = configparser.ConfigParser()
        config.read(filename)

        public_key = key
        private_key = secret

        EXCHANGE = ccxt.ftx({"verbose": False, "enableRateLimit": True, "apiKey": public_key, "secret": private_key})

        coin_pair = config['instance_info']['coin_pair']
        buy_grid_percentage = float(config['instance_info']['buy_grid_percentage'])
        sell_grid_percentage = float(config['instance_info']['sell_grid_percentage'])

        AI = ai.AIGridBot(EXCHANGE, dummy, coin_pair, buy_grid_percentage, sell_grid_percentage)
        return AI
        
        
    def add_Pair(self, id, dummy, key, secret, coin):
        
        self.activeMiddleware[id] = AIPairs(id, self.makeAIInstance(dummy, key, secret, coin))       
        print("Current number of Instances: ", len(self.activeMiddleware))
        self.activeMiddleware[id].start()
        print("Started AI")
        return

    def add_Pair_Read(self, id, dummy, key, secret):
        
        self.activeMiddleware[id] = AIPairs(id, self.makeAIInstance(dummy, key, secret))       
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
            dummy = ai.get_type()
            if (dummy):
                return 'Dummy'
            else:
                return 'Live'
        else:
            return 'Idle'

    def info(self, id):

        if id in self.activeMiddleware:
            return self.activeMiddleware[id].get_information()

        return "No Data Retrieved"

class AIPairs:

    def __init__(self, id, ai):
        self.id = id
        self.ai = ai
        print("Created new pair with ID: ", id)

    def get_type(self):        
        dummy = self.ai.get_information()["Dummy"]
        return dummy

    def get_information(self):        
        return self.ai.get_information()

    def start(self):
        self.ai.start()

    def stop(self):
        self.ai.stop()