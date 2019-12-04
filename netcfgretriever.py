@@ -0,0 +1,62 @@
#!/usr/bin/env python3
#
# netcfgretriever.py
# ver 0.3 - 20191204
#
# given a CSV in below format, connects to a client via SSH,
#     runs a sequence of commands, and saves cfg to a file
#
# ip,username,password,hostname
# e.g.
#     192.168.13.37,escollapse,s3cr3t,nerdbox
#     ***NOTE: no spaces
#
# **************
# * escollapse *
# * CISSP, PT+ *
# *  20191129  *
# **************

from paramiko import client
from paramiko import ssh_exception
from time import sleep

TARGETSFILE = "/absolute/path/to/CSV/file.txt"
TARGETS = []
#                                                  V--- NOTE: trailing '/'
DESTDIR = "/absolute/path/to/cfg-file/save/location/"

# never hardcode cred's...
with open("/absolute/path/to/enablepw.txt", 'r') as f:
    ENABLEPW = f.read().rstrip('\n')
CMDSEQ = ["enable", "terminal length 0", "show running-config", "terminal length 24", "disable", "exit"]

with open(TARGETSFILE, 'r') as f:
    for line in f:
        ip, username, password, hostname = line.split(',')
        target = {"ip": ip, "username": username, "password": password, "hostname": hostname.rstrip('\n')}
        TARGETS.append(target)

connection = client.SSHClient()
connection.set_missing_host_key_policy(client.AutoAddPolicy)

for i in range(len(TARGETS)):
    ofile = DESTDIR + TARGETS[i]["hostname"] + ".txt"
    try:
        connection.connect(hostname=TARGETS[i]["ip"], username=TARGETS[i]["username"], password=TARGETS[i]["password"])
        channel = connection.invoke_shell()
        for j in range(len(CMDSEQ)):
            channel.send(CMDSEQ[j] + "\n")
            sleep(1)
            if CMDSEQ[j] == "enable":
                channel.send(ENABLEPW + "\n")
                sleep(1)
            elif CMDSEQ[j] == "show running-config":
                with open(ofile, 'a') as f:
                    f.write(channel.recv(9999).decode("ascii"))
    except ssh_exception.SSHException:
        print("Target {}: SSH Exception!".format(TARGETS[i]["ip"]))
    except ssh_exception.AuthenticationException:
        print("Target {}: Authentication Failure!".format(TARGETS[i]["ip"]))
    finally:
        connection.close()