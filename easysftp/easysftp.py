# easysftp console 2.5.0
# An easy to use console based client for transferring files via sftp
# Program made with paramiko
# Made by DAWN/ペンギン
# Last Updated: 06-01-2024


import sys
import cui
import requests
import connector
from time import sleep, strftime
from getpass import getpass
from threading import Thread
from os import mkdir, path, system, listdir

#os.startfile is not available for linux
if sys.platform == 'win32': from os import startfile


ldir = []
version = '2.5'


def initialise():

    logger('Starting Initialization', 0)
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
    if path.exists('easysftp') == False: mkdir('easysftp')
    downloadDir = 'easysftp'

    # Checking config
    print('Checking for config files', end='', flush = True)
    clear()
    if not path.exists('easysftp/config.bin'):
        connector.saveConfig()
    connector.loadConfig()
    msg = 'Do you want to load data from previous login [{}@{}] (Y/N)? '.format(connector.previousLogin['user'], connector.previousLogin['host'])
    if connector.previousLogin != {} and input(msg)[0].upper() == 'Y':
        data = connector.previousLogin
    else:
        print()
        host = input('Enter hostname: ')
        user = input('Enter username: ')
        cPath = input('Enter remote path: ')
        data = {'host': host, 'user': user, 'cPath': cPath}
        connector.previousLogin = data
        connector.saveConfig()

    if not connector.checkHost(data['host']):
        if input("Do you want to add this host to known_hosts? (Y/N)? ")[0].upper() == 'Y':
            connector.addHostKey(data['host'])
        else:
            logger(connector.errorCode[2.4], 2.4)
            print(cui.red, "{}".format(connector.errorCode[2.4]), cui.reset, sep = '')
            return 2.4
    
    keyfile = None
    if path.exists('easysftp/key.pub'):
        keyfile = 'easysftp/key.pub'
        
    key = getpass('Enter password: ')
    r = connector.connect(data['host'], data['user'], key, data['cPath'], keyfile)

    if r:
        return r
    
    del key
    print('Connection Established Successfully')
    logger('Connection Establised to {}'.format(data['host']), 0)
    return 0


def logger(message, code):
    currentTime = strftime('%Y-%m-%d/%H%M%S')
    with open('easysftp/logs.txt', 'a') as logFile:
        log = '{cTime}\t:\t{action} | {actionCode}\n'.format(cTime = currentTime, action = message, actionCode = code)
        logFile.write(log)
        logFile.flush()
    return 0

'''
def exportErrorInfo(data):
    with open('error_{}'.format(strftime('%Y%m%d%H%M%S')), 'w') as file:
        file.write(data)
    return 0
'''


def tProgress(transferred, toBeTransferred):
    cui.queue.put([transferred, toBeTransferred])


def get(file):
    if file.isdigit(): file = ldir[int(file)-1]
    '''
    print('Starting Download...')
    progress = Thread(target=cui.progressBar, args=("Downloading", ))
    progress.daemon = True
    progress.start()
    connector.sftp.get(file, downloadDir+'/'+file, tProgress)
    progress.join()
    print('\nFile Downloaded successfully')
    '''
    fileDownload = Thread(target=connector.sftp.get, args=(file, downloadDir+'/'+file, tProgress))
    fileDownload.daemon = True
    fileDownload.start()
    cui.progressBar(fileDownload, "Downloading")
    fileDownload.join()
    print('\nFile Downloaded successfully')
    logger('File Downloaded successfully', 0)


def put(file):
    fileUpload = Thread(target=connector.sftp.put, args=(downloadDir+'/'+file, file, tProgress))
    fileUpload.daemon = True
    fileUpload.start()
    cui.progressBar(fileUpload, "Uploading")
    fileUpload.join()
    print('\nFile Uploaded successfully')
    logger('File Uploaded Successfuly', 0)


def ls():
    global ldir
    print('Current Directory: {}\n'.format(connector.sftp.getcwd()))
    ldir = connector.sftp.listdir()
    for i in ldir: print('[{}]\t\t{}'.format(ldir.index(i)+1, i))
    print()


def lls():
    print('\n')
    ldir = listdir(downloadDir)
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
    logger('Downloading Updates', 0)
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
    logger('Checking for Updates', 0)
    try:
        response = requests.get('https://api.github.com/repos/flamboyantpenguin/easysftp/releases/latest')
        newVersion = response.json()['name'].split()[1]
        if newVersion >= version:
            return 0
        else:
            logger('New Update Found', 0)
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
        logger('Update Check Failed', 1)
        print(cui.red, 'Error Checking for Updates\n', cui.reset, sep = '')


# Startup
if sys.platform != 'linux': system('echo on')
checkUpdate()
print(cui.cyan, '\neasyftp 2.5.0', sep='')
print('https://github.com/flamboyantpenguin/easysftp')
print('An easy to use program for downloading files from a remote server via sftp', cui.reset, sep='')
errorCode = initialise()
if (errorCode):
    logger(connector.errorCode[errorCode], errorCode)
    print(cui.red, "{}".format(connector.errorCode[errorCode]), cui.reset, sep = '')
    sys.exit(int(errorCode))


# Interaction Phase
cui.eventCheck()
ls()
while 1:
    ch = input('easysftp>')
    try:
        if ch.isdigit():
            ch = int(ch)
            if connector.isDir(ldir[ch-1]): connector.sftp.chdir(ldir[ch-1]); ls(); continue
            else: 
                try: 
                    get(str(ch))
                except Exception as e:
                    print(e)
                continue
        elif ch == '.' or ch == '..':
            connector.sftp.chdir(ch)
            ls()
        else:
            if ch == 'help': displayManual()
            elif ch == 'exit': sys.exit(0)
            elif 'cd' in ch: connector.sftp.chdir(ch.split()[1]); ls()
            elif 'get' in ch: get(ch.split()[1]); ls()
            elif 'put' in ch: 
                if path.exists(downloadDir+'/'+ch.split()[1]):
                    put(ch.split()[1])
                    ls()
                else:
                    logger(connector.errorCode[3], 3)
                    print(cui.red, "{}".format(connector.errorCode[3]), cui.reset, sep = '')
            elif 'ls' in ch: ls() 
            elif 'lls' in ch: lls() 
            elif ch == 'cls' or ch == 'clear': clearConsole()
            elif ch == 'version': print('\neasysftp 2.5.0 Pre-Alpha\n')
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
