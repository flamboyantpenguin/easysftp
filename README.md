# easysftp

An easy to use program for downloading files from a remote server via sftp

## Introduction

easysftp is a console based program made using [pysftp](https://bitbucket.org/dundeemt/pysftp/src/master/) in Python. The program basically makes downloading files from a server via sftp easy by making use of simple navigation. 

## Getting Started

Download the latest release here or clone this repository by typing the command below in CMD

`git clone https://github.com/flamboyantpenguin/easysftp`

Note: To clone this repository, you need to have [git for windows](https://git-scm.com/) installed in your system. 

To run the program without a Python Interpreter, download the binary version. 

## Basic Commands

After connecting to the server, you will see a list of directories in the remote server and a console output in the window. 

`easysftp>`

To get a list of basic commands type help

To navigate/download type the number of the file/directory. 

For example:

```
Current Directory: /home/user/Data

[1] Backup
[2] Data

easysftp>
```

Type one and hit enter to move to Directory `Backup`

```
Current Directory: /home/user/Backup

[1] Documents
[2] Pictures
[3] Hello.txt

easysftp>
```

To download files, type the coressponding number of the required file

```
easysftp>3
Starting Download...
Downloading hello.txt [/]
```

To change to parent directory, type .. and hit enter

```
easysftp>..
Current Directory: /home/user/Data

[1] Backup
[2] Data

easysftp>
```

To change to a specfic directory, use cd command

```
easysftp>cd /media/user/data
Current Directory: /media/user/data

[1] Movies

easysftp>
```

For more info refer [manuals](./docs/manual.md)


## Login

Upon successfull login to a server, you will be asked whether to save login info locally. Login info is stored as `config.bin` in the local directory using `pickle`. Currently, the program supports only key based authentication. 


## About

    easysftp 1.0.0

    Last Updated: 29-07-2023

    Made by DAWN/ペンギン