# easysftp 2.2.0
# An easy to use console based client for Downloading files from a remote server using sftp
# Program made with paramiko
# Made by DAWN/ペンギン
# Last Updated 28-12-2023


import bses03.ph03 as bses
from pickle import loads, dumps
from paramiko import SSHClient, AutoAddPolicy


def connect(host, user, key, cPath = ''):
    global sftp
    connection = SSHClient()
    connection.set_missing_host_key_policy(AutoAddPolicy())
    try: 
        connection.connect(hostname=host, username=user, password=key)
    except:
        return 1
    sftp = connection.open_sftp()
    sftp.listdir()
    if cPath != '': sftp.chdir(cPath)
    return 0
    

def isDir(dir):
    try: 
        sftp.chdir(dir)
        sftp.chdir('..')
        return True
    except:
        return False
    

def encode(data):
    n = 0
    l = []
    for i in range(8, len(data)+1, 8):
        l.append(data[n:i])
        n = i
    rData = []
    for i in l:
            n = k = 0
            for j in reversed(i):
                n+=int(j)*(2**k)
                k+=1
            rData.append(n)
    return bytes(rData)


def decode(data):
    rData = ''
    l = []
    for i in data:
        b = bin(i)[2:]
        if len(b)!= 8:
            b='0'*(8-len(b))+b
        l.append(b)
    for i in l: rData+=i
    return rData


def loadConfig():
    with open('easysftp/config.bin', 'rb') as config:
        data = config.read()
        data = decode(data)
    data = bses.switch(data, 'Tilda4744#@', 0)
    data = loads(encode(data))
    return data
    

def saveConfig(data):
    with open('easysftp/config.bin', 'wb') as config:
        data = dumps(data)
        data = decode(data)
        data = bses.switch(data, 'Tilda4744#@', 0)
        config.write(encode(data))
    return 0