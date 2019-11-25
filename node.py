from port import Port


class Node:
    """
    :param name:
    :type name: str
    :param port:
    :type port: Port
    :param gateway:
    :type gateway: str
    """
    def __init__(self, name, port, gateway):
        self.name = name
        self.port = port
        self.gateway = gateway

    def __str__(self):
        return '%s %s %s' % (self.name, str(self.port), self.gateway)
