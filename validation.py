import ipaddress

def is_ipv4_valid(addr):
    """
    Makes sure that an input is an ipv4.
    Then checks this ipv4 is neither multicast, unspecified, reserved, loopback
    nor link local.
    If the ip passes all tests, it return True, else it return False.
    """
    try:
        ipaddress.IPv4Address(addr)
    except ipaddress.AddressValueError:
        # isn't an ipv4
        return False

    ip = ipaddress.ip_address(addr)
    if ip.is_multicast:
        return False
    elif ip.is_unspecified:
        return False
    elif ip.is_reserved:
        return False
    elif ip.is_loopback:
        return False
    elif ip.is_link_local:
        return False
    else:
        return True

def is_mac_valid(addr):
    """
    Return True if a mac address is valid, else return False
    """
    addr = addr.split(":")
    if len(addr)!=6:
        return False
    else:
        for nb in addr:
            if len(nb)!=2:
                # value isn't 2 char long
                return False
            nb = f"0x{nb}"
            try:
                int(nb, 16)
            except ValueError:
                # isn't a hexadecimal number
                return False
        return True