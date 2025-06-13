from config import hooks
from lib.request import Request
from lib.response import Response

class Hooks:
    @staticmethod
    def receive(request: Request) -> Request:
        """Execute receive hook."""
        for hook in hooks.hooks["receive"]:
            request = hook().handle(request)
        return request

    @staticmethod
    def send(request: Request, response: Response) -> Response:
        """Execute response hook."""
        for hook in hooks.hooks["send"]:
            response = hook().handle(request, response)
        return response