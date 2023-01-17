import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from typing import List

import shared.PathUtil as PathUtil
from shared.ObserverPattern import Observer
from models.FileReference import FileAccess, FileReference
from views.View import View


class ExplorerView(View, Observer):
    def setup_view(self):
        self.__id_to_file_reference = {}
        columns = ('Access', 'Name', 'Owner', 'Uploaded at')
        self.tree = ttk.Treeview(self.parent,
                                 columns=columns,
                                 show='headings')
        self.tree.pack(expand=True, fill=tk.BOTH)
        for column in columns:
            self.tree.heading(column, text=column)
            self.tree.column(column, stretch=True, minwidth=0, width=100)
        self.tree.column('Access', width=20, anchor=tk.CENTER)
        self.tree.bind("<Button-3>", self.on_right_click)

    def register_observers(self):
        self.app.file_references_service.register_observer(self)

    def unregister_observers(self):
        self.app.file_references_service.unregister_observer(self)

    @property
    def file_references(self):
        return self.__id_to_file_reference.values()

    @file_references.setter
    def file_references(self, file_references: List[FileReference]):
        self.__id_to_file_reference = {file_reference.id: file_reference
                                       for file_reference in file_references}
        self.tree.delete(*self.tree.get_children())
        for ref in file_references:
            self.tree.insert('', tk.END,
                             values=(
                                 self.access_icon(ref.access),
                                 ref.name,
                                 ref.owner_name,
                                 ref.uploaded_at),
                             tags=(ref.id, ref.access)
                             )

    def on_right_click(self, event):
        iid = self.tree.identify_row(event.y)
        if iid:
            self.tree.selection_set(iid)
            menu = tk.Menu(self.parent, tearoff=0)
            file_id = self.tree.item(iid)['tags'][0]
            file_reference = self.__id_to_file_reference[file_id]
            if file_reference.access == FileAccess.NOT_REQUESTED:
                menu.add_command(
                    label="Request access",
                    command=lambda: self.request_access(file_reference)
                )
            elif file_reference.access == FileAccess.REQUESTED:
                menu.add_command(
                    label="Requested",
                    command=None,
                    state=tk.DISABLED
                )
            elif file_reference.access == FileAccess.PERMITTED:
                menu.add_command(
                    label="Download",
                    command=lambda: self.download(file_reference)
                )
            elif file_reference.access == FileAccess.DENIED:
                menu.add_command(
                    label="Denied",
                    command=None,
                    state=tk.DISABLED
                )
            menu.add_separator()
            menu.add_command(
                label="Upload",
                command=self.upload
            )
            menu.tk_popup(event.x_root, event.y_root)
        else:
            menu = tk.Menu(self.parent, tearoff=0)
            menu.add_command(
                label="Upload",
                command=self.upload
            )
            menu.tk_popup(event.x_root, event.y_root)

    def download(self, file_reference: FileReference):
        filename = asksaveasfilename(
            defaultextension=PathUtil.extension(file_reference.name),
            initialfile=file_reference.name)
        if filename:
            self.app.ftp_service.download(file_reference, filename)

    def request_access(self, file_reference: FileReference):
        self.app.file_requests_service.request(file_reference)

    def upload(self):
        filename = askopenfilename()
        if filename:
            self.app.ftp_service.upload(filename)

    def access_icon(self, access: FileAccess):
        if access == FileAccess.NOT_REQUESTED:
            return ''
        elif access == FileAccess.REQUESTED:
            return '🔔'
        elif access == FileAccess.PERMITTED:
            return '✅'
        elif access == FileAccess.DENIED:
            return '❌'

    def update(self, subject):
        if isinstance(subject, self.app.file_references_service.__class__):
            self.file_references = subject.file_references
