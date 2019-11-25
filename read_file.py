from node import Node
from router import Router
from port import Port
from table_row import TableRow


def read(network, file_name):
    type = 0
    with open(file_name, "r") as file:
        for line in file:
            line = line.replace("\n", "")
            type = read_line(network, line, type)


def read_line(network, line, type=0):
    if line.startswith("#NODE"):
        return 1
    elif line.startswith("#ROUTERTABLE"):
        return 3
    elif line.startswith("#ROUTER"):
        return 2
    else:
        line_items = line.split(",")

        if type == 1:
            network.nodes.append(create_node(line_items))
        elif type == 2:
            network.routers.append(create_router(line_items))
        elif type == 3:
            add_router_table(network, line_items)

        return type


def create_node(line_items):
    line_items[3] = line_items[3].strip("\r")
    p = Port(line_items[1], line_items[2].split('/')[0], line_items[3])
    n = Node(line_items[0], p, line_items[4])
    return n


def create_router(line_items):
    r = Router(line_items[0], int(line_items[1]))
    i = 0
    for index in range(2, len(line_items), 3):
        p = Port(line_items[index], line_items[index+1].split('/')[0], line_items[index+2])
        r.add_port(p)
    return r


def add_router_table(network, line_items):
    r = TableRow(line_items[1].split('/')[0], line_items[2], int(line_items[3]))
    for n in network.routers:
        if n.name == line_items[0]:
            n.table.add(r)
