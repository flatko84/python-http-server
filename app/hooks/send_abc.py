import abc

class SendABC(abc.ABC):
    @abc.abstractmethod
    def handle(self, request, response):
        pass