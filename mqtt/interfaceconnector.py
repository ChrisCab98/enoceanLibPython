import abc


class IMqttConnector(abc.ABC):

    @abc.abstractmethod
    def Receive(self, server, topic : str, payload : bytes):
        pass

    @abc.abstractmethod
    def Connected(self, server):
        pass

    @abc.abstractmethod
    def Acknowledge(self, server, messageId : int):
        pass