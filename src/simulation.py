from node import Node
import write_file

current_hop = ''
current_hop_port = -1
next_hop = ''
next_hop_port = -1
dest_ip = ''
src_ip = ''
ttl = -1
data_chunks = []


def start(network, source_name, destination_name, data):
    global current_hop, current_hop_port, next_hop, next_hop_port, dest_ip, ttl, src_ip, data_chunks

    ttl = 8

    for n in network.nodes:
        # find the src and dest
        if source_name == n.name:
            src_ip = n.port.ip_address
            current_hop = n
        if destination_name == n.name:
            dest_ip = n.port.ip_address

    simulate(network, True, data)

    ttl = 8
    for n in network.nodes:
        if destination_name == n.name:
            src_ip = n.port.ip_address
            current_hop = n
        if source_name == n.name:
            dest_ip = n.port.ip_address

    simulate(network, False, data)


def simulate(network, is_arp, data):
    global dest_ip, ttl, src_ip
    global current_hop, current_hop_port, next_hop, next_hop_port
    find_first_hop_from_node(network, current_hop, dest_ip, is_arp)

    if is_arp:
        send_icmp("request", data)
    else:
        send_icmp("reply", data)

    current_hop = next_hop
    current_hop_port = next_hop_port

    while get_ip_from_current_hop() != dest_ip:     # while it's not on destination
        ttl -= 1
        if ttl == 0:    # stop the simulation
            write_file.icmp_time_exceeded(current_hop.name, next_hop.name, src_ip, dest_ip, current_hop.ports[current_hop_port].mac_address, next_hop.ports[next_hop_port].mac_address, str(ttl))
            break

        find_next_hop_from_router(network, dest_ip, is_arp)
        if is_arp:
            send_icmp("request", data)
        else:
            send_icmp("reply", data)
        current_hop = next_hop
        current_hop_port = next_hop_port


def get_ip_from_current_hop():
    global current_hop, current_hop_port

    if current_hop_port == -1:
        return current_hop.port.ip_address
    else:
        return current_hop.ports[current_hop_port].ip_address


def is_ip_in_same_network(ip_address_a, ip_address_b):
    ip_address_a = ip_address_a.split(".")
    ip_address_b = ip_address_b.split(".")
    first_digits = int(ip_address_a[0])
    mask = 0

    if first_digits < 128:    # if it's in class A (mask: 255.0.0.0)
        mask = 1
    elif first_digits < 192:   # if it's in class B (mask: 255.255.0.0)
        mask = 2
    elif first_digits < 224:   # if it's in class C (mask: 255.255.255.0)
        mask = 3

    for i in range(0, mask):
        if ip_address_a[i] != ip_address_b[i]:
            return False
    return True


def find_first_hop_from_node(network, node, dest_ip, is_arp):
    global next_hop, next_hop_port

    if is_ip_in_same_network(node.port.ip_address, dest_ip):
        for n in network.nodes:
            if n.port.ip_address == dest_ip:
                if is_arp:
                    write_file.arp_request(node.name, n.port.ip_address, node.port.ip_address, node.port.mac_address)
                    write_file.arp_reply(n.name, node.name, n.port.ip_address, n.port.mac_address, node.port.mac_address)
                next_hop = n
                next_hop_port = -1
                return

    for r in network.routers:
        for i in range(len(r.ports)):
            if r.ports[i].ip_address == node.gateway:   # get node gateway
                if is_arp:
                    write_file.arp_request(node.name, r.ports[i].ip_address, node.port.ip_address, node.port.mac_address)
                    write_file.arp_reply(r.name, node.name, r.ports[i].ip_address, r.ports[i].mac_address, node.port.mac_address)
                next_hop = r
                next_hop_port = i
                return


def find_next_hop_from_router(network, dest_ip, is_arp):
    global current_hop, current_hop_port, next_hop, next_hop_port

    row = None
    for row in current_hop.table.rows:
        # check the routing table to see which port the destination is
        if is_ip_in_same_network(row.destination, dest_ip):
            next_hop = row.next_hop
            current_hop_port = row.port
            break

    if next_hop == '0.0.0.0':   # if ip from next is 0.0.0.0 search nodes for the destination
        next_hop_port = -1
        for n in network.nodes:
            if n.port.ip_address == dest_ip:
                if is_arp:
                    write_file.arp_request(current_hop.name, dest_ip, current_hop.ports[current_hop_port].ip_address, current_hop.ports[current_hop_port].mac_address)
                    write_file.arp_reply(n.name, current_hop.name, dest_ip, n.port.mac_address, current_hop.ports[current_hop_port].mac_address)
                next_hop = n
                return
    else:   # search for routers to find the next hop and its port
        for r in network.routers:
            for i in range(len(r.ports)):
                good_to_go = False
                try:
                    good_to_go = r.ports[i].ip_address == next_hop.gateway
                except:
                    try:
                        good_to_go = r.ports[i].ip_address == row.next_hop
                    except:
                        good_to_go = r.ports[i].ip_address in [port.ip_address for port in next_hop.ports]

                if good_to_go:
                    if is_arp:
                        write_file.arp_request(current_hop.name, r.ports[i].ip_address, current_hop.ports[current_hop_port].ip_address, current_hop.ports[current_hop_port].mac_address)
                        write_file.arp_reply(r.name, current_hop.name, r.ports[i].ip_address, r.ports[i].mac_address, current_hop.ports[current_hop_port].mac_address)

                    next_hop = r
                    next_hop_port = i
                    return


def send_icmp(r, data):
    global current_hop, current_hop_port, next_hop, next_hop_port, dest_ip, ttl, data_chunks

    src_mac = current_hop.port.mac_address if type(current_hop) is Node else current_hop.ports[current_hop_port].mac_address
    dest_mac = next_hop.port.mac_address if type(next_hop) is Node else next_hop.ports[next_hop_port].mac_address
    mtu = current_hop.port.mtu if type(current_hop) is Node else current_hop.ports[current_hop_port].mtu

    if len(data_chunks) != 0:
        data_chunks = [chunk[i:i+mtu] for chunk in data_chunks for i in range(0, len(chunk), mtu)]
    else:
        data_chunks = [data[i:i+mtu] for i in range(0, len(data), mtu)]

    off = 0
    for i in range(len(data_chunks)):
        chunk = data_chunks[i]
        mf = 1 if i != len(data_chunks) - 1 else 0

        if r == "reply":    # if the type is reply
            write_file.icmp_echo_reply(current_hop.name, next_hop.name, src_ip, dest_ip, str(ttl), src_mac, dest_mac, chunk, str(mf), str(off))
        else:
            write_file.icmp_echo_request(current_hop.name, next_hop.name, src_ip, dest_ip, str(ttl), src_mac, dest_mac, chunk, str(mf), str(off))

        off += len(chunk)

    if type(next_hop) is Node:
        write_file.icmp_rbox(next_hop.name, next_hop.name, ''.join(data_chunks))
