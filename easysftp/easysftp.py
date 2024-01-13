# easysftp console 2.6.0
# An easy to use console based client for transferring files via sftp
# Program made with paramiko
# Made by DAWN/ペンギン
# Last Updated: 14-01-2024


import sys
import cui
import requests
import connector
from json import dumps
from getpass import getpass
from threading import Thread
from time import sleep, strftime
from os import mkdir, path, system, listdir, remove, stat

#os.startfile is not available for linux
if sys.platform == 'win32': from os import startfile


ldir = []
version = '2.6.0'
wDir = connector.wDir
sysfiles = ['.cfg', '.log', 'easysftp-2.6.exe', 'easysftp-2.6']


def initialise():

    if connector.settings['clearLogonStartup']:
        clearlogs()

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
    if path.exists(wDir) == False: mkdir(wDir)

    # Checking config
    print('Checking for config files', end='', flush = True)
    clear()
    if not path.exists(wDir+'/.cfg'):
        connector.saveConfig()
    connector.loadConfig()
    if connector.previousLogin != {} and input('Do you want to load data from previous login [{}@{}] (Y/N)? '.format(connector.previousLogin['user'], connector.previousLogin['host']))[0].upper() == 'Y':
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
            return 2.4
    
    keyfile = None
    if path.exists(wDir+'/key'):
        keyfile = wDir+'/key'
        
    key = getpass('Enter password: ')
    r = connector.connect(data['host'], data['user'], key, data['cPath'], keyfile)

    if r:
        return r
    
    del key
    print('Connection Established Successfully')
    logger('Connection Establised to {}'.format(data['host']), 0)
    return 0


def logger(message, code):
    if path.exists(wDir) == False: mkdir(wDir)
    currentTime = strftime('%Y%m%d/%H:%M:%S')
    
    with open(wDir+'/.log', 'a+') as logFile:
        log = '{cT}>\t{action} [{actionCode}]\n'.format(cT = currentTime, action = message, actionCode = code)
        logFile.write(log)
        logFile.flush()
    if sys.platform == 'win32': system(r"attrib +H {}\.log".format(wDir))
    return 0


def exportErrorInfo(data):
    with open(wDir+'/errorInfo.txt', 'w') as file:
        file.write(data)
    return 0


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
    fsize = cui.unitCalc(connector.sftp.lstat(file).st_size)
    print('Downloading {} ({:.2f} {})'.format(file, fsize[0], fsize[1]))
    fileDownload = Thread(target=connector.sftp.get, args=(file, wDir+'/'+file, tProgress))
    fileDownload.daemon = True
    fileDownload.start()
    cui.progressBar(fileDownload, file, 'D')
    fileDownload.join()
    print('\nFile Downloaded successfully')

    if connector.settings['logFileName']:
        logger("Downloaded {} from {} successfully".format(file, connector.previousLogin['host']), 0)
    else: 
        logger('File Downloaded successfully', 0)
    return 0


def put(file):
    fsize = cui.unitCalc(stat(file).st_size)
    print('Uploading {} ({:.2f} {})'.format(file, fsize[0], fsize[1]))
    fileUpload = Thread(target=connector.sftp.put, args=(wDir+'/'+file, file, tProgress))
    fileUpload.daemon = True
    fileUpload.start()
    cui.progressBar(fileUpload, file, 'U')
    fileUpload.join()
    print('\nFile Uploaded successfully')
    logger('File Uploaded Successfuly', 0)
    return 0


def ls():
    global ldir
    ldir.clear()
    print('Current Directory: {}\n'.format(connector.sftp.getcwd()))
    ldir = connector.sftp.listdir()
    if not connector.settings['showHiddenFiles']:
         for i in list(ldir):
            if i[0] == ".": ldir.remove(i)
    for i in ldir: print('[{}]\t\t{}'.format(ldir.index(i)+1, i))
    print()


def lls():
    print('\n')
    ld = listdir(wDir)
    for i in sysfiles: 
        if i in ld: ld.remove(i)
    for i in ld: print('[{}]\t\t{}'.format(ld.index(i)+1, i))
    print()
    return 0


def start(file):
    if sys.platform == 'win32': startfile(file)
    else: system('open {}'.format(file))
    return 0


def clearlogs():
    remove(wDir+'/.log')
    logger("Logs Cleared Successfully", 0)
    return 0

    
def clear():
    sleep(0.5)
    print('\b'*100, end = '', flush=True)
    return 0


def clearConsole():
    if sys.platform == 'linux': system('clear')
    else: system('cls')


def displayAbout():
    cui.setColor(cui.green)
    with open(assetPath+'/about.txt', 'r', encoding = 'UTF-8') as about:
        print(about.read())
    cui.setColor(cui.reset)


def displayManual(p = None):
    file = '/manual.txt'
    if p == 'settings': file = '/settingsHelp.txt'
    with open(assetPath+file, 'r') as manual:
        print(manual.read())
    return 0


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
        if (str(newVersion) <= version):
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
                if sys.platform == 'win32': start('easysftp-{}.exe'.format(newVersion[:3]))
                else: 
                    system('tar xzf easysftp-linux-installer.tar.gz')
                    system('sudo ./install.sh')
                sys.exit()
            return 1

    except Exception as e:
        logger('Update Check Failed', 1)
        print(cui.red, 'Error Checking for Updates\n', cui.reset, sep = '')
        return 2


# Startup
if sys.platform != 'linux': system('echo on')
checkUpdate()
print(cui.cyan, 'easyftp {}'.format(version), sep='')
print('https://github.com/flamboyantpenguin/easysftp')
print('An easy to use program for downloading files from a remote server via sftp', cui.reset, sep='')
errorCode = initialise()
if (errorCode):
    logger(connector.errorCode[errorCode], errorCode)
    print(cui.red, "{}".format(connector.errorCode[errorCode]), cui.reset, sep = '')
    sleep(1)
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
                if path.exists(wDir+'/'+ch.split()[1]):
                    put(ch.split()[1])
                    ls()
                else:
                    logger(connector.errorCode[3], 3)
                    print(cui.red, "{}".format(connector.errorCode[3]), cui.reset, sep = '')
            elif 'set' == ch.split()[0]:
                if len(ch.split()) < 3 or ch.split()[1] == 'help':
                    displayManual('settings')
                    continue
                connector.changeSettings(ch.split()[1], int(ch.split()[2]))
                print(cui.green, "Done!", cui.reset, sep = '')
            
            elif ch == 'lls': lls() 
            elif ch == 'ls': ls() 
            elif ch == 'cls' or ch == 'clear': clearConsole()
            elif ch == 'version': print(cui.green, '\neasysftp {}\n'.format(version), cui.reset, sep = '')
            elif ch == 'clearlogs': clearlogs(); print(cui.green, "Done!", cui.reset, sep = '')
            elif ch == 'viewlogs': start(wDir+r'\.log'); print("Opening Logs...")
            elif ch == 'showhidden': connector.changeSettings('showHiddenFiles', True); print(cui.green, "Done!", cui.reset, sep = '')
            elif ch == 'hidehidden': connector.changeSettings('showHiddenFiles', False); print(cui.green, "Done!", cui.reset, sep = '')
            elif ch == 'clearHosts': connector.hosts.clear(); connector.saveConfig(); print(cui.green, "Host Keys Cleared Successfully", cui.reset, sep = '')
            elif ch == 'settings': print("Settings////////////>", dumps(connector.settings, indent = 6), sep = '\n')
            elif ch == 'checkupdate':

                r = checkUpdate()
                if r is False:
                    print(cui.green, 'The software is up to date. For downloading other versions, go to https://github.com/flamboyantpenguin/easysftp/releases', cui.reset, sep = ' ')
                else:
                    print(cui.red, 'Update check failed! Check your internet connection and try again', cui.reset, sep = ' ')


            elif ch == 'about': clearConsole(); displayAbout()

            elif ch in ['', ' ']: continue
            else: print(cui.red, '\aInvalid Command', cui.reset, sep = ' ')

    except Exception as error:
        cui.setColor(cui.red)
        print('\aUnexpected Error')
        print(error)
        cui.setColor(cui.reset)
        print('\nReport Errors at https://github.com/flamboyantpenguin/easysftp')
