import json
import tkinter
from tkinter import *
from extract import class_prediction, get_response
from keras.models import load_model
import time
import sys
sys.stdout.reconfigure(encoding='utf-8')


# extraimos o modelo usando o keras
model = load_model(r'model.h5')

# carregamos nossas intenções
intents = json.loads(open('intents.json', encoding='utf-8').read())

base = Tk()
base.title("Chatbot")
base.geometry("800x650") 
base.resizable(width=TRUE, height=TRUE)


def chatbot_response(msg):
    """
        Resposta do bot
    """
    ints = class_prediction(msg, model)
    res = get_response(ints, intents)
    return res

def send():
    """
        Envia a mensagem
    """
    msg = EntryBox.get("1.0", 'end-1c').strip()
    EntryBox.delete("0.0", END)

    if msg != '':
        Chat.config(state=NORMAL)
        Chat.insert(END, f"Você: {msg}\n\n")
        Chat.config(foreground="#000000", font=("Arial", 12))

        response = chatbot_response(msg)
        Chat.insert(END, f"Botina: {response}\n\n")

        Chat.config(state=DISABLED)
        Chat.yview(END)

# Cria a janela do chat
Chat = Text(base, bd=0, bg="white", height="20", width="50", font="Arial",)
Chat.config(state=DISABLED)

# Vincula a barra de rolagem à janela de bate-papo
scrollbar = Scrollbar(base, command=Chat.yview)
Chat['yscrollcommand'] = scrollbar.set

# Cria o botão de envio de mensagem, onde o comando envia para a função de send
SendButton = Button(base, font=("Verdana", 10, 'bold'), text="Enviar", width="12", height=2, bd=0, bg="#666", activebackground="#333", fg='#ffffff', command=send)

# Cria o box de texto
EntryBox = Text(base, bd=0, bg="white", width="29", height="2", font="Arial")

# Coloca todos os componentes na tela
scrollbar.place(x=770, y=10, height=600)
Chat.place(x=10, y=10, height=570, width=750)
EntryBox.place(x=10, y=600, height=40, width=580)
SendButton.place(x=600, y=600, height=40, width=180)


base.mainloop()