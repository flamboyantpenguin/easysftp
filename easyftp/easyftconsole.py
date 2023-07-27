from os import system
from tkinter import messagebox
from threading import Thread


def connect(host, key):
    system('ssh {}'.format(host))


print('easyftp 0.9 Pre-Alpha')
print('A easy to use program for downloading files from a remote system via sftp')

host = input('Enter hostname: ')
if '@' not in host:
    user = input('Enter username: ')
    host = user+'@'+host
key = input('Enter username: ')
c = Thread(target=connect, args=(host,key))
c.start()