# easysftp

An easy to use program for downloading files from a remote server via SFTP

## Introduction

easysftp is a console based program made using [paramiko](https://github.com/paramiko/paramiko) in Python. The program basically makes downloading files from a server via sftp easy by making use of simple navigation.

## Installation Instructions

### Windows

easysftp is available as a portable executable for Windows. To get started, download the latest version of easysftp from here or use the check-update command in easysftp to download the latest version.

For previous editions of Windows (7/8.1), you can download and run the legacy executable.

### Linux

easysftp can be compiled as an executable using pyinstaller. However, there will be combatability issues due to difference in package versions. To avoid this we introduced a script which will clone this repository and compile automatically.
To start using easysftp in Linux, you need to download the easysftp-linux-installer. The installer automatically downloads the latest source code and required libraries and compiles the program using pyinstaller.

After downloading the installer, extract the contents and run the install.sh script as admin

`tar xvf easysftp-linux-installer.tar.gz`

`sudo ./install.sh`

After successfull installation, you will see an executable file named easysftp-_version_.

`./easysftp-2.6`

To learn more about the installer, refer installer manual included with the installer.

## Running from Source

To run easysftp from source, clone this repository using git or download the source from the [latest release](https://github.com/flamboyantpenguin/easysftp/releases/latest).

`git clone https://github.com/flamboyantpenguin/easysftp`

> [!NOTE]
> To clone this repository on Windows, you need to have [git for windows](https://git-scm.com/) installed in your system.

## Basic Commands

After connecting to the server, you will see a list of directories in the remote server and a console output in the window.

`easysftp>`

To get a list of basic commands type help

To navigate/download type the number of the file/directory.

For example:

```Console
Current Directory: /home/penguin/Data

[1]             Share
[2]             Backup

easysftp>
```

> [!NOTE]
> Hidden files are not displayed by default. To turn view them, type `showhidden` in console.

Type `2` and hit enter to move to Directory `Backup`

```Console
easysftp>2
Current Directory: /home/penguin/Data/Backup

[1]             Documents
[2]             Pictures
[3]             Hello.txt

easysftp>
```

> [!WARNING]
> Numbering system is based on the files displayed on console when you use `ls`. To access/download hidden files/directories type `showhidden` and `ls` before accessing them.

To download files, type the coressponding number of the required file. Files will be stored in a local folder named easysftp.

```Console
easysftp>3
Downloading [///////////////////////////////////////\] 0.01 KB / 0.01 KB 100% 0.01 KB/s     ▼
```

    Note: The upload/download speed may not be accurate. Do not rely it for speed testing. 

To change to parent directory, type .. and hit enter

```Console
File Downloaded successfully
easysftp>..
Current Directory: /home/penguin/Data

[1]             Share
[2]             Backup

easysftp>
```

To change to a specfic directory, use cd command

```Console
easysftp>cd /media/user/data
Current Directory: /media/user/data

[1]             Movies

easysftp>
```

To upload a file located in the `easysftp` directory, use put command

```Console
put 20220912_083256.jpg
Uploading [//////////////////////////////////////////-] 2.45 MB / 2.45 MB 100% 191.74 KB/s   ▲
File Uploaded successfully
Current Directory: /home/penguin/Data/Backup

[1]             Documents
[2]             Pictures
[3]             20220912_083256.jpg
[4]             Hello.txt

easysftp>
```

> [!IMPORTANT]
> While using put command make sure to type the full file name. 

For more info refer [manuals](./docs/manual.md)

## Authentication

easysftp now supports key based authentication. Previously, easysftp ignored unknown hosts. This is not a recommended practise and is a security vulnerability. Therefore, we have modified our authentication system. If the ssh-fingerprint of your remote server is present in your system (stored in `.ssh/known_hosts` in your home directory) the fingerprints will be automatically loaded from it. In case of a unrecognised host, you have the option to add the fingerprint key to the local easysftp storage (`.cfg`) without disturbing your system `known_hosts` file. This fingerprint will be used for furthur authentication. For public key based authentication, you can copy your `key` file to the `easysftp` directory. Upon successfull login to a server, login info will be saved automatically. Passwords are no longer stored locally and you need to manually enter the password upon each login. 

Fingerprints are stored in `.cfg`. `.cfg` is encrypted using bses and can be decrypted only by the `easysftp` client. As of now config is version specific and we can guarentee maximum compatibility of a previous config file with latest versions. It is recommended that you delete the previously created config files before using the latest version. `.cfg`. is hidden and stored in the `easysftp` directory. You can view them by enabling View Hidden Files option in file explorer. However, you also have the option to turn of saving fingerprints locally. This can be done using the command 

```Console
easysftp> set saveFingerprints 0
```


> [!NOTE]
> After turning off `saveFingerprints` you will have to verify previously connected hosts on each login if not authorized by the OS

## Privacy

With the introduction to application settings in version `2.6`, users now have more choice towards how easysftp works. We have decided to make fingerprint storage and logging file names optional to improve user privacy. __We do not collect software logs/reports.__ However we believe these options give the user a sense of privacy. 

- `saveFingerprints` > Enable/Disable saving fingerprints locally
- `logFileName` > Enable/Disable logging file names during download/upload

You can use the set command to modify these parameters. Refer [Changing Application Settings](https://github.com/flamboyantpenguin/easysftp/edit/release2.6_doc/README.md#Changing-Application-Settings) to learn more about the commnand. 

## Changing Application Settings 

easysftp 2.6.0 supports application settings. You can modify the following values. 

- `showHiddenFiles` > Enable/Disable showing hidden files on the remote system
- `saveFingerprints` > Enable/Disable saving fingerprints locally
- `clearLogonStartup` > Enable/Disable clearing logs on startup
- `logFileName` > Enable/Disable logging file names during download/upload

Use `set` command to change settings. For instance, 

```Console
easysftp> set logFileName 0
```

Disables logging flenames. 

## Errors and Debugging

In case of any error, you can check the `.log` and `errorInfo.txt` file in the `easysftp` directory. `errorInfo.txt` is an error report of the last reported error. The logging system is still in development but will be useful in some cases. Since `.log` is hidden, you can also use the `viewlogs` command to open the logs in your default text editor. Logs will be useful in reporting errors. To clear old logs use `clearlogs` command. 

## Supported Platforms and Requirements

To run the program from source you need to install Python 3.10 or above since [bses]() encryption uses match case (introduced in Python 3.10)
The program has been tested successfully in the following platforms

- Windows 10/11
- Linux
  - amd64
    - Ubuntu (22.04.1, 23.10)
  - armv8
    - Ubuntu

## About

```Txt
easysftp 2.6.0

Last Updated: 14-01-2024
Made by DAWN/ペンギン
```

![DAWN](https://github.com/flamboyantpenguin/easysftp/assets/49310641/a2a6cd50-1ccf-4a8e-9b9c-fe7b36207ebc)
