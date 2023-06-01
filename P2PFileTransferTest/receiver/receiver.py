import peer
import socket


receiver = peer.Peer("localhost", 7777)
receiver.request()