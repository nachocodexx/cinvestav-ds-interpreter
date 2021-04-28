from abc import ABC,abstractmethod
class Node(ABC):
    def __init__(self, ip,nodeId):
        self.ip     = ip
        self.nodeId = nodeId
    @abstractmethod
    def run(client):
        pass

