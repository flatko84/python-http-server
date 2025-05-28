from config import hooks

class Hooks:

    @staticmethod
    def receive(request):
        for hook in hooks.hooks["receive"]:
            request = hook().handle(request)
        return request

    @staticmethod
    def send(request, response):
        for hook in hooks.hooks["send"]:
            response = hook().handle(request, response)
        return response