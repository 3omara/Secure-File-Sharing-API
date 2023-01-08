import tkinter as tk
from tkinter import ttk
from models.FileRequest import FileRequest, FileRequestStatus

from views.View import View


class RequestsView(View):
    def setup_view(self):
        self.user_id = 1
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
        self.tree.bind("<Button-3>", self.on_right_click)

    def register_observers(self):
        self.app.file_requests_service.register_observer(self)

    def unregister_observers(self):
        self.app.file_requests_service.unregister_observer(self)

    def update(self, subject):
        if isinstance(subject, self.app.file_requests_service.__class__):
            self.tree.delete(*self.tree.get_children())
            for file_request in self.app.file_requests_service.file_requests:
                self.tree.insert('', tk.END,
                                 values=(file_request.sender_name,
                                         file_request.file_name),
                                 tags=(file_request,
                                       file_request.status))

    def on_right_click(self, event):
        iid = self.tree.identify_row(event.y)
        if iid:
            self.tree.selection_set(iid)
            file_request: FileRequest = self.tree.item(iid)["tags"][0]
            menu = tk.Menu(self.parent, tearoff=0)
            if file_request.status == FileRequestStatus.PENDING:
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
