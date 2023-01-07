import tkinter as tk
from tkinter import ttk

from views.View import View
from views.RequestsView import RequestsView
from views.ExplorerView import ExplorerView


class MainView(View):
    def setup_view(self):
        frame = ttk.Frame(self.parent)
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
