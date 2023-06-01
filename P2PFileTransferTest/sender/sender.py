import socket
import peer

sender = peer.Peer("localhost", 7777)
sender.send()