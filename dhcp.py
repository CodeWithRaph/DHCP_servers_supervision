from fabric import Connection
import paramiko
import os
import getpass
import config

configuration = config.load_config("config.yaml", True)
user = configuration['user']

# ssh connection with key
private_key_path = os.path.expanduser("~/.ssh/id_rsa")
passphrase = getpass.getpass("Entrez la passphrase de votre clé privée : ")

try:
    pkey = paramiko.RSAKey.from_private_key_file(private_key_path, password=passphrase)
except paramiko.ssh_exception.SSHException:
    print("\33[31mWrong passphrase.\33[0m")
    exit(1) #to avoid errors following the previous
except ValueError:
    print("\33[31mPassphrase is required.\33[0m")
    exit(1) #to avoid errors following the previous

def ip_other_mac_exists(ssh, ip, mac, fichier_conf):
    """
    Return true if the ip is already used by a host with another mac address.
    Else return false.
    """
    ip_enscribed = ssh.sudo(f'grep -o {ip} {fichier_conf} | grep -v {mac}',warn=True, hide=True)
    return ip_enscribed.ok

def mac_exists(ssh, mac, fichier_conf):
    """
    Return true if the mac addresse is already used.
    Else return false.paramiko.RSAKey.from_private_key_file(...
    """
    mac_enscribed = ssh.sudo(f'grep -o dhcp-host={mac} {fichier_conf}',warn=True, hide=True)
    return mac_enscribed.ok

def dhcp_add(ip, mac, server, fichier_conf):
    """
    Return true if ip/mac correspondance has been successfully
    added the the dhcp configuration.
    Else return false.
    """
    ssh = Connection(host=server,user=user,connect_kwargs={"pkey":pkey})
    ssh.sudo(f'touch {fichier_conf}') #create the file it doesn't exists
    if mac_exists(ssh, mac, fichier_conf):
        #the mac is already enscribed
        if ip_other_mac_exists(ssh, ip, mac, fichier_conf):
            print("\033[31merror: IP address already in use.\033[0m")
        else:
            #the ip isn't already used => update
            ssh.sudo(f"sed -i '/{mac}/c\\dhcp-host={mac},{ip}' {fichier_conf}")
            ssh.sudo(f'systemctl restart dnsmasq')
            print(f"\33[32mMac successfully updated on {server}.\33[0m")
    else:
        #the mac isn't already enscribed
        if ip_other_mac_exists(ssh, ip, mac, fichier_conf):
            print("\033[31merror: IP address already in use.\033[0m")
        else:
            #no conflict => add
            ssh.sudo(f"bash -c 'echo \"dhcp-host={mac},{ip}\" >> {fichier_conf}'")
            ssh.sudo(f'systemctl restart dnsmasq')
            print(f"\33[32mMac successfully added on {server}.\33[0m")

def dhcp_remove(mac, server, fichier_conf):
    """
    Return true if a mac/ip correspondance has been successfully removed.
    Else return false.
    """
    ssh = Connection(host=server,user=user,connect_kwargs={"pkey":pkey})
    ssh.sudo(f'touch {fichier_conf}') #create the file it doesn't exists
    if mac_exists(ssh, mac, fichier_conf):
        #the mac is effectively here
        ssh.sudo(f'sed -i "/{mac}/d" {fichier_conf}')
        ssh.sudo(f'systemctl restart dnsmasq')
        print(f"\33[32mMac successfully removed on {server}.\33[0m")
        return True
    else:
        print(f"\033[31mMac address not found on {server}.\033[0m")
        return False

def dhcp_list(server, fichier_conf):
    """
    return a list that contains the mac/ip association in a specified server config
    """
    ssh = Connection(host=server,user=user,connect_kwargs={"pkey":pkey})
    
    ssh.sudo(f'touch {fichier_conf}') #create the file it doesn't exists
    texte = ssh.sudo(f"cat {fichier_conf}", hide =True)
    texte = str(texte).split('\n')
    #if the file is empty
    if texte[1] == "(no stdout)":
        return {}
    else:
        liste_correspondance = []
        i=2
        while i <= len(texte) and texte[i] != "": #filtering fabric output
            if(texte[i][0]!= "#"): #we keep only the line that are not a comment
                mac_ip=""
                for j in range(10,len(texte[i])):
                    mac_ip+=texte[i][j]
                mac_ip = mac_ip.split(",")
                liste_correspondance.append({"mac": mac_ip[0], "ip": mac_ip[1]})
            i+=1
        return liste_correspondance