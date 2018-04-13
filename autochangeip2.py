#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import socket
import shlex
import ctypes
import sys
import platform


def is_admin():
    """Check if user has admin rights in Windows"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if len(sys.argv) > 1:
    clientIP = sys.argv[1]
else:
    print("Pogresan IP broj. Mora biti izmedu 2-254")
    sys.exit()


if is_admin():
    try:
        # run ipconfig command in Windows and return
        ipconfigCommand = "ipconfig"
        ipconfigPro = subprocess.Popen(ipconfigCommand, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        ipconfigOut, ipconfigErr = ipconfigPro.communicate()

        # don't print output if there is no error
        if ipconfigErr != "" and ipconfigPro.returncode != 0:
            print(ipconfigOut, ipconfigErr, ipconfigPro.returncode)

        with open('autochangeip2.log', 'wb') as fh:
            fh.write(ipconfigOut)
            print("Upisano u file autochangeip2.log")

        # print that string of bytes as text on screen
        #ipconfigOutText = ipconfigOut.decode('utf-8')
        #print(ipconfigOutText)

        # find out your IP address, network, gateway and a interfacename
        interfaceName = ""
        defaultGateway = ""
        myIP = socket.gethostbyname(socket.gethostname())
        # myNetwork, if network is 192.168.100.0, than myNetwork is 100
        myNetwork = myIP.split(".")[2]
        with open('autochangeip2.log', 'r') as f:
            for line in f:
                if line.startswith("Ethernet adapter"):
                    line = line.split(" ")
                    # for XP or Win10 version
                    if len(line) > 3:
                        interfaceName = line[2] + " " + line[3] + " " + line[4]
                        interfaceName = interfaceName[:-2]  # remove space and : at the end
                    else:
                        interfaceName = line[2]
                        interfaceName = interfaceName[:-2]  # remove space and : at the end
                elif line.startswith(" ") and "Default Gateway" in line and "192" in line:
                    line = line.split(" ")
                    # find gateway IP
                    for index, item in enumerate(line):
                        defaultGateway = item[:-1]
                else:
                    pass


        print("IP: {}".format(myIP))
        print("Network: {}".format(myNetwork))
        print("Default gateway: {}".format(defaultGateway))
        print("Interface name: {}".format(interfaceName))

        changeIP = 'netsh interface ip set address' + ' ' + 'name="' + interfaceName + '" ' + \
                    'static 192.168.' + myNetwork + '.' + clientIP + ' ' + '255.255.255.0 ' + defaultGateway + ' 1'
        changeDNS = 'netsh interface ipv4 add dnsserver "' + interfaceName + '" address=' + defaultGateway + ' index=1'

        if platform.release() == 'XP':
            # set address name="Local Area Connection" source=static addr=[IP Address] mask=255.255.255.0
            # set address name="Local Area Connection" gateway=[GW IP Address] gwmetric=0
            changeDNS = 'netsh interface ip set dns "' + interfaceName + '" static ' + defaultGateway

        # shlex prepare command for Popen like it is written in Windows cmd
        changeIPshlex = shlex.split(changeIP)
        changeDNSshlex = shlex.split(changeDNS)

        subprocessIP = subprocess.Popen(changeIPshlex, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        subprocessDNS = subprocess.Popen(changeDNSshlex, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # subprocess.comunicate() returns a tuple of stdout and stderr
        outIP, errIP = subprocessIP.communicate()
        outDNS, errDNS = subprocessDNS.communicate()

        # returncode is 0 if everything is ok
        print(outIP, errIP, subprocessIP.returncode)
        print(outDNS, errDNS, subprocessDNS.returncode)


    except Exception as e:
        print("Error message: {}".format(e))
    finally:
        # run this before exception is returned
        # only waiting for input after UAC opens second cmd Window so it doesn't close for debugging
        input("Enter for end please ...")

else:
    input("Not admin")
    # Re-run the program with admin rights
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, sys.argv[0], None, 1)
