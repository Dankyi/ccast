

class AiController:
        
    activeMiddleware = []

    def __init__(self):
        return

    def search_Active_By_ID(self, id):
        for pair in self.activeMiddleware:
            if (pair.id == id): 
                return True
        return False

    def replace_middleware(self, id, middleware):
        for pair in self.activeMiddleware:
            if (pair.id == id): 
                pair.middleware = middleware
        return
        
    def add_Pair(self, id, middleware):

        if not self.search_Active_By_ID(id):
            self.activeMiddleware.append(MiddlewarePairs(id, middleware))
        else:
            self.replace_middleware(id, middleware)

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