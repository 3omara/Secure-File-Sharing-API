import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename

from shared.ObserverPattern import Observer
from views.View import View


class ExplorerView(View, Observer):
    def setup_view(self):
        columns = ('Access', 'Name', 'Owner', 'Uploaded at')
        self.tree = ttk.Treeview(self.parent,
                                 columns=columns,
                                 show='headings')
        self.tree.pack(expand=True, fill=tk.BOTH)
        for column in columns:
            self.tree.heading(column, text=column)
            self.tree.column(column, stretch=True, minwidth=0, width=100)
        self.tree.column('Access', width=20)
        self.tree.bind("<Button-3>", self.on_right_click)

        self.item_popup_menu = tk.Menu(self.parent, tearoff=0)
        self.item_popup_menu.add_command(
            label="Download",
            command=self.download
        )
        self.item_popup_menu.add_command(
            label="Request access",
            command=self.request_access
        )
        self.item_popup_menu.add_separator()
        self.item_popup_menu.add_command(
            label="Upload",
            command=self.upload
        )

        self.empty_popup_menu = tk.Menu(self.parent, tearoff=0)
        self.empty_popup_menu.add_command(
            label="Upload",
            command=self.upload
        )

    def register_observers(self):
        self.app.subjects.files.register_observer(self)

    def unregister_observers(self):
        self.app.subjects.files.unregister_observer(self)

    def on_right_click(self, event):
        iid = self.tree.identify_row(event.y)
        if iid:
            # mouse pointer over item
            self.tree.selection_set(iid)
            self.item_popup_menu.tk_popup(event.x_root, event.y_root)
        else:
            self.empty_popup_menu.tk_popup(event.x_root, event.y_root)

    def download(self):
        for selection in self.tree.selection():
            item = self.tree.item(selection)
            print(item['values'])

    def request_access(self):
        for selection in self.tree.selection():
            item = self.tree.item(selection)
            print(item['values'])

    def upload(self):
        filename = askopenfilename()
        if filename:
            self.app.ftp_service.upload(filename)

    def update(self, subject):
        if isinstance(subject, self.app.subjects.files.__class__):
            self.tree.delete(*self.tree.get_children())
            for ref in subject.file_references:
                self.tree.insert('', tk.END, values=(
                    '✅',
                    ref.name,
                    ref.owner_name,
                    ref.uploaded_at
                ))
