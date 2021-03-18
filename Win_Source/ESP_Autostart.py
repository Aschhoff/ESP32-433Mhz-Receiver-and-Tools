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
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import *
import serial

root=Tk()
root.title("ESP Autostart Changer")
err=""


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
            #ESPsend(chr(4))
            ESPsend(chr(3))
            time.sleep(1)
            
            if ser.inWaiting() != 0:
                ser.read()
                return (comport)
            else:
                serialopen=False
    return ("Error")
    
def ESPsend(out):
    out+="\r\n"
    out=out.encode("utf-8")
    ser.write(out)
    time.sleep(0.1)
    
def autooff():
    if ser.isOpen() == False:start()
    ESPsend("import os")
    ESPsend("os.rename('main.py','mainxxx.py')")
    time.sleep(0.5)
    res=""       
    while ser.inWaiting() != 0:
        a=ser.read()
        res+=a.decode("utf-8")
    pos=res.find("OSError")
    if pos==-1:
        hinweistxt="Autostart is off"
    else:
        hinweistxt="Autostart already off"
    hinweis.config(text=hinweistxt)
    stop()
    
def autoon():
    if ser.isOpen() == False:start()
    ESPsend("import os")
    ESPsend("os.rename('mainxxx.py','main.py')")
    res=""       
    while ser.inWaiting() != 0:
        a=ser.read()
        res+=a.decode("utf-8")
    pos=res.find("OSError")
    if pos==-1:
        hinweistxt="Autostart is on"
    else:
        hinweistxt="Autostart already on"
    hinweis.config(text=hinweistxt)
    stop()
    
def stop():
    ser.close()
    
def start():
    while True:
        res=""
        err=serialOn()
        if err!="Error":
            statustxt="ESP connectet on: "+err
            status.config(text=statustxt)
            ESPsend("import os")
            ESPsend("os.listdir()")
            while ser.inWaiting() != 0:
                a=ser.read()
                res+=a.decode("utf-8")
            if "main.py" in res:
                hinweistxt="Autostart is on"
            else:
                hinweistxt="Autostart is off"
            hinweis.config(text=hinweistxt)
            break
        else:
            if askyesno("No ESP found!!! Try again?"):
                ser.close()
                pass
            else:
                exit()


#----------------------------------------------------------------------------------   
#----------  Witgets laden


   
frameButton = Frame(root)
frameButton.pack(fill='both')
button2=Button(frameButton, text="Autostart ON              ", command=autoon)
button2.pack(side="right",padx="5",pady="2")

button1=Button(frameButton, text="Autostart OFF             ", command=autooff)
button1.pack(side="right",padx="5")

hinweis = Label(root, fg = "lightgreen",bg = "gray", font = "Verdana 10 bold" )
hinweis.pack(fill='both',padx="5",pady="2")
hinweistxt="Change Autostart "
hinweis.config(text=hinweistxt)

status = Label(root)
status.pack(fill='both',padx="5",pady="2")
statustxt="                               "
status.config(text=statustxt)
#------------------------------------------------------------------------------------

start()
root.mainloop() 
