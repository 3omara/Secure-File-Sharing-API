import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
from tkinter import messagebox

from views.View import View
from views.RequestsView import RequestsView
from views.ExplorerView import ExplorerView


class MainView(View):
    def setup_view(self):
        self.width = 1000
        self.height = 600
        self.window = ThemedTk(theme="arc")
        self.window.title("Vault")
        self.window.geometry(f"{self.width}x{self.height}")
        self.window.resizable(False, False)
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        frame = ttk.Frame(self.window)
        frame.pack(fill=tk.BOTH, expand=True)
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=3)
        frame.rowconfigure(0, weight=1)
        requests_frame = ttk.Frame(frame)
        requests_frame.grid(row=0, column=0, sticky="nsew")
        explorer_frame = ttk.Frame(frame)
        explorer_frame.grid(row=0, column=1, sticky="nsew")
        RequestsView(requests_frame).build(self.app)
        ExplorerView(explorer_frame).build(self.app)
        self.window.mainloop()

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.window.destroy()
            self.app.on_closing()
