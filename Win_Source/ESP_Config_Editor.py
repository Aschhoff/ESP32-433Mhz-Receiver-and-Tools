
import time
from ESP_Config_load import *
from tkinter import *
from tkinter import ttk
import tkinter.scrolledtext as tkst
import tkinter.filedialog
from tkinter.messagebox import *

root=Tk()
root.title("ESP config.py Editor")
err=""

def saveconfig():
    hinweis.config(text="")
    global textfeld
    t = textfeld.get("1.0", "end-1c")       # t= Text aus Textfeld vom Zeile1 col 0 bis Ende
    err=ESPsave(filename,t)       # File zum ESP schicken
    if err=="ok":
        hinweis.config(text="File auf ESP gespeichert")
    else:
        hinweis.config(text="Fehler in der USB Verbindung")

def loaddir():
    textfeld.delete('1.0', END)     # Textfeld leer machen
    listdir=ESPloaddir()
    match=[]
    for i in listdir:
        if i.find("config")!= -1:   # match auf 'config' im File
            match.append(i)
    filename=match[0][2:-1]         # am Anfang und Ende ' und lf weg
    return(filename)
    
def loadconfig():
    textfeld.delete('1.0', END)     # Textfeld leer machen
    err=ESPloadfile(filename)
    if err=="ok":
        file=open(filename)
        txt=file.read()
        file.close()
        textfeld.insert("1.0",txt)
        hinweis.config(text="Datei: "+filename)
    else:
        hinweis.config(text="Fehler in der USB Verbindung")

def loadbackup():
    textfeld.delete('1.0', END)
    hinweis.config(text="")
    file=open(filename)#+"-backup")
    txt=file.read()
    file.close()
    textfeld.insert("1.0",txt)
    hinweis.config(text="Backup-Datei")
#----------------------------------------------------------------------------------   
#----------  Witgets laden

    
textfeld=tkst.ScrolledText(root,bg="black",fg="#4ede5a",insertbackground="#4ede5a")
textfeld.pack(expand="True",fill="both")

button2=ttk.Button(root, text="Load Config Backup", command=loadbackup)
button2.pack(side="right",padx="5")

button3=ttk.Button(root, text="Save Config ESP", command=saveconfig)
button3.pack(side="right",padx="5")

button1=ttk.Button(root, text="Load Config ESP", command=loadconfig)
button1.pack(side="right",padx="5")

hinweis = Label(root, fg = "black",bg = "lightgray")#, font = "Verdana 10")
hinweis.pack(side="left")

#------------------------------------------------------------------------------------

filename="rx433_config.py"

while True:
    err=Serialon()
    if err=="ok": 
        hinweistxt="ESP über USB angeschlossen"
        hinweis.config(text=hinweistxt)
        break
    else:
        if askyesno("Keinen ESP am COM Port gefunden!", "Nochmal versuchen?"):
            pass
        else:
            exit()

filename=loaddir()
loadconfig()

root.mainloop()       

