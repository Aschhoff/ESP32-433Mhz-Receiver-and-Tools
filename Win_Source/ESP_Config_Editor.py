
# Detlev Aschhoff info@vmais.de
# The MIT License (MIT)
#
# Copyright (c) 2020
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


import time
import serial
from tkinter import *
from tkinter import ttk
import tkinter.scrolledtext as tkst
import tkinter.filedialog
from tkinter.messagebox import *

root=Tk()
root.title("ESP config.py Editor")
err=""
def serialOn():
    global ser
    for port in range(3,9):
        comport="COM"+str(port)+":"
        try:
            ser = serial.Serial(port=comport,baudrate=115200)
            serialopen=True
        except Exception as e:
            serialopen=False            
        if serialopen == True:
            ESPsend(chr(3))
            time.sleep(1)
            ESPsend(chr(3))
            time.sleep(1)            
            if ser.inWaiting() != 0:
                a=ser.read()
                print(a)
                return (comport)
            else:
                serialopen=False
    return ("Error") 
        
    
def ESPsend(out):
    out+="\r\n"
    out=out.encode("utf-8")
    ser.write(out)
    time.sleep(0.05)                # sonst verschluckt sich der ESP
    
def ESPsave(filename,t):
    ser.reset_input_buffer()        # Input Buffer leer
    fileopen='file=open("'+filename+'","w")'    # Kommando an ESP open File
    ESPsend(fileopen)
    tline=t.splitlines()

    for i in tline:
        out=i+"\\r"         # Zeilenende escaped \\r
        ESPsend("dummy=file.write('"+out+"')") # Zeile an ESP
        time.sleep(0.05)    # sonst verschluckt sich der ESP
    ESPsend('file.close()')
    return("ok")

def ESPloadfile(filename):
    ser.reset_input_buffer()
    fileopen='file = open("'+filename+'")'
    ESPsend(fileopen)
    ser.reset_input_buffer()    
    ESPsend("file.read()")  # Kommando an ESP
    txt1=ser.readline()     # Echo vom gesendetem Befehle abholen
    txt2=ser.readline()     # Daten vom ESP
    txt_dec=txt2.decode()
    txt=txt_dec[1:-3]           # Zeichen ' an Anfang und 'cr lf am Ende weg
    out=txt.replace("\\r",chr(10))  # \\r escaped CR nach LF
    save=open(filename,'w')
    save.write(out)     
    ESPsend("file.close()")
    return("ok")
    
def ESPloaddir():
    ser.reset_input_buffer() 
    ESPsend("import os")
    ser.reset_input_buffer()
    ESPsend("os.listdir()")
    time.sleep(0.5)
    txt1=ser.readline()     # Echo vom gesendetem Befehle abholen
    txt2=ser.readline()     # Daten vom ESP
    txt=txt2.decode()
    listdir=eval(txt)       # Liste aus String 
    return(listdir)
    
def saveconfig():
    hinweis.config(text="")
    global textfeld
    t = textfeld.get("1.0", "end-1c")       # t= Text aus Textfeld vom Zeile1 col 0 bis Ende
    hinweis.config(text="File wird gespeichert")
    err=ESPsave(filename,t)       # File zum ESP schicken
    if err=="ok":
        hinweis.config(text="File auf ESP gespeichert")
    else:
        hinweis.config(text="Fehler in der USB Verbindung")

def loaddir(file):
    textfeld.delete('1.0', END)     # Textfeld leer machen
    listdir=ESPloaddir()
    match=[]
    filename="Error"
    for i in listdir:
        if i.find(file)!= -1:   # match auf file in Listdir
            match.append(i)
            print(i)
    if match!=[]:filename=match[0]   
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

file="config.py" # Editor File

while True:
    err=serialOn()
    if err!="Error":
        statustxt="ESP connectet on: "+err
        hinweis.config(text=statustxt)
        break
    else:
        if askyesno("Keinen ESP am COM Port gefunden!", "Nochmal versuchen?"):

            continue
        else:
            exit()
print("--",ser)
filename=loaddir(file)
if filename=="Error":
    if showwarning(file+" nicht gefunden!\n Abbruch"):
        exit()
loadconfig()

root.mainloop()       

