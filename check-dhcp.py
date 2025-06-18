import validation as vld
import config
import dhcp
import sys

def error_finder(liste_correspondance, type):
    """
    Set type parameter to mac or ip and it detects
    duplicated mac or ip in the correspondance list.
    Return the list of duplicate
    """
    liste_totale = []
    liste_double = []
    for each in liste_correspondance:
        liste_totale.append(each[type])
    n=0
    for target in liste_totale:
        for each in liste_totale:
            if target == each:
                n+=1
        if n >= 2:
            liste_double.append(target)
        n=0
    return liste_double

def dhcp_error_finder(ip, fichier_conf):
    """
    check if there is mac or ip duplicated in the config file
    """
    liste_correspondance = dhcp.dhcp_list(ip, fichier_conf)

    #mac error finder
    liste_mac_double = error_finder(liste_correspondance, "mac")
    if len(liste_mac_double) != 0:
        print(f"\033[31m=== Error - server dhcp {ip} ===\033[0m") # separator
        print("Duplicated MAC addresses:")
        for each in liste_correspondance:
            if each['mac'] in liste_mac_double:
                print(f"dhcp-host={each['mac']},{each['ip']}")

    #ip error finder
    liste_ip_double = error_finder(liste_correspondance, "ip")
    #makes a separator if there is only duplicated ip
    if len(liste_mac_double) == 0 and len(liste_ip_double) != 0:
        print(f"\033[31m=== Error - server dhcp {ip} ===\033[0m")
    elif len(liste_mac_double) == 0 and len(liste_ip_double) == 0:
        print(f"\033[32m=== Coherent configuration - serveur dhcp {ip} ===\033[0m")

    if len(liste_ip_double) != 0:
        print("Duplicated IP addresses:")
        for each in liste_correspondance:
            if each['ip'] in liste_ip_double:
                print(f"dhcp-host={each['mac']},{each['ip']}")

def check_dhcp(ip=None):
    """
    Check the ip/mac configuration coherence of a specified dhcp server.
    Or check it for each dhcp server inscribed in the yaml config file.
    """
    yaml_conf = "config.yaml"
    configuration = config.load_config(yaml_conf, True)
    fichier_conf = configuration['dhcp_hosts_cfg']
    if ip == None:
        #we check every server
        for ip in configuration['dhcp-servers']:
            dhcp_error_finder(ip, fichier_conf)
    else:
        #we only check the server that match the ip
        server = config.get_dhcp_server(ip, yaml_conf)
        if server == None:
            print("\033[31mCannot identify DHCP server.\033[0m")
        else:
            for ip in server:
                dhcp_error_finder(ip, fichier_conf)

def main():
    if len(sys.argv) == 1:
        check_dhcp()
    elif len(sys.argv) == 2:
        ip = sys.argv[1]
        check_dhcp(ip)
    else:
        print("this command has one optionnal parameter: server (ip or network)")

if __name__ == '__main__':
    main()