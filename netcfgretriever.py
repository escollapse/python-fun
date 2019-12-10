@@ -0,0 +1,62 @@
#!/usr/bin/env python3
#
# netcfgretriever.py
# ver 0.4 - 20191209
#    -added note for cisco ASAs
#    -added date to save file
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
from datetime import date

TARGETSFILE = "/absolute/path/to/CSV/file.txt"
TARGETS = []
#                                                  V--- NOTE: trailing '/'
DESTDIR = "/absolute/path/to/cfg-file/save/location/"

# never hardcode cred's...
with open("/absolute/path/to/enablepw.txt", 'r') as f:
    ENABLEPW = f.read().rstrip('\n')
                            # for cisco ASAs, change "terminal length #" to "terminal pager #"
CMDSEQ = ["enable", "terminal length 0", "show running-config", "terminal length 24", "disable", "exit"]

with open(TARGETSFILE, 'r') as f:
    for line in f:
        ip, username, password, hostname = line.split(',')
        target = {"ip": ip, "username": username, "password": password, "hostname": hostname.rstrip('\n')}
        TARGETS.append(target)

connection = client.SSHClient()
connection.set_missing_host_key_policy(client.AutoAddPolicy)

for i in range(len(TARGETS)):
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
                ofile = DESTDIR + TARGETS[i]["hostname"] + '-' + date.today().isoformat().replace('-', '') + ".txt"
                with open(ofile, 'a') as f:
                    f.write(channel.recv(99999).decode("ascii"))
    except ssh_exception.SSHException:
        print("Target {}: SSH Exception!".format(TARGETS[i]["ip"]))
    except ssh_exception.AuthenticationException:
        print("Target {}: Authentication Failure!".format(TARGETS[i]["ip"]))
    finally:
        connection.close()
