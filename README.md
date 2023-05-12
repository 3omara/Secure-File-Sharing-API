# Secure-File-Sharing-Vault

## Description

This desktop application allows users to share files in an end-to-end encrypted manner using hybrid cryptography. Before being uploaded to the server, files are sliced into several parts which are encrypted using three different symmetric cyphers on a round-robin basis; the symmetric ciphers used are DES, AES, and Blowfish. Afterward, the encrypted parts are added together into a single encrypted file. For every file, there are three randomly generated keys corresponding to each of the symmetric ciphers used. These keys are then merged into one file and encrypted using another key called a master key. Both the encrypted file and its encrypted keys file are uploaded to the FTP server while the master key is stored locally on the uploader's device. Every user is granted a pair of public and private keys on registration; these are used for the public key cryptosystem, specifically RSA, used for key exchange. When a user needs to access a certain file, they should send a request to the owner who may grant or deny access. If access is granted, the owner encrypts the master key using the public key of the receiver before sending it to them. Only the intended receiver can then decrypt the master key using their private key. The receiver can now successfully decrypt the keys file and use the recovered keys to decrypt the resource file.

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

Upon app launch, this registration panel appears:

![image](https://user-images.githubusercontent.com/61950995/218223584-1d249550-6ffd-489d-bb6f-b09fed5b710c.png)

You can register a new account or log in to an already existing account:

![image](https://user-images.githubusercontent.com/61950995/218223836-f7dc66f3-d5c8-4765-bb10-f9da150c84b4.png)

After logging in, the following screen appears:

![image](https://user-images.githubusercontent.com/61950995/218223904-69a58ab3-3820-4d72-a180-415830b6d465.png)

To upload a file simply right click in the files view and click upload then choose the file you need to upload:

![image](https://user-images.githubusercontent.com/61950995/218224036-157401ec-256b-4953-a45c-d827256a0922.png)

![image](https://user-images.githubusercontent.com/61950995/218224052-29c287a9-c7e9-4ba5-94ae-8d08f1935d01.png)

In this example, this is how the original file looks like:

![image](https://user-images.githubusercontent.com/61950995/218224124-267b752f-c7a6-4c5f-beaa-af48e98de8e2.png)

After successful upload, the FTP server now has the encrypted file and its encrypted keys file as follows:

![image](https://user-images.githubusercontent.com/61950995/218224236-c9e031a7-e24e-423e-89d1-ef2ae5d44796.png)

This is how the file, in this example, looks like after encryption:

![image](https://user-images.githubusercontent.com/61950995/218224269-9180924b-680f-4787-b30f-dec8567ed2e7.png)

Now, any user can find the uploaded file in the files view:

![image](https://user-images.githubusercontent.com/61950995/218224321-0fef5e21-c8d9-4ba4-aeb3-2eeb6c4a4893.png)

To request access to a certain file, Right click the file in the files view and then click request access:

![image](https://user-images.githubusercontent.com/61950995/218224407-a0f7f055-c059-4994-bc69-0e6661477037.png)

All incoming and outgoing requests can be seen on the left side of the screen. In the following image, we can see how both the sender and the reciever can see the request:

![image](https://user-images.githubusercontent.com/61950995/218224600-e5d8db20-775e-4468-a982-3af0d194d9f2.png)

A user can cancel any pending outgoing requests they sent as follows. A bell icon beside a file indicates an access request is pending for that file:

![image](https://user-images.githubusercontent.com/61950995/218224688-2f5effd7-269a-4c05-8e4a-620aa8e9df36.png)

The owner of the requested files can accept or decline incoming requests to those files as follows:

![image](https://user-images.githubusercontent.com/61950995/218224740-e913da19-e1be-4179-be94-dded48756cee.png)

Accepted requests are indicated with the green color. A check mark beside a requested file indicates that this account can now access the file:

![image](https://user-images.githubusercontent.com/61950995/218224778-b280bb0e-cdab-44c2-946f-b42988a4b566.png)

While declined requests are indicated with the red color. A cross mark beside a requested file indicates that this account has been denied access to that particular file:

![image](https://user-images.githubusercontent.com/61950995/218224823-75885be5-1e91-4059-bef5-6b17fe647599.png)

If you wish to download a file that you have access to, simply right click the file then click download and choose where to save the file:

![image](https://user-images.githubusercontent.com/61950995/218224952-7eaf5aff-64d9-4047-a7b8-d98290e82a94.png)

![image](https://user-images.githubusercontent.com/61950995/218225013-b4cae7df-6ba4-49d0-ad33-a35ad93bbcf0.png)

After downloading the fie we have been granted access to, we can see that it is no longer encrypted and that it has been decrypted successfully:

![image](https://user-images.githubusercontent.com/61950995/218225306-64e1f4ce-ba1b-4437-8403-aa1594ac5cef.png)
