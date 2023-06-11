import peerR
import socket
import os

receiver = peerR.PeerR(5353)
receiver.request("11112")