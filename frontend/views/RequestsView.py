import tkinter as tk
from tkinter import ttk
from models.FileRequest import FileRequestStatus

from views.View import View


class RequestsView(View):
    def setup_view(self):
        columns = ('From', 'File')
        self.tree = ttk.Treeview(self.parent,
                                 columns=columns,
                                 show='headings')
        for column in columns:
            self.tree.heading(column, text=column)
            self.tree.column(column, stretch=True, minwidth=0, width=100)
        self.tree.tag_configure(FileRequestStatus.ACCEPTED, background='green')
        self.tree.tag_configure(FileRequestStatus.DECLINED, background='red')
        self.tree.pack(expand=True, fill=tk.BOTH)

    def register_observers(self):
        self.app.subjects.requests.register_observer(self)

    def unregister_observers(self):
        self.app.subjects.requests.unregister_observer(self)

    def update(self, subject):
        if isinstance(subject, self.app.subjects.requests.__class__):
            self.tree.delete(*self.tree.get_children())
            for file_request in self.app.subjects.requests.file_requests:
                self.tree.insert('', tk.END,
                                 values=(file_request.sender_name,
                                         file_request.file_name),
                                 tags=(file_request.status))
