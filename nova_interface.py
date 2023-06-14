from tkinter import *
from tkinter import filedialog
import os
class Application:
    def __init__(self, master=None):
        
        ### Container do Sender ###
        self.senderContainer = Frame(master)
        self.senderContainer["pady"] = 10
        self.senderContainer.pack()
        self.escolhaDocumentos = Frame(master)
        self.escolhaDocumentos["padx"] = 20
        self.escolhaDocumentos.pack(side=TOP)
        self.chaveSender = Frame(master)
        self.chaveSender["padx"] = 20
        self.chaveSender["pady"] = 20
        self.chaveSender.pack(side=TOP)
        self.tituloSender = Label(self.senderContainer, text="Sender")
        self.tituloSender["font"] = ("Roboto Slab", "10", "bold")
        self.tituloSender.pack()
        self.documentoLabel = Label(self.escolhaDocumentos, text="Selecione um ou mais arquivos:  ")
        self.documentoLabel.pack(side=LEFT)
        self.buttonDocumentos = Button(self.escolhaDocumentos)
        self.buttonDocumentos["text"] = "Escolha um documento"
        self.buttonDocumentos["font"] = ("Calibri", "8")
        self.buttonDocumentos["width"] = 10
        self.buttonDocumentos["padx"] = 40
        self.buttonDocumentos["command"] = self.buttonEscolheDocumentos
        self.buttonDocumentos.pack(side=RIGHT)
        self.chaveSenderLabel = Label(self.chaveSender, text="Insira sua chave identificadora:  ")
        self.chaveSenderLabel.pack(side=LEFT)
        self.chaveSenderEntrada = Entry(self.chaveSender)
        self.chaveSenderEntrada["width"] = 20
        self.chaveSenderEntrada["font"] = ("Arial", "10")
        self.chaveSenderEntrada.pack(side=RIGHT)
        ###Tabela de arquivos selecionados sender###
        self.tableArchivesSender = Frame(self.senderContainer)
        self.tableArchivesSender["pady"] = 10
        self.tableArchivesSender.pack(side=BOTTOM)
        self.buttonEnviar = Button(self.senderContainer)
        self.buttonEnviar["text"] = "Enviar"
        self.buttonEnviar["font"] = ("Calibri", "8")
        self.buttonEnviar["width"] = 10
        #self.buttonEnviar["command"] = self.enviarDocumentos
        self.buttonEnviar.pack(side=BOTTOM)
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
        self.buttonPesquisar = Button(self.receiverContainer)
        self.buttonPesquisar["text"] = "Pesquisar"
        self.buttonPesquisar["font"] = ("Calibri", "8")
        self.buttonPesquisar["width"] = 10
        self.buttonPesquisar["padx"] = 40
        #self.buttonPesquisar["command"] = self.buttonEscolheDocumentos
        self.buttonPesquisar.pack(side=RIGHT)
        ###Tabela de arquivos selecionados receiver###
        self.tableArchivesReceiver = Frame(self.receiverContainer)
        self.tableArchivesReceiver["pady"] = 10
        self.tableArchivesReceiver.pack(side=BOTTOM)
    def buttonEscolheDocumentos(self):
        self.files = filedialog.askopenfilenames()
        temp = [("Nome", "Tamanho")]
        for i in range(len(self.files)):
            file = os.path.basename(self.files[i])
            size = f'{os.stat(self.files[i]).st_size / 1024:.2f}' + " KB"
            temp.append((file, size))
        self.files = temp[:]
        #print(self.files)
        self.atualizaTabelaSender()
    def atualizaTabelaSender(self):
        for i in range(len(self.files)):
            for j in range(2):
                if (i == 0):
                    self.tabela = Entry(self.tableArchivesSender, width=20, bg='LightSteelBlue',fg='Black',
                                       font=('Arial', 10, 'bold'))
                else:
                    self.tabela = Entry(self.tableArchivesSender, width=20, font=("Arial", 10))
                self.tabela.grid(row=i, column=j)
                self.tabela.insert(END, self.files[i][j])
            # self.buttonExcluirLinha = Button(self.tabela)
            # self.buttonExcluirLinha["text"] = "Excluir"
            # self.buttonExcluirLinha["font"] = ("Calibri", "8")
            # self.buttonExcluirLinha["width"] = 5
            # self.buttonExcluirLinha["command"] = lambda: self.files.pop(i); self.atualizaTabela
            # self.tabela.grid(row=i, column=2)
            # self.tabela.insert(END, self.buttonExcluirLinha)
            # self.buttonExcluirLinha.pack()
       
    
root = Tk()
Application(root)
root.mainloop()