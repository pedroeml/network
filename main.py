import sys
import read_file
import simulation
from network import Network


if __name__ == "__main__":
    with open('output.txt', 'w') as file:
        file.write('')

    simulation_file_name = sys.argv[1]

    network = Network([], [])
    read_file.read(network, simulation_file_name)

    nodes = network.nodes
    routers = network.routers

    simulation.start(network, sys.argv[2], sys.argv[3], sys.argv[4])

    with open('output.txt', 'r') as file:
        print(file.read())

    # for node in nodes:
    #     print(node)
    # for router in routers:
    #     print(router)
