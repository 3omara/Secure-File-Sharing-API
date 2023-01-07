import tkinter as tk
from tkinter import ttk

from views.View import View


class RequestsView(View):
    def setup_view(self):
        columns = ('From', 'File')
        list = ttk.Treeview(self.parent,
                            columns=columns,
                            show='headings')
        for column in columns:
            list.heading(column, text=column)
            list.column(column, stretch=True, minwidth=0, width=100)
        list.insert('', tk.END, values=("User 1", "File 1"))
        list.insert('', tk.END, values=("User 2", "File 2"))
        list.insert('', tk.END, values=("User 3", "File 3"))
        list.pack(expand=True, fill=tk.BOTH)
