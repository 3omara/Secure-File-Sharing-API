import tkinter as tk
from tkinter import ttk
from typing import List

from models.FileRequest import FileRequest, FileRequestStatus
from views.View import View


class RequestsView(View):
    def setup_view(self):
        self.user_id = self.app.user.id
        # (file_id, sender_id) -> FileRequest
        self.__file_request_by_ids = {}
        columns = ('From', 'To', 'File')
        self.tree = ttk.Treeview(self.parent,
                                 columns=columns,
                                 show='headings')
        for column in columns:
            self.tree.heading(column, text=column)
            self.tree.column(column, stretch=True, minwidth=0, width=100)
        self.tree.tag_configure(
            FileRequestStatus.ACCEPTED, background='green', foreground='white')
        self.tree.tag_configure(
            FileRequestStatus.DECLINED, background='red', foreground='white')
        self.tree.pack(expand=True, fill=tk.BOTH)
        self.tree.bind("<Button-3>", self.on_right_click)

    def register_observers(self):
        self.app.file_requests_service.register_observer(self)

    def unregister_observers(self):
        self.app.file_requests_service.unregister_observer(self)

    @property
    def file_requests(self):
        return self.__file_request_by_ids.values()

    @file_requests.setter
    def file_requests(self, file_requests: List[FileRequest]):
        self.__file_request_by_ids = {(request.file_id, request.sender_id): request
                                      for request in file_requests}
        self.tree.delete(*self.tree.get_children())
        for file_request in self.app.file_requests_service.file_requests:
            self.tree.insert('', tk.END,
                             values=(file_request.sender_name,
                                     file_request.receiver_name,
                                     file_request.file_name),
                             tags=(file_request.file_id,
                                   file_request.sender_id,
                                   file_request.status))

    def update(self, subject):
        if isinstance(subject, self.app.file_requests_service.__class__):
            self.file_requests = subject.file_requests

    def on_right_click(self, event):
        iid = self.tree.identify_row(event.y)
        if iid:
            self.tree.selection_set(iid)
            tags = self.tree.item(iid)["tags"]
            file_request: FileRequest = self.__file_request_by_ids.get(
                (tags[0], tags[1]), None)
            if file_request is None:
                return
            if file_request.status == FileRequestStatus.PENDING:
                menu = tk.Menu(self.parent, tearoff=0)
                if file_request.sender_id == self.user_id:
                    menu.add_command(
                        label="Cancel",
                        command=lambda: self.app.file_requests_service.cancel(
                            file_request)
                    )
                else:
                    menu.add_command(
                        label="Accept",
                        command=lambda: self.app.file_requests_service.accept(
                            file_request)
                    )
                    menu.add_command(
                        label="Decline",
                        command=lambda: self.app.file_requests_service.decline(
                            file_request)
                    )
                menu.tk_popup(event.x_root, event.y_root)
        else:
            pass
