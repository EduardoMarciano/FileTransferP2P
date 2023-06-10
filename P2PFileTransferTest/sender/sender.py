import socket
import peer
import os

sender = peer.Peer("localhost", 9999,"F")
sender.send()