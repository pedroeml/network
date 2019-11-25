
class Port:
    def __init__(self, mac_address, ip_address, mtu):
        self.mac_address = mac_address
        self.ip_address = ip_address
        self.mtu = mtu

    def __str__(self):
        return '(%s - %s - %d)' % (self.mac_address, self.ip_address, self.mtu)
