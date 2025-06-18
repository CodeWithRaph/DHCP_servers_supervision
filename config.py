import os
import yaml
import sys

def load_config(yaml_conf, create):
    """
    Read an existing file or creating it (if specified).
    Then return the configuration
    """
    if os.path.exists(yaml_conf):
        try:
            with open(yaml_conf, "r") as fd:
                config = yaml.safe_load(fd)
            return config
        except yaml.YAMLError as e:
            print("\033[31mThe config file may be corrupted.\033[0m")
            return None
    elif create:
        minimal_config="dhcp_hosts_cfg: /etc/dnsmasq.d/hosts.conf\nuser: sae203\n"
        with open(yaml_conf, "w") as fichier:
            fichier.write(minimal_config)
        with open(yaml_conf, "r") as fd:
            config = yaml.safe_load(fd)
        return config
    else:
        print("The file doesn't exists and the create parameter is set to False.")
        return None

def get_dhcp_server(ip, yaml_conf):
    ip = ip.split(".")
    config = load_config(yaml_conf, False)
    for server in config['dhcp-servers']:
        config_entry = {server : config['dhcp-servers'][server]}
        network = config['dhcp-servers'][server].split("/") #separe ip reseaux et masque reseau dans une liste
        network[0] = network[0].split(".") #separe les octets dans une liste
        if network[1] == "24":
            for i in range(0,3):
                octet = network[0][i]
                if octet != ip[i]:
                    config_entry = None
                    break
            #to not return None if the first server fail the test
            if config_entry != None:
                return config_entry
        elif network[1] == "16":
            for i in range(0,2):
                octet = network[0][i]
                if octet != ip[i]:
                    config_entry = None
                    break
            #to not return None if the first server fail the test
            if config_entry != None:
                return config_entry
        elif network[1] == "8":
            if network[0][0] == ip[0]:
                return config_entry
            else:
                config_entry = None
    return config_entry

if __name__ == '__main__':
    if len(sys.argv)== 2 and sys.argv[1] == 'create':
        load_config('config.yaml', True)