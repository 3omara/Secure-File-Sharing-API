from dotenv import load_dotenv
import tkinter as tk
from tkinter import ttk
from tkinter import *
import requests
from database.Database import Database
from ciphers.RSACipher import RSACipher
import App



if __name__ == '__main__':
    load_dotenv()
    def submit():
        name = uname_var.get()
        password = pass_var.get()
        
        print("The name is : " + name)
        print("The password is : " + password)
        
        
        public_key = "None"
        database = Database()
        if(database.get_private_key(name)==None):
            public_key, private_key = RSACipher().generate_keys()
            database.insert_private_key(name, private_key)
        
        data = {"user_name":name, "password": password, "public_key": public_key}
        
        res = requests.post("http://127.0.0.1:5000/login", data=data)
        if res.status_code!=404:    
            print("status_code", res.status_code)
            root.destroy()
            App.App().run()
        else:
            print("status_code", res.status_code)
            uname_var.set("")
            pass_var.set("")


    root = Tk()

    uname_var=tk.StringVar()
    pass_var=tk.StringVar()

    label = tk.Label(root, text="Welcome!", font=('Arial', 18))
    label.pack(padx=20, pady=20)

    usernameframe = ttk.Frame(root)
    usernameframe.pack()

    passwordframe = ttk.Frame(root)
    passwordframe.pack()

    usernameLabel = tk.Label(usernameframe, text="Username", font=('Arial', 16))
    usernameLabel.pack(padx=5, side='left')
    usernameEntry =tk.Entry(usernameframe, textvariable = uname_var, font=('Arial', 16))
    usernameEntry.pack(pady=10, padx=5, side='left')

    passLabel = tk.Label(passwordframe, text="Password", font=('Arial', 16))
    passLabel.pack(padx=5, side='left')
    passEntry =tk.Entry(passwordframe, textvariable = pass_var, show="*", font=('Arial', 16))
    passEntry.pack(pady=10, padx=5, side='left')

    submitBtn = tk.Button(root, command = submit, text="Register/ Login", font=('Arial', 18))
    submitBtn.pack(padx=50, pady=20)

    root.mainloop()

