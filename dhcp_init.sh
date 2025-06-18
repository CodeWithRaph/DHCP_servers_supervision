#!/bin/bash

#parameter that you need to set
user=""
rsa_pub_key_file=""

#############################################

#script automation
if [ "$user" = "" ]; then
    echo "User parameter not yet set."
elif [ "$rsa_pub_key_file" = "" ]; then
    echo "The parameter that ensure the path toward the central server's public key copy is not yet set."
else
    restriction="ALL=(ALL) NOPASSWD: /bin/systemctl restart dnsmasq, /bin/cat /etc/dnsmasq.d/*, /usr/bin/sed -i */etc/dnsmasq.d/*, /usr/bin/echo *>> /etc/dnsmasq.d/*, /usr/bin/bash -c *echo *>> /etc/dnsmasq.d/*, /usr/bin/touch /etc/dnsmasq.d/*, /usr/bin/grep * /etc/dnsmasq.d*"
    restriction_sudoers="$user $restriction"

    public_key=$(cat $rsa_pub_key_file)
    cmd_limiter_caller="command="~/.ssh/cmd_limiter.py",no-port-forwarding,no-X11-forwarding,no-agent-forwarding"
    authorized_line="$cmd_limiter_caller $public_key"

    #Allow the sudo use without password for specified cmd
    sudo bash -c 'echo "$1" >> /etc/sudoers.d/cmd_no_passwd' _ "$restriction_sudoers"

     #creating the ssh limiter script
    cat <<'EOF' > ~/.ssh/cmd_limiter.py
#!/usr/bin/env python3
import os
import sys
import subprocess
from fnmatch import fnmatch

# Collect ssh cmd
cmd = os.environ.get('SSH_ORIGINAL_COMMAND', '')

# Allowed patterns
patterns = [
    "sudo*systemctl restart dnsmasq",
    "sudo*cat /etc/dnsmasq.d/*",
    "sudo*sed -i */etc/dnsmasq.d/*",
    "sudo*echo *>> /etc/dnsmasq.d/*",
    "sudo*bash -c *echo *>> /etc/dnsmasq.d/*",
    "sudo*touch /etc/dnsmasq.d/*",
    "sudo*grep * /etc/dnsmasq.d*"
]

# Check and execute
if '&' in cmd or ';' in cmd:
    print("UNAUTHORIZED COMMAND")
elif any(fnmatch(cmd, p) for p in patterns):
    proc = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    sys.stdout.buffer.write(proc.stdout)
    sys.stderr.buffer.write(proc.stderr)
    sys.exit(proc.returncode)
else:
    print("UNAUTHORIZED COMMAND")
EOF

    #giving it executive permissions for proprietory
    sudo chmod 744 ~/.ssh/cmd_limiter.py

    #adding the central server to authorized ssh client with the script that limits the cmd use
    echo $authorized_line >> ~/.ssh/authorized_keys
fi