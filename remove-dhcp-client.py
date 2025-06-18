import validation as vld
import config
import dhcp
import sys

def remove_dhcp_client(mac):
    yaml_conf = "config.yaml"
    if vld.is_mac_valid(mac):
        #the parameter is valid so we can pursue
        yaml_conf = config.load_config(yaml_conf, True)
        for server in yaml_conf['dhcp-servers']:
            dhcp.dhcp_remove(mac ,server, yaml_conf['dhcp_hosts_cfg'])
    else:
        print("\033[31merror: bad MAC address.\033[0m")

def main():
    if len(sys.argv) != 2:
        print("this command requires the following argument: mac")
    else:
        mac = sys.argv[1]
        remove_dhcp_client(mac)
    

if __name__ == '__main__':
    main()