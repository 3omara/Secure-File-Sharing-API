import json
import os
from typing import List
import socketio as sio
from dataclasses import replace
from shared.ObserverPattern import Subject
from models.FileRequest import FileRequest, FileRequestStatus


class FileRequestsRepository(Subject):
    SIO_NAMESPACE = "/file_requests"

    def __init__(self, client: sio.Client):
        super().__init__()
        self.client = client
        self.__file_requests = []
        self.client.on("init_file_requests",
                       self.__on_init_file_requests,
                       namespace=self.SIO_NAMESPACE)
        self.client.on("new_file_request",
                       self.__on_new_file_request,
                       namespace=self.SIO_NAMESPACE)
        self.client.on("delete_file_request",
                       self.__on_delete_file_request,
                       namespace=self.SIO_NAMESPACE)
        self.client.on("accept_file_request",
                       self.__on_accept_file_request,
                       namespace=self.SIO_NAMESPACE)
        self.client.on("decline_file_request",
                       self.__on_decline_file_request,
                       namespace=self.SIO_NAMESPACE)
        self.client.connect(
            os.getenv("SIO_HOST"),
            auth={"user_id": 1},
            transports=["polling", "websocket"],
            namespaces=[self.SIO_NAMESPACE],
        )

    @property
    def file_requests(self):
        return [*self.__file_requests]

    @file_requests.setter
    def file_requests(self, file_requests: List[FileRequest]):
        self.__file_requests = file_requests
        self.notify_observers()

    def insert(self, request: FileRequest):
        def on_uploaded(response):
            self.file_requests = [*self.__file_requests,
                                  FileRequest.from_response(response["data"])]
        self.client.emit("new_file_request",
                         request.to_response(),
                         callback=on_uploaded,
                         namespace=self.SIO_NAMESPACE)

    def delete(self, request: FileRequest):
        def on_deleted(response):
            self.file_requests = [request for request in self.__file_requests
                                  if request.file_id != response["data"]["file_id"]]
        self.client.emit("delete_file_request",
                         request.to_response(),
                         callback=on_deleted,
                         namespace=self.SIO_NAMESPACE)

    def accept(self, request: FileRequest):
        def on_accepted(response):
            self.file_requests = [request if request.sender_id != response["data"]["sender_id"]
                                  else replace(request, status=FileRequestStatus.ACCEPTED)
                                  for request in self.__file_requests]
        self.client.emit("accept_file_request",
                         request.to_response(),
                         callback=on_accepted,
                         namespace=self.SIO_NAMESPACE)

    def decline(self, request: FileRequest):
        def on_declined(response):
            self.file_requests = [request if request.sender_id != response["data"]["sender_id"]
                                  else replace(request, status=FileRequestStatus.DECLINED)
                                  for request in self.__file_requests]
        self.client.emit("decline_file_request",
                         request.to_response(),
                         callback=on_declined,
                         namespace=self.SIO_NAMESPACE)

    def __on_init_file_requests(self, response):
        self.file_requests = [FileRequest.from_response(request)
                              for request in response["data"]]

    def __on_new_file_request(self, response):
        self.file_requests = [*self.__file_requests,
                              FileRequest.from_response(response["data"])]

    def __on_delete_file_request(self, response):
        self.file_requests = [request for request in self.__file_requests
                              if request.file_id != response["data"]["file_id"]]

    def __on_accept_file_request(self, response):
        self.file_requests = [request if request.file_id != response["data"]["file_id"]
                              else replace(request, status=FileRequestStatus.ACCEPTED)
                              for request in self.__file_requests]

    def __on_decline_file_request(self, response):
        print(response)
        self.file_requests = [request if request.file_id != response["data"]["file_id"]
                              else replace(request, status=FileRequestStatus.DECLINED)
                              for request in self.__file_requests]
