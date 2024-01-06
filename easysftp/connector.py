# easysftp 2.5.0
# An easy to use console based client for Downloading files from a remote server using sftp
# Program made with paramiko
# Made by DAWN/ペンギン
# Last Updated 06-01-2024


import paramiko
from os import system
import bses03.ph03 as bses
from base64 import decodebytes
from pickle import loads, dumps


hosts = []
previousLogin = {}
connection = paramiko.SSHClient()

errorCode = {1:'Err:1.1 Config File Corrupted!', 2.1:'Err:2.1 Authentication Error! Check your credentials', 2.2:'Err:2.2 Invalid Authentication Type! You might require a keyfile', 2.3:'Err:2.3 Invalid Host Key!', 2.4: 'Err:2.4 Unknown Host! Add host to known hosts in the program or system', 3: 'Err3: Specified File Does Not Exist', 4: 'Err4: An unknown error has occured. Check logs or error.txt'}


def exportErrorInfo(data):
    with open('error', 'w') as file:
        file.write(data)
    return 0


def connect(host, user, key, cPath = '', keyfile = None):
    global sftp
    global connection
    loadHosts()
    connection.load_system_host_keys() 

    try: 
        connection.connect(hostname=host, username=user, password=key, key_filename = keyfile)
    except Exception as e:
        exportErrorInfo(str(e))
        match (e):
            case paramiko.AuthenticationException:
                return 2.1
            case paramiko.BadAuthenticationType:
                return 2.2
            case paramiko.BadHostKeyException:
                return 2.3
            case _:
                return 4
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
    global hosts
    global previousLogin
    with open('easysftp/config.bin', 'rb') as config:
        data = config.read()
        data = decode(data)
    data = bses.switch(data, 'Tilda4744#@', 0)
    data = loads(encode(data))
    previousLogin = data[0]
    hosts = data[1]
    return 0
    

def saveConfig():
    with open('easysftp/config.bin', 'wb') as config:
        data = dumps({0: previousLogin, 1: hosts})
        data = decode(data)
        data = bses.switch(data, 'Tilda4744#@', 0)
        config.write(encode(data))
    return 0


def loadHosts():
    global hosts
    global connection
    t = connection.get_host_keys()
    for host in hosts:
        if host[1] == 'ssh-rsa':
            key = paramiko.RSAKey(data=decodebytes(host[2]))
        else:
            key = paramiko.Ed25519Key(data=decodebytes(host[2]))
        t.add(hostname = host[0], keytype= host[1], key = key)
    t.update()
    return 0


def getKey(host):
    keys = list()
    system('@echo off')
    system(r'ssh-keyscan {} > easysftp\key.pub'.format(host))
    with open('easysftp/key.pub', 'r') as keyfile:
        data = keyfile.read().split()
    for i in data:
        if i == 'ssh-rsa' or i == 'ssh-ed25519':
            keys.append([i, data[data.index(i)+1].encode()])
    system(r'del easysftp\key.pub')
    system('@echo on')
    return keys


def addHostKey(host):
    global hosts
    global connection
    keys = getKey(host)
    for key in keys:
        hosts.append([host, key[0], key[1]])
    saveConfig()
    return 0


def checkHost(host):
    global connection
    loadHosts()
    if not (connection.get_host_keys().lookup(host)):
        return 0
    return 1