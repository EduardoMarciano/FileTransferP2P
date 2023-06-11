import Reciver
import socket
import os

receiver = Reciver.Reciver("localhost", 9999)
receiver.request("LTLT1")