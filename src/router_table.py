
class RouterTable:
    def __init__(self):
        self.rows = []

    def __str__(self):
        string = "Destination     NextHop         Port \n"

        for row in self.rows:
            string += str(row) + "\n"

        return string

    def add(self, row):
        self.rows.append(row)
