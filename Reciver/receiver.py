import peerR
import socket
import os

receiver = peerR.PeerR(5600)
receiver.request("TTT")