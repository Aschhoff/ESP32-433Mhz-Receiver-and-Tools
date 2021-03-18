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


#----------------------------- ESP 433Mhz Sniffer ---------------------------

#   on ESP must run rx433_ESP433RX.py and debug = on

#----------------------------------------------------------------------------        
def serialOn():
    global ser
    for port in range(3,9):
        comport="COM"+str(port)+":"
        try:
            ser = serial.Serial(port=comport,baudrate=115200)
            serialopen=True
        except Exception as e:
            #print ("error open serial port: " + str(e))
            serialopen=False            
        if serialopen == True:
            ESPsend(chr(3))
            ESPsend(chr(4))
            time.sleep(1)
            
            if ser.inWaiting() != 0:
                a=ser.read()
                return (comport)
            else:
                serialopen=False
    return ("Error")        

def ESPsend(out):
    out+="\r\n"
    out=out.encode("utf-8")
    ser.write(out)
    time.sleep(0.05)                # sonst verschluckt sich der ESP
    
def anzeigeLeer():
    textRaw.delete('1.0', END)
    
def ESPloadprot():
    line1="*"
    line2="*"
    while ser.in_waiting >40:
        line=ser.readline()        # Zeilenweise holen
        line=line.decode()
        if line.find("-->") >-1:   # 1.Zeile RAW Protokoll
            line1=line[5:]

        if line.find("==>") >-1 and line.find("repeat") == -1 :
            line2=line[5:]         # 2.Zeile DEC Protokoll

    return line1,line2

    
def anzeigeRaw(protRaw):
    protPattern=str(protRaw[0])
    binData=protRaw[1]
    prot=protRaw[2]
    zeit=time.strftime("%H:%M:%S", time.localtime())
    
    protRawout="{} {:>10}{:>42}{:>10}".format(zeit,protPattern,binData,prot)
    textRaw.insert('1.0',protRawout+chr(10))   # Pattern auflisten 
    if log==1:
        
        protPattern=json.loads(protPattern)
        logRawout="'{}',{},{},{},{},'{}','{}'\n".format(zeit,protPattern[0],protPattern[1],protPattern[2],protPattern[3],binData,prot)
        
        file=open(filename,"a")
        file.write(logRawout)
        print("LOG ",logRawout)
        file.close()
    
    
def anzeigeDec(highlight):
    nr=0
    textDec.delete('1.0', END)
    for i in anzDec:                # Durchlauf anzDec alle recv Protokolle
        nr+=1
        anzKeys=i.keys()            # Keys im Protokoll aus anzDec
        protProt=i["prot"]
        protAddr=i["addr"]          # Protokoll und Adresse aus anzDec

        anz="{:>2}{:>8}{:>10}".format(nr,protProt,protAddr)# formatieren
        hl=""
        for n in anzKeys:
            if n!="prot" and n!="addr": # Eintraege ausser Prot und addr als String
                anz+="  "+n+" "+i[n]+" "
      
        if i==highlight:            # letzte revc Protokoll
            hl="repeat"             # hl repeat ist Name aus textDec.tag_config 
        anz=anz+chr(10)

        textDec.insert(END,anz,hl)  # Protokolle auflisten hl Farben setzen

def start():
    global anzDec
    global blink
    anz=""
    line1,line2=ESPloadprot()
    
    if line1!="*":
        protRaw=json.loads(line1)    
        anzeigeRaw(protRaw)         # Anzeigemit Protokollnummer in anzDec            
    
    if line2!="*":
        protDec=json.loads(line2)
        if anzDec==[]:              # Liste am Anfang einmal fuellen
            anzDec.append(protDec)
            anzeigeDec(0)
        
        repeatDec=0
        for existDec in anzDec:     # ist das Protokoll schon in der anzDec
            if protDec == existDec:
                repeatDec=existDec
                break
            
        if repeatDec==0:            # nein dann anhaengen      
            anzDec.append(protDec)
        anzeigeDec(existDec)        # Anzeige mit Protokollnummer in anzDec
        
    if blink==0:
        live.config(text="receive :")
        blink=1
    else:
        live.config(text="receive .")
        blink=0
        
    root.after(100,start)           # Tkinter Timer in ms

def loggerOn():
    global log
    log=1
    button1.config(fg="red")
def loggerOff():
    global log
    log=0
    button1.config(fg="black")
#----------------------------------------------------------------------------------

import time
import json
import serial

from tkinter import *
from tkinter import ttk
import tkinter.scrolledtext as tkst
import tkinter.filedialog
from tkinter.messagebox import *

root=Tk()
root.title("ESP 433 Sniffer")

filename="ESP433Logger.csv"
anzDec=[]
blink=0
log=0
    
#----------------------------------------------------------------------------------   
#----------  Witgets laden

frameoben = Frame(root)
frameoben.pack(fill='both')



button1=Button(frameoben, text="Logger on", command=loggerOn)
button1.pack(side ="left",padx="3",pady="15")

button3=Button(frameoben, text="Logger off", command=loggerOff)
button3.pack(side ="left",padx="3")

button2=Button(frameoben, text="Raw Data clear", command=anzeigeLeer)
button2.pack(side ="left",padx="8")

live=Label(frameoben, text="")
live.pack(side ="right",padx="8")

headerRaw1txt="433Mhz Raw Data"
headerRaw1=Label(root, font = "Verdana 10 bold",text=headerRaw1txt)
headerRaw1.pack(fill='both')
    
headerRawtxt="{:<13}{:^15}{:^70}{:<10}".format("Time","Sync   Short   Long  Len  ","Data","Protokol")
headerRaw=Label(root,anchor='w', font = "Verdana 10",text=headerRawtxt)
headerRaw.pack(fill='both')

textRaw=Text(root, height=10,bg="black",fg="#4ede5a",insertbackground="#4ede5a")
textRaw.pack(expand="True",fill="both")

headerDec1txt="433Mhz decode Data"
headerDec1=Label(root, font = "Verdana 10 bold",text=headerDec1txt)
headerDec1.pack(fill='both')

headerDectxt="{:^10}{:^10}{:<50}".format("     Protokol","      Address","   Data/State")
headerDec=Label(root,anchor='w', font = "Verdana 10",text=headerDectxt)
headerDec.pack(fill='both')

textDec=tkst.ScrolledText(root,bg="black",fg="#4ede5a",insertbackground="#4ede5a")
textDec.pack(expand="True",fill="both")
textDec.tag_config("repeat",foreground="yellow")


hinweis = Label(root, fg = "black",bg = "lightgray")#, font = "Verdana 10")
hinweis.pack(side="left")

#------------------------------------------------------------------------------------

while True:
    err=serialOn()
    if err!="Error": 
        hinweistxt="ESP connected on USB  :  "+err
        hinweis.config(text=hinweistxt)
        break
    else:
        if askyesno("No ESP fount on COM Port!", "Try again?"):
            pass
        else:
            exit()

start()

root.mainloop()       

