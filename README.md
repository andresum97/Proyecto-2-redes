# Proyect #2
## Chat application with XMMP protocol

### Requirements
- Python 3.7

## Installation
Clone the project
```bash
git clone https://github.com/andresum97/Proyecto-2-redes
```
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install all the packages
```bash
pip install sleekxmpp==1.3.3
pip install pyasn1==0.3.6 pyasn1-modules==0.1.5
pip install filetype
pip install PrettyTable
```

## Run the project
```bash
python menu.py
```

## Usage
When you start the program, it will show a menu with this options

### Register
Create a new account in the server with the name that you want

### Login
If you already have an account, you can login with your username and password


**If you Login, you are able to see the other options** 

### Message
You are able to send a message to any contact of your roster, or you can talk with people in a room or send png files.
#### Files
You are able to send image files, like **png** or **jpg**. When you choice this option, **the direction where the files must be is Desktop/Images**, and any
file in this carpet can be possible to send, you just have to write **filename.(jpg|png)** when the application ask for the filename, and that's it.  

### Roster
You can visualize any user in the server, even if they are not contacts with you, and see the status of your contacts

### Rooms
You can create or join rooms with people and messaging with different people

### Notifications
You will receive two types of notifications:
* A user subscribe to you
* A user mention you in a room

*Remember this functions are in different options in the application*

