import socket
import Sender
import os

sender = Sender.Peer("localhost", 9999,"LTLT1")
sender.send()