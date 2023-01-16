from dotenv import load_dotenv
import tkinter as tk
from tkinter import ttk
from tkinter import *
import requests
from database.Database import Database
from ciphers.RSACipher import RSACipher
from views.LoginView import LoginView
import App


if __name__ == '__main__':
    load_dotenv()
    App.App().run()
