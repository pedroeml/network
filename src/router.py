from router_table import RouterTable


class Router:
    def __init__(self, name, number_of_ports):
        self.name = name
        self.number_of_ports = number_of_ports
        self.ports = []
        self.table = RouterTable()

    def __str__(self):
        string = '%s ' % self.name

        for i in range(self.number_of_ports):
            string += '%s%s\n   ' % (str(i + 1), str(self.ports[i]))

        string += "\n%s" % str(self.table)

        return string

    def add_port(self, port):
        self.ports.append(port)
