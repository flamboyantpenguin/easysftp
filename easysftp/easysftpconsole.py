#easysftp 1.2.0
#An easy to use console based client for Downloading files from a remote server using sftp
#Program made using pysftp
#Made by DAWN/ペンギン


import sys
import themes
from time import sleep
from getpass import getpass
from threading import Thread
from pickle import load, dump
from paramiko import SSHClient, AutoAddPolicy
from os import mkdir, chdir, path, system, getcwd


ldir = []
lAIcons = ['|', '/', '-', '\\']
manual = 'Coming Soon...'



def initialise():
    global assetPath
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        assetPath = path.dirname(__file__)+'\\assets'
    else:
        assetPath = getcwd()+'\\assets'
    #Creating Local Directories
    if path.exists('Downloads') == False: mkdir('Downloads')
    #Checking for config
    print('Checking for config files', end='', flush = True)
    clear()
    if path.exists('config.bin') and input('Do you want to load data from config (Y/N)? ').upper() == 'Y':
        with open('config.bin', 'rb') as config: data = load(config)
        #Connecting to server
        connect(data['host'], data['user'], data['key'], data['cPath'])
        print('Connection Established Successfully')
        chdir('Downloads')
        return 0
    print()
    #Connecting to server
    host = input('Enter hostname: ')
    user = input('Enter username: ')
    key = getpass('Enter password: ')
    cPath = input('Enter remote path: ')
    if input('Do you want to store login info for furthur login? (Y/N) ').upper()[0] == 'Y':
        with open('config.bin', 'wb') as config: dump({'host': host, 'user': user, 'key': key, 'cPath': cPath}, config)
    connect(host, user, key, cPath)
    print('Connection Established Successfully')
    chdir('Downloads')
    return 0


def connect(host, user, key, cPath):
    global sftp
    connection = SSHClient()
    connection.set_missing_host_key_policy(AutoAddPolicy())
    try: 
        connection.connect(hostname=host, username=user, password=key)
    except:
        print('Cannot connect to server. Check your password and try again')
        sys.exit()
    sftp = connection.open_sftp()
    sftp.listdir()
    if cPath != '': sftp.chdir(cPath)
    

def ls():
    global ldir
    print('Current Directory: {}\n'.format(sftp.getcwd()))
    ldir = sftp.listdir()
    for i in ldir: print('[{}]\t\t{}'.format(ldir.index(i)+1, i))
    print()


def get(file):
    k = 0
    print('Starting Download...')
    fileDownload = Thread(target=sftp.get, args=(file, file))
    fileDownload.daemon = True
    fileDownload.start()
    while fileDownload.is_alive():
        print('Downloading {} [{}]'.format(file, lAIcons[k]), flush=True, end='')
        k = k+1 if k < 3 else 0
        clear()
    clear()
    print('\nFile Downloaded successfully')


def isDir(dir):
    try: 
        sftp.chdir(dir)
        sftp.chdir('..')
        return True
    except:
        return False



def clear():
    sleep(0.5)
    print('\b'*100, end = '', flush=True)
    return 0


def clearConsole():
    if sys.platform == 'linux': system('clear')
    else: system('cls')


def displayAbout():
    themes.setColor(themes.green)
    with open(assetPath+'\\about.txt', 'r') as about:
        print(about.read())
    themes.setColor(themes.reset)

def displayManual():
    with open(assetPath+'\\manual.txt', 'r') as manual:
        print(manual.read())


#Startup
if sys.platform != 'linux': system('echo on')
print(themes.blue, 'easyftp 1.2.0', sep='')
print('An easy to use program for downloading files from a remote server via sftp', themes.reset, sep='')
initialise()


#Interaction Phase
ls()
while 1:
    ch = input(themes.blue+'easysftp>'+themes.reset)
    try: 
        if ch.isdigit():
            ch = int(ch)
            if isDir(ldir[ch-1]): sftp.chdir(ldir[ch-1]); ls(); continue
            else: get(ldir[ch-1]); continue
        else: 
            if ch == 'help': displayManual()
            elif ch == 'exit': sys.exit(0)
            elif 'cd' in ch: sftp.chdir(ch.split()[1]); ls()
            elif 'ls' in ch: ls()
            elif ch == 'cls' or ch == 'clear': clearConsole()
            elif ch == 'version': print('\neasysftp 1.0.0 Stable\n')
            elif ch == 'about': system('cls'); displayAbout()
            elif ch in ['', ' ']: continue
            else: print('\aInvalid Command')
    except Exception as error:
        themes.setColor(themes.red)
        print('\aUnexpected Error')
        print(error)
        themes.setColor(themes.reset)
        print('\nReport Errors at https://github.com/flamboyantpenguin/easysftp')