# easysftp console 2.0.0
# An easy to use console based client for transferring files via sftp
# Program made with paramiko
# Made by DAWN/ペンギン
# Last Updated: 10-09-2023


import sys
import cui
import requests
import connector
from time import sleep
from subprocess import run
from getpass import getpass
from threading import Thread
from os import mkdir, path, system

#os.startfile is not available for linux
if sys.platform == 'win32': from os import startfile


ldir = []
version = '2.0.0'


def initialise():
    # For fetching assets
    global assetPath, downloadDir
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        # Fetching from pyinstaller bundles
        assetPath = path.dirname(__file__)+'/docs'
    else:
        # Fetching from local directory
        # assetPath = getcwd()+'\\assets'
        assetPath = '../docs'
    # Creating Local Directories
    if path.exists('Downloads') == False: mkdir('Downloads')
    downloadDir = 'Downloads'
    # Checking for config
    print('Checking for config files', end='', flush = True)
    clear()
    if path.exists('config.bin') and input('Do you want to load data from config (Y/N)? ').upper() == 'Y':
        data = connector.loadConfig()
    else:
        print()
        host = input('Enter hostname: ')
        user = input('Enter username: ')
        key = getpass('Enter password: ')
        cPath = input('Enter remote path: ')
        data = {'host': host, 'user': user, 'key': key, 'cPath': cPath}
        if input('Do you want to store login info for furthur login? (Y/N) ').upper()[0] == 'Y':
            connector.saveConfig(data)
    connector.connect(data['host'], data['user'], data['key'], data['cPath'])
    print('Connection Established Successfully')
    return 0


def tProgress(transferred, toBeTransferred):
    cui.queue.put(int((transferred/toBeTransferred)*100))


def get(file):
    if file.isdigit(): file = ldir[int(file)-1]
    print('Starting Download...')
    fileDownload = Thread(target=connector.sftp.get, args=(file, downloadDir+'/'+file, tProgress))
    fileDownload.daemon = True
    fileDownload.start()
    cui.progressBar(fileDownload, "Downloading")
    fileDownload.join()
    print('\nFile Downloaded successfully')


def put(file):
    if file.isdigit(): file = ldir[int(file)-1]
    print('Starting Upload...')
    fileUpload = Thread(target=connector.sftp.put, args=(file, file, tProgress))
    fileUpload.daemon = True
    fileUpload.start()
    cui.progressBar(fileUpload, "Uploading")
    fileUpload.join()
    print('\nFile Uploaded successfully')


def ls():
    global ldir
    print('Current Directory: {}\n'.format(connector.sftp.getcwd()))
    ldir = connector.sftp.listdir()
    for i in ldir: print('[{}]\t\t{}'.format(ldir.index(i)+1, i))
    print()

    
def clear():
    sleep(0.5)
    print('\b'*100, end = '', flush=True)
    return 0


def clearConsole():
    if sys.platform == 'linux': system('clear')
    else: system('cls')


def displayAbout():
    cui.setColor(cui.green)
    with open(assetPath+'/about.txt', 'r') as about:
        print(about.read())
    cui.setColor(cui.reset)


def displayManual():
    with open(assetPath+'/manual.txt', 'r') as manual:
        print(manual.read())


def downloadUpdate(newVersion):
    if sys.platform != 'linux':
        url = 'https://github.com/flamboyantpenguin/easysftp/releases/latest/download/easysftp-{}.exe'.format(newVersion[:3])
        fileResponse = requests.get(url = url, allow_redirects=True)
        fileName = "easysftp-{}.exe".format(newVersion[:3])
    else:
        url = 'https://github.com/flamboyantpenguin/easysftp/releases/latest/download/easysftp-linux-installer.tar.gz'
        fileResponse = requests.get(url = url, allow_redirects=True)
        fileName = "easysftp-linux-installer.tar.gz"
    with open(fileName, 'wb') as file:
        file.write(fileResponse.content)
    print('\nUpdate Downloaded Successfully!')


def checkUpdate():
    try:
        response = requests.get('https://api.github.com/repos/flamboyantpenguin/easysftp/releases/latest')
        newVersion = response.json()['name'].split()[1]
        if newVersion >= version:
            return 0
        else:
            print(cui.cyan, 'easysftp {} is available'.format(newVersion), sep='')
            if input('Do you want to download the latest version? (Y/N) ').upper()[0] == 'Y':
                k = 0
                updateDownload = Thread(target=downloadUpdate, args=(newVersion, ))
                updateDownload.daemon = True
                updateDownload.start()
                while updateDownload.is_alive():
                    print('Downloading easysftp-{} [{}]'.format(newVersion, cui.lAIcons[k]), flush=True, end='')
                    k = k+1 if k < len(cui.lAIcons)-1 else 0
                    clear()
                if sys.platform == 'win32': startfile('easysftp-{}.exe'.format(newVersion[:3]))
                else: 
                    system('tar xzf easysftp-linux-installer.tar.gz')
                    system('sudo ./install.sh')
                sys.exit()
            return 1

    except Exception as e:
        print(e)
        print(cui.red, 'Error Checking for Updates\n', cui.reset, sep = '')


# Startup
if sys.platform != 'linux': system('echo on')
checkUpdate()
print(cui.cyan, 'easyftp 2.0.0', sep='')
print('An easy to use program for downloading files from a remote server via sftp', cui.reset, sep='')
initialise()


# Interaction Phase
ls()
while 1:
    ch = input('easysftp>')
    try:
        if ch.isdigit():
            ch = int(ch)
            if connector.isDir(ldir[ch-1]): connector.sftp.chdir(ldir[ch-1]); ls(); continue
            else: get(str(ch)); continue
        elif ch == '.' or ch == '..':
            connector.sftp.chdir(ch)
            ls()
        else:
            if ch == 'help': displayManual()
            elif ch == 'exit': sys.exit(0)
            elif 'cd' in ch: connector.sftp.chdir(ch.split()[1]); ls()
            elif 'get' in ch: get(ch.split()[1]); ls()
            elif 'put' in ch: put(ch.split()[1]); ls()
            elif 'ls' in ch: ls() 
            elif ch == 'cls' or ch == 'clear': clearConsole()
            elif ch == 'version': print('\neasysftp 2.0.0 Pre-Alpha\n')
            elif ch == 'checkupdate':
                if checkUpdate() is False:
                    print('The software is up to date. For downloading other versions, go to https://github.com/flamboyantpenguin/easysftp/releases')
            elif ch == 'about': system('cls'); displayAbout()
            elif ch in ['', ' ']: continue
            else: print('\aInvalid Command')
    except Exception as error:
        cui.setColor(cui.red)
        print('\aUnexpected Error')
        print(error)
        cui.setColor(cui.reset)
        print('\nReport Errors at https://github.com/flamboyantpenguin/easysftp')
