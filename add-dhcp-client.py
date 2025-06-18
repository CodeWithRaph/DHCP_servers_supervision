import validation as vld
import config
import dhcp
import sys

def add_dhcp_client(mac, ip):
    yaml_conf = 'config.yaml'
    configuration = config.load_config(yaml_conf, True)
    fichier_conf = configuration['dhcp_hosts_cfg']

    if vld.is_ipv4_valid(ip):
        if vld.is_mac_valid(mac):
            #both parameters are valid so we can pursue
            servers = config.get_dhcp_server(ip, yaml_conf)
            if servers == None:
                print("\33[31mUnable to identify DHCP server.\33[0m")
            else:
                for server in servers:
                    dhcp.dhcp_add(ip, mac, server, fichier_conf)
        else:
            print("\033[31merror: bad MAC address.\033[0m")
    else:
        print("\033[31merror: bad IP address.\033[0m")

def main():
    
    if len(sys.argv) != 3:
        print("this command requires 2 arguments: mac & ip")
    else:
        mac = sys.argv[1]
        ip = sys.argv[2]
        add_dhcp_client(mac, ip)

if __name__ == '__main__':
    main()