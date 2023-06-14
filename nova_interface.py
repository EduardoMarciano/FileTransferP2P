from tkinter import *
from tkinter import messagebox
from peerR import PeerR
from peerS import PeerS

class Application:
    def __init__(self, master=None):
        
        ### Container do Sender ###
        self.senderContainer = Frame(master)
        self.senderContainer["pady"] = 10
        self.senderContainer.pack()
        
        
        self.chaveSender = Frame(master)
        self.chaveSender["padx"] = 20
        self.chaveSender["pady"] = 20
        self.chaveSender.pack(side=TOP)
        
        self.tituloSender = Label(self.senderContainer, text="Sender")
        self.tituloSender["font"] = ("Roboto Slab", "10", "bold")
        self.tituloSender.pack()
    
        self.chaveSenderLabel = Label(self.chaveSender, text="Insira sua chave identificadora:  ")
        self.chaveSenderLabel.pack(side=LEFT)
        
        self.chaveSenderEntrada = Entry(self.chaveSender)
        self.chaveSenderEntrada["width"] = 20
        self.chaveSenderEntrada["font"] = ("Arial", "10")
        self.chaveSenderEntrada.pack(side=RIGHT)

        self.buttonSincroniazr = Button(self.senderContainer)
        self.buttonSincroniazr["text"] = "Sincronizar"
        self.buttonSincroniazr["font"] = ("Calibri", "8")
        self.buttonSincroniazr["width"] = 10
        self.buttonSincroniazr["command"] = self.sincronizarPasta
        self.buttonSincroniazr.pack(side=BOTTOM)
        
        ### Container do Receiver ###
        self.receiverContainer = Frame(master)
        self.receiverContainer["pady"] = 10
        self.receiverContainer.pack()
        
        self.tituloReceiver = Label(self.receiverContainer, text="Receiver")
        self.tituloReceiver["font"] = ("Roboto Slab", "10", "bold")
        self.tituloReceiver.pack()
        
        self.chaveReceiver = Frame(master)
        self.chaveReceiver["padx"] = 20
        self.chaveReceiver["pady"] = 20
        self.chaveReceiver.pack()
        
        self.chaveReceiverLabel = Label(self.chaveReceiver, text="Insira a chave primária do Sender:  ")
        self.chaveReceiverLabel.pack(side=LEFT)
        self.chaveReceiverEntrada = Entry(self.chaveReceiver)
        self.chaveReceiverEntrada["width"] = 20
        self.chaveReceiverEntrada["font"] = ("Arial", "10")
        self.chaveReceiverEntrada.pack(side=RIGHT)
        
        self.buttonSincronizarReceiver = Button(self.receiverContainer)
        self.buttonSincronizarReceiver["text"] = "Sincronizar"
        self.buttonSincronizarReceiver["font"] = ("Calibri", "8")
        self.buttonSincronizarReceiver["width"] = 10
        self.buttonSincronizarReceiver["command"] = self.sincronizarReceiver
        self.buttonSincronizarReceiver.pack(side=BOTTOM)


    def sincronizarPasta(self):
        chaveSender = self.chaveSenderEntrada.get()

        if (chaveSender == ''):
            messagebox.showwarning(title="Alerta!", message="Insira sua chave identificadora.")
        else:
            peerS = PeerS(port=5600, chave=chaveSender)
            peerS.send()

    def sincronizarReceiver(self):
        chaveReceiver = self.chaveReceiverEntrada.get()

        if (chaveReceiver == ''):
            messagebox.showwarning(title="Alerta!", message="Insira a chave identificadora do Sender.")
        else:
            peerR = PeerR(5600)
            peerR.request(chaveReceiver)
    
root = Tk()
Application(root)
root.mainloop()