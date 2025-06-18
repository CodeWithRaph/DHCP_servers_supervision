# Configuration & Usage

## Comment configurer l'installation
Le produit est personnalisable en fonction de votre réseaux. La modification de la configuration de votre installation se fait dans le fichier `config.yaml`.

Exemple:
```yaml
dhcp_hosts_cfg: /etc/dnsmasq.d/hosts.conf
user: sae203
dhcp-servers:
  10.20.1.5: 10.20.1.0/24
  10.20.2.5: 10.20.2.0/24
```
- **dhcp_host_cfg:** Définit quel fichier de config va être manipulé sur les serveurs dhcp. **Doit toujours commencer par `/etc/dnsmasq.d/`**.
- **user:** est l'utilisateur que vous désignez pour établir la connexion ssh sur les serveurs dhcp.
- **dhcp-servers:** rubrique optionnelle si le réseau ne possède pas encore de serveur dhcp. Mais qu'il faut créer et remplir pour pouvoir agir sur la configuration des serveur dhcp s'il y en a.
Pour chaque serveur dhcp que l'on veut ajouter il faut mettre son **ip** et le **réseau** dans lequel il opère.
## Comment utiliser les commandes

### Commande: add-dhcp-client
#### Description
```bash
python3 add-dhcp-client.py [mac] [ip]
```
Trouve le serveur dhcp qui opère sur le réseau auquel appartient l'ip. Et met à jour la correspondance mac/ip ou la créé si l'adresse mac n'a pas d'adresse ip.
#### Options
- **[mac]:** doit être remplacé par l'**adresse mac de la machine** sur laquelle vous voulez ajouter ou modifier l'ip.
- **[ip]:**  doit être remplacé par l'**ip à attribuer**.
---
### Commande: remove-dhcp-client
#### Description
```bash
python3 remove-dhcp-client.py [mac]
```
Supprime la correspondance mac/ip de la machine qui est ciblée par l'adresse mac.
#### Options
- **[mac]:** doit être remplacé par l'addresse mac de la machine cible.
---
### Commande: check-dhcp
#### Description
```bash
python3 check-dhcp.py [ip]
```
Cherche des erreurs de doublons mac ou ip dans le fichier de config dhcp.
Si le paramètre est présent, uniquement pour le serveur en question. Sinon pour tout les serveurs mentionnés dans le fichier `config.yaml`.
#### Options
- **[ip]:** Paramètre **optionnel**. Doit être remplacé par l'adresse **ip du serveur dhcp** ou l'adresse **ip du réseau** qu'il gère.
---
### Commande: list-dhcp
#### Description
```bash
python3 list-dhcp.py [ip]
```
Affiche les correspondances mac/ip de la config dhcp.
Si le paramètre est présent, uniquement pour le serveur en question. Sinon pour tout les serveurs mentionnés dans le fichier `config.yaml`.
#### Options
- **[ip]:** Paramètre **optionnel**. Doit être remplacé par l'adresse **ip du serveur dhcp** ou son **nom**.