

def icmp_echo_request(src_name, dest_name, src_ip, dest_ip, ttl, src_mac, dest_mac, data='', mf='0', off='0'):
    write_line('%s => %s : ETH (src=%s dst=%s) \\n IP (src=%s dst=%s ttl=%s mf=%s off=%s) \\n ICMP - Echo request (data=%s);' % (src_name, dest_name, src_mac, dest_mac, src_ip, dest_ip, ttl, mf, off, data))


def icmp_echo_reply(src_name, dest_name, src_ip, dest_ip, ttl, src_mac, dest_mac, data='', mf='0', off='0'):
    write_line('%s => %s : ETH (src=%s dst=%s) \\n IP (src=%s dst=%s ttl=%s mf=%s off=%s) \\n ICMP - Echo reply (data=%s);' % (src_name, dest_name, src_mac, dest_mac, src_ip, dest_ip, ttl, mf, off, data))


def icmp_time_exceeded(src_name, dest_name, src_ip, dest_ip, src_mac, dest_mac, ttl):
    write_line('%s => %s : ETH (src=%s dst=%s) \\n IP (src=%s dst=%s ttl=%s) \\n ICMP - Time Exceeded;' % (src_name, dest_name, src_mac, dest_mac, src_ip, dest_ip, ttl))


def icmp_rbox(src_name, dest_name, data=''):
    write_line('%s rbox %s : Received %s;' % (src_name, dest_name, data))


def arp_request(src_name, dest_ip, src_ip, src_mac):
    write_line('%s box %s : ETH (src=%s dst=FF:FF:FF:FF:FF:FF) \\n ARP - Who has %s? Tell %s;' % (src_name, src_name, src_mac, dest_ip, src_ip))


def arp_reply(src_name, dest_name, src_ip, src_mac, dest_mac):
    write_line('%s => %s : ETH (src=%s dst=%s) \\n ARP - %s is at %s;' % (src_name, dest_name, src_mac, dest_mac, src_ip, src_mac))


def write_line(line):
    with open('output.txt', 'a') as file:
        file.write(line + '\n')
