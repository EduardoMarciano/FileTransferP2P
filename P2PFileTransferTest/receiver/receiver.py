import peer
import socket
import os

receiver = peer.Peer("localhost", 9999)
receiver.request()