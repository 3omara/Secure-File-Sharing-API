import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk


class App:
    def __init__(self):
        self.width = 1000
        self.height = 600
        self.__setup_window()

    def run(self):
        self.window.mainloop()

    def __setup_window(self):
        self.window = ThemedTk(theme="arc")
        self.window.title("Frontend")
        self.window.geometry(f"{self.width}x{self.height}")
        self.window.resizable(False, False)
        self.__add_main_layout()

    def __add_main_layout(self):
        frame = ttk.Frame(self.window, width=self.width, height=self.height)
        frame.rowconfigure(1)
        frame.columnconfigure(2)
        requests_frame = ttk.Frame(frame)
        requests_frame.grid(row=0, column=0, sticky="nsew")
        explorer_frame = ttk.Frame(frame)
        explorer_frame.grid(row=0, column=1, sticky="nsew")
        self.__add_requests(requests_frame)
        self.__add_explorer(explorer_frame)
        frame.pack(fill=tk.BOTH, expand=True)

    def __add_requests(self, frame: ttk.Frame):
        list = ttk.Treeview(frame,
                            columns=('From', 'File'),
                            show='headings')
        list.heading('From', text='From')
        list.heading('File', text='File')
        list.insert('', tk.END, values=("User 1", "File 1"))
        list.insert('', tk.END, values=("User 2", "File 2"))
        list.insert('', tk.END, values=("User 3", "File 3"))
        list.pack(expand=True, fill=tk.BOTH)

    def __add_explorer(self, frame: ttk.Frame):
        list = ttk.Treeview(frame,
                            columns=('Access', 'Name', 'Owner', 'Uploaded at'),
                            show='headings')
        list.column('Access', width=60)
        list.heading('Access', text='Access')
        list.heading('Name', text='Name')
        list.heading('Owner', text='Owner')
        list.heading('Uploaded at', text='Uploaded at')
        list.insert('', tk.END, values=('', "Item 1", "Owner 1", "2020-01-01"))
        list.insert('', tk.END, values=('', "Item 2", "Owner 2", "2020-01-01"))
        list.insert('', tk.END, values=('', "Item 3", "Owner 3", "2020-01-01"))
        list.pack(expand=True, fill=tk.BOTH)


if __name__ == '__main__':
    App().run()
