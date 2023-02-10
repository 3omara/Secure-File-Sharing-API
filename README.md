# Secure-File-Sharing-Vault

## Description

This desktop application allows users to share files in an end-to-end encrypted manner using hybrid cryptography. Before being uploaded to the server, files are sliced into several parts which are encrypted using three different symmetric cyphers on a round rubin basis; the symmetric cyphers used are DES, AES, and Blowfish. Afterwards the encrypted parts are added together into a single encrypted file. For every file, there are three randomly generated keys corresponding to each of the symmetric cyphers used. These keys are then merged into one file and encrypted using another key called a master key. Both the encrypted file and its encrypted keys file are uploaded to the FTP server while the master key is stored locally on the uploader's device. Every user is granted a pair of public and private keys on registration; these are used for the public key cryptosystem part, specifically RSA. When a user needs to access a certain file, they should send a request to the owner whom may grant or deny access. If access is granted, the owner encrypts the master key using the public key of the reciever before sending it to them. Only the intended reciever can then decrypt the master key using their private key. The reciever can now successfully decrypt the keys file and use the recovered keys to decrypt the resource file. 

This desktop application offers the following functionality: 

- Users can upload files securely and download files they have access to. 
- Users can browse through the encrypted files available on the server. 
- Users can send, recieve, and monitor file requests. 
- Users can deny or accept requests.


## Used Cryptographic Algorithms

- Rivest-Shamir-Adleman (RSA)
- Advanced Encryption Standard (AES)
- Data Encryption Standard (DES)
- Blowfish


## Tech Stack

- A Python binding to the Tk GUI toolkit called Tkinter was used for the user interface.
- Flask was used to build the backend server.
- PostgreSQL was used for the backend database.
- SQLite was used for the frontend database.


## Guide

First, you need to install all the dependencies by running `pip install -r requirements.txt` from a command prompt. Make sure you are in the project directory and using administrative privileges.

### Running the Flask Server:

1- Make sure you are in the backend directory by running `cd backend`.
2- Run `flask run` to get the server running.

### Running the FTP Server:

1- You need to install the python ftp server as follows: `python -m pip install python-ftp-server`.
2- From the project directory, run the FTP server as follows: `python -m python_ftp_server -u "admin" -p "admin" --ip 0.0.0.0 --port 6060 -d "ftp_storage"`.

### Running the GUI:

1- Make sure you are in the frontend directory by running `cd frontend`.
2- Run `python main.py` and the desktop application should start running successfully.


## Demo
