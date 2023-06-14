import socket
import os
import datetime
import time
import peerR

receiver = peerR.PeerR(5600)
receiver.request("BRTT")