
class TableRow:
    def __init__(self, destination, next_hop, port):
        self.destination = destination
        self.next_hop = next_hop
        self.port = port

    def __str__(self):
        d = 16 - len(self.destination)
        string = self.destination
        for i in range(d):
            string += " "

        d = 16 - len(self.next_hop)
        string += self.next_hop
        for i in range(d):
            string += " "

        return string + str(self.port)
