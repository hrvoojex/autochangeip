#!/usr/bin/env python3
#! -*- coding:utf-8 -*-

import subprocess
import socket
import shlex
import ctypes
import sys
import platform


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if is_admin():
    # cmd shows network interface names (Local Area network, Ethernet, Wireless Network Connection)
    cmd_inter = ['netsh', 'interface', 'show', 'interface']
    # cmd_ip = ['netsh', 'interface', 'ip', 'show', 'config', 'name=Ethernet', '|', 'findstr', 'IP Address']

    # Use this for command if you take raw input from user or complex cases
    # cmd_ip_raw = 'netsh interface ip show config name="Ethernet" | findstr "IP Address"'
    # cmd_ip = shlex.split(cmd_ip_raw)

    ###########################################
    # Example for complex command in subprocess
    ###########################################
    # The right way when using in complex cases
    # https://docs.python.org/3/library/subprocess.html
    #
    # >>> import shlex, subprocess
    # >>> command_line = input()
    # /bin/vikings -input eggs.txt -output "spam spam.txt" -cmd "echo '$MONEY'"
    # >>> args = shlex.split(command_line)
    # >>> print(args)
    # ['/bin/vikings', '-input', 'eggs.txt', '-output', 'spam spam.txt', '-cmd', "echo '$MONEY'"]
    # >>> p = subprocess.Popen(args) # Success!

    p_inter = subprocess.Popen(cmd_inter, stdout=subprocess.PIPE)
    # shell=True only when using built-in commands in Windows cmd
    # p_ip = subprocess.Popen(cmd_ip, shell=True, stdout=subprocess.PIPE)

    # output of popen is bytes type, so we need to decode
    out_p_inter = p_inter.stdout.read().decode()
    # out_p_ip = p_ip.stdout.read()

    # print(out_p_inter.decode())
    # print(out_p_ip.decode())

    lines = out_p_inter.splitlines()
    my_line = lines[3]
    my_word = my_line.split(" ")

    # XP has network interface name in different location then Win10
    if platform.release() == 'XP':
        net_int = my_word[31] + ' ' + my_word[32] + ' ' + my_word[33]
    else:
        net_int = my_word[22]

    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)

    # find out third octet from IP address
    ip_list = ip.split('.')
    ip_network = ip_list[2]

    # print for debug
    # print('OS: {}'.format(platform.release()))
    # print('lines: {}'.format(lines))
    # print('my_line: {}'.format(my_line))
    # print('my_word: {}'.format(my_word))
    # print('net_int: {}'.format(net_int))
    # print('ip: {}'.format(ip))
    # print('ip_list: {}'.format(ip_list))
    # print('ip_network: {}'.format(ip_network))


    # cmd_change_ip = ['netEsh', 'interface', 'ip', 'set', 'address',
    #                 net_int, 'static', '192.168.0.3', '255.255.255.0', '192.168.0.251', '1']

    cmd_change_ip_raw = 'netsh interface ip set address' + ' ' + 'name="' + net_int + '" ' + \
                        'static 192.168.' + ip_network + '.2' + ' ' + '255.255.255.0 192.168.0.251 1'
    cmd_change_ip = shlex.split(cmd_change_ip_raw)

    sp = subprocess.Popen(cmd_change_ip, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = sp.communicate()
    print(out, err, sp.returncode)
    input("Enter for end")
else:
    # Re-run the program with admin rights
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, sys.argv[0], None, 1)





