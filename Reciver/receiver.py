import peerR
import socket
import os

receiver = peerR.PeerR("localhost", 9999, "None")
receiver.request("TREM11")