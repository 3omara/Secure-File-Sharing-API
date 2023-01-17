import tkinter as tk
from ttkthemes import ThemedTk
from tkinter import ttk
from tkinter import *
import requests

from database.Database import Database
from ciphers.RSACipher import RSACipher
from models.User import User
from views.View import View


class LoginView(View):

    def setup_view(self):
        self.width = 400
        self.height = 240
        self.root = ThemedTk(theme="arc")
        self.root.title("Vault")
        self.root.geometry(f"{self.width}x{self.height}")
        self.root.resizable(False, False)

        self.uname_var = tk.StringVar()
        self.pass_var = tk.StringVar()

        self.label = ttk.Label(self.root, text="Welcome!")
        self.label.pack(padx=20, pady=20)

        self.usernameframe = ttk.Frame(self.root)
        self.usernameframe.pack()

        self.passwordframe = ttk.Frame(self.root)
        self.passwordframe.pack()

        self.usernameLabel = ttk.Label(self.usernameframe, text="Username")
        self.usernameLabel.pack(padx=5, side='left')
        self.usernameEntry = ttk.Entry(
            self.usernameframe, textvariable=self.uname_var)
        self.usernameEntry.pack(pady=10, padx=5, side='left')

        self.passLabel = ttk.Label(self.passwordframe, text="Password")
        self.passLabel.pack(padx=5, side='left')
        self.passEntry = ttk.Entry(
            self.passwordframe, textvariable=self.pass_var, show="*")
        self.passEntry.pack(pady=10, padx=5, side='left')

        self.submitBtn = ttk.Button(
            self.root, command=self.submit, text="Register/ Login")
        self.submitBtn.pack(padx=50, pady=20)

        self.root.mainloop()

    def submit(self):
        name = self.uname_var.get()
        password = self.pass_var.get()

        public_key = "None"
        database = Database()
        if (database.get_private_key(name) == None):
            public_key, private_key = RSACipher().generate_keys()
            database.insert_private_key(name, private_key)

        data = {"user_name": name, "password": password,
                "public_key": public_key}
        try:
            res = requests.post("http://127.0.0.1:5000/login", data=data)
            self.app.user = User(
                res.json()['id'],
                self.uname_var.get(),
                database.get_private_key(name)
            )
            self.root.destroy()
        except:
            self.uname_var.set("")
            self.pass_var.set("")
