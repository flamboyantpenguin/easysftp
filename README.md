# easysftp

An easy to use program for downloading files from a remote server via sftp

## Introduction

easysftp is a console based program made using [paramiko](https://github.com/paramiko/paramiko) in Python. The program basically makes downloading files from a server via sftp easy by making use of simple navigation.

## Installation Instructions

### Windows

easysftp is available as a portable executable for Windows. The Download directory and config files are stored locally. To get started, download the latest version of easysftp from here or use the check-update command in easysftp-1.8 to download the latest version.

### Linux

To start using easysftp in Linux, you need to download the easysftp-linux-installer. The installer automatically downloads the latest source code and required libraries and compiles the program using pyinstaller.

After downloading the installer, extract the contents and run the install.sh script as admin

`sudo ./install.sh`

After successfull installation, you will see an executable file named easysftp-2.0.

`./easysftp-2.0`

To learn more about the installer, refer installer manual.

## Downloading Source

To download the source, clone this repository using git or download the source from the [latest release](https://github.com/flamboyantpenguin/easysftp/releases/latest).

`git clone https://github.com/flamboyantpenguin/easysftp`

Note: To clone this repository on Windows, you need to have [git for windows](https://git-scm.com/) installed in your system.

To download

## Basic Commands

After connecting to the server, you will see a list of directories in the remote server and a console output in the window.

`easysftp>`

To get a list of basic commands type help

To navigate/download type the number of the file/directory.

For example:

```Console
Current Directory: /home/user/Data

[1] Backup
[2] Data

easysftp>
```

Type one and hit enter to move to Directory `Backup`

```Console
Current Directory: /home/user/Backup

[1] Documents
[2] Pictures
[3] Hello.txt

easysftp>
```

To download files, type the coressponding number of the required file

```Console
easysftp>3
Starting Download...
Downloading hello.txt [/]
```

To change to parent directory, type .. and hit enter

```Console
easysftp>..
Current Directory: /home/user/Data

[1] Backup
[2] Data

easysftp>
```

To change to a specfic directory, use cd command

```Console
easysftp>cd /media/user/data
Current Directory: /media/user/data

[1] Movies

easysftp>
```

For more info refer [manuals](./docs/manual.md)

## Login

Upon successfull login to a server, you will be asked whether to save login info locally. Login info is stored as `config.bin` in the local directory using `pickle`. Currently, the program supports only key based authentication.

## Supported Platforms and Requirements

To run the program you need Python 3.10 or above especially since bses algorith uses match case for level based encryption.

## About

```Txt
easysftp 2.0.0

Last Updated: 10-09-2023
Made by DAWN/ペンギン
```
