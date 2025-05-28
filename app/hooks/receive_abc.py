import abc

class ReceiveABC(abc.ABC):
    @abc.abstractmethod
    def handle(self, request):
        pass