#easysftp console 1.8.0
#An easy to use console based client for Downloading files from a remote server using sftp
#Program made with paramiko
#Made by DAWN/ペンギン


import sys
import themes
import requests
import connectionmanager as cm
from time import sleep
from getpass import getpass
from threading import Thread
from pickle import load, dump

from os import mkdir, chdir, path, system, startfile


ldir = []
lAIcons = ['|', '/', '-', '\\'] #Loading Animation Characters
version = '1.8.0'


def initialise():
    #For fetching assets
    global assetPath, downloadDir
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        #Fetching from pyinstaller bundles
        assetPath = path.dirname(__file__)+'\\docs'
    else:
        #Fetching from local directory
        #assetPath = getcwd()+'\\assets'
        assetPath = '../docs'
    #Creating Local Directories
    if path.exists('Downloads') == False: mkdir('Downloads')
    downloadDir = 'Downloads'
    #Checking for config
    print('Checking for config files', end='', flush = True)
    clear()
    if path.exists('config.bin') and input('Do you want to load data from config (Y/N)? ').upper() == 'Y':
        data = cm.loadConfig()
    else: 
        print()
        host = input('Enter hostname: ')
        user = input('Enter username: ')
        key = getpass('Enter password: ')
        cPath = input('Enter remote path: ')
        data = {'host': host, 'user': user, 'key': key, 'cPath': cPath}
        if input('Do you want to store login info for furthur login? (Y/N) ').upper()[0] == 'Y':
            cm.saveConfig(data)
    #cm.connect(host, user, key, cPath)
    print('Connection Established Successfully')
    chdir('Downloads')
    return 0


def get(file):
    k = 0
    if file.isdigit(): file = ldir[int(file)-1]
    print('Starting Download...')
    fileDownload = Thread(target=cm.sftp.get, args=(file, downloadDir+'/'+file))
    fileDownload.daemon = True
    fileDownload.start()
    while fileDownload.is_alive():
        print('Downloading {} [{}]'.format(file, lAIcons[k]), flush=True, end='')
        k = k+1 if k < len(lAIcons)-1 else 0
        clear()
    clear()
    print('\nFile Downloaded successfully')


def put(file):
    k = 0
    if file.isdigit(): file = ldir[int(file)-1]
    print('Starting Upload...')
    fileDownload = Thread(target=cm.sftp.put, args=(file, file))
    fileDownload.daemon = True
    fileDownload.start()
    while fileDownload.is_alive():
        print('Uploading {} [{}]'.format(file, lAIcons[k]), flush=True, end='')
        k = k+1 if k < len(lAIcons)-1 else 0
        clear()
    clear()
    print('\nFile Uploaded successfully')


def ls():
    global ldir
    print('Current Directory: {}\n'.format(cm.sftp.getcwd()))
    ldir = cm.sftp.listdir()
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
    themes.setColor(themes.green)
    with open(assetPath+'/about.txt', 'r') as about:
        print(about.read())
    themes.setColor(themes.reset)


def displayManual():
    with open(assetPath+'/manual.txt', 'r') as manual:
        print(manual.read())


def downloadUpdate(newVersion):
    fileResponse = requests.get(url = 'https://github.com/flamboyantpenguin/easysftp/releases/latest/download/easysftp-{}.exe'.format(newVersion[:3]), allow_redirects=True)
    with open('easysftp-{}.exe'.format(newVersion[:3]), 'wb') as file:
        file.write(fileResponse.content)
    print('\nUpdate Downloaded Successfully!')


def checkUpdate():
    try: 
        response = requests.get('https://api.github.com/repos/flamboyantpenguin/easysftp/releases/latest')
        newVersion = response.json()['name'].split()[1]
        if newVersion == version:
            return 0
        else:
            print(themes.cyan, 'easysftp {} is available'.format(newVersion), sep='')
            if input('Do you want to download the latest version? (Y/N) ').upper()[0] == 'Y':
                k = 0
                updateDownload = Thread(target=downloadUpdate, args=(newVersion, ))
                updateDownload.daemon = True
                updateDownload.start()
                while updateDownload.is_alive():
                    print('Downloading easysftp-{} [{}]'.format(newVersion, lAIcons[k]), flush=True, end='')
                    k = k+1 if k < len(lAIcons)-1 else 0
                    clear()
                print('Lauching new version...')
                print(newVersion[:3])
                startfile('easysftp-{}.exe'.format(newVersion[:3]))
                sys.exit()
            return 1
    except Exception as e:
        print(e)
        print(themes.red, 'Error Checking for Updates\n', themes.reset, sep = '')


#Startup
if sys.platform != 'linux': system('echo on')
checkUpdate()
print(themes.cyan, 'easyftp 1.8.0', sep='')
print('An easy to use program for downloading files from a remote server via sftp', themes.reset, sep='')
initialise()


#Interaction Phase
ls()
while 1:
    ch = input('easysftp>')
    try: 
        if ch.isdigit():
            ch = int(ch)
            if cm.isDir(ldir[ch-1]): cm.sftp.chdir(ldir[ch-1]); ls(); continue
            else: get(str(ch)); continue
        elif ch == '.' or ch == '..':
            cm.sftp.chdir(ch)
            ls()
        else: 
            if ch == 'help': displayManual()
            elif ch == 'exit': sys.exit(0)
            elif 'cd' in ch: cm.sftp.chdir(ch.split()[1]); ls()
            elif 'get' in ch: get(ch.split()[1]); ls()
            elif 'put' in ch: put(ch.split()[1]); ls()
            elif 'ls' in ch: ls()
            elif ch == 'cls' or ch == 'clear': clearConsole()
            elif ch == 'version': print('\neasysftp 1.8.0 Pre-Alpha\n')
            elif ch == 'checkupdate': 
                if not checkUpdate():
                    print('The software is up to date. For downloading other versions, go to https://github.com/flamboyantpenguin/easysftp/releases')
            elif ch == 'about': system('cls'); displayAbout()
            elif ch in ['', ' ']: continue
            else: print('\aInvalid Command')
    except Exception as error:
        themes.setColor(themes.red)
        print('\aUnexpected Error')
        print(error)
        themes.setColor(themes.reset)
        print('\nReport Errors at https://github.com/flamboyantpenguin/easysftp')