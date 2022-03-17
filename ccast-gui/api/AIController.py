

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

    def replace_middleware(self, id, dummy):
        for pair in self.activeMiddleware:
            if (pair.id == id): 
                pair.middleware = CCAST_AI_Backend.Middleware.middleware_orders.Middleware(self.GRID_AMOUNT, dummy)
        return
        
    def add_Pair(self, id, dummy):

        if not self.search_Active_By_ID(id):
            self.activeMiddleware.append(MiddlewarePairs(id, CCAST_AI_Backend.Middleware.middleware_orders.Middleware(self.GRID_AMOUNT, dummy)))
        else:
            self.replace_middleware(id, dummy)

        return

    def remove_Pair(self, id):

        for pair in self.activeMiddleware:
            if pair.id == id:
                self.activeMiddleware.remove(pair)
                print("Removed pair with ID:", pair.id)
                return

        return

class MiddlewarePairs:

    def __init__(self, id, middleware):
        self.id = id
        self.middleware = middleware
        print("Created new pair with ID: ", id)