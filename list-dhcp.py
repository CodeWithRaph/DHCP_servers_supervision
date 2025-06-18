import validation as vld
import config
import dhcp
import sys

def list_single_dhcp(ip, fichier_conf):
    """
    list the ip mac association of a config file
    """
    liste_correspondance = dhcp.dhcp_list(ip, fichier_conf)
    for line in liste_correspondance:
        print(f"{line['mac']}\t\t{line['ip']}")

def list_dhcp(ip=None):
    """
    List the ip/mac configuration of a specified dhcp server.
    Or list it for each dhcp server inscribed in the yaml config file.
    """
    yaml_conf = "config.yaml"
    configuration = config.load_config(yaml_conf, True)
    fichier_conf = configuration['dhcp_hosts_cfg']
    if ip == None:
        #we check every server
        for ip in configuration['dhcp-servers']:
            print(f"\033[34m=== dhcp server {ip} ===\033[0m")
            list_single_dhcp(ip, fichier_conf)
    else:
        #we only check the server that match the ip
        server = config.get_dhcp_server(ip, yaml_conf)
        if server == None:
            print("\033[31mCannot identify DHCP server.\033[0m")
        else:
            list_single_dhcp(ip, fichier_conf)

def main():
    if len(sys.argv) == 1:
        list_dhcp()
    elif len(sys.argv) == 2:
        ip = sys.argv[1]
        list_dhcp(ip)
    else:
        print("this command has one optionnal parameter: server (ip or name)")

if __name__ == '__main__':
    main()