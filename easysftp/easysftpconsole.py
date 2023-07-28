import sys
import pysftp

#sftp = ''

def connect(host, user, key, path):
    global sftp
    sftp = pysftp.Connection(host, username=user, password=key)
    print('Connection Established Successfully')
    sftp.chdir(path)

print('easyftp 0.9 Pre-Alpha')
print('A easy to use program for downloading files from a remote system via sftp')

host = input('Enter hostname: ')
user = input('Enter username: ')
key = input('Enter password: ')
path = input('Enter remote path: ')

connect(host, user, key, path)

while 1:
    ldir = sftp.listdir()
    for i in ldir: print('[{}]      {}'.format(ldir.index(i)+1, i))
    break
