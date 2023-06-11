import socket
import peerS
import os

sender = peerS.PeerS("localhost", 9999,"TREM")
sender.send()