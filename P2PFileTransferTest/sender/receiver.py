import peer
import socket
import os

receiver = peer.Peer(9999, "None")
receiver.request("SSS")