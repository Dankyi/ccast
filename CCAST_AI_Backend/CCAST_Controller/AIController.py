from middleware_orders import *

class AiController:
        
    activeMiddleware = []

    GRID_AMOUNT = 32

    def __init__(self):
        return

    def grid_amount():
        return 32    

    def search_Active_By_ID(self, id):
        for pair in self.activeMiddleware:
            if (pair.id == id): 
                return True
        return False

    def replace_Middleware(self, id, dummy):
        for pair in self.activeMiddleware:
            if (pair.id == id): 
                pair.middleware = Middleware(self.GRID_AMOUNT, dummy)
        return
        
    def add_Pair(self, id, dummy):

        if not self.search_Active_By_ID(id):
            self.activeMiddleware.append(MiddlewarePairs(id, Middleware(self.GRID_AMOUNT, dummy)))
        else:
            self.replace_Middleware(id, dummy)

        print("Current number of Instances: ", len(self.activeMiddleware))

        return

    def remove_Pair(self, id):

        for pair in self.activeMiddleware:
            if pair.id == id:
                self.activeMiddleware.remove(pair)
                print("Removed pair with ID:", pair.id)

                print("Current number of Instances: ", len(self.activeMiddleware))

                return
        
        print("Current number of Instances: ", len(self.activeMiddleware))

        return

class MiddlewarePairs:

    def __init__(self, id, middleware):
        self.id = id
        self.middleware = middleware
        print("Created new pair with ID: ", id)