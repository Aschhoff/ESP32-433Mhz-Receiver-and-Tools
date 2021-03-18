





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


#----------------------------- Puls Detection ---------------------------
def rxpuls(pin):

  global puls_length_raw                # Liste fuer Impulse
  global count 
  if count<rxlen:
    puls=time_pulse_us(rx,0)              # puls ist Laenge Low am Pin
    if puls>250 and count<rxlen:
      puls_length_raw[count]=puls         # wenn > 250us in Liste eintragen
      count+=1
  else: 
    analyse()                           # wenn Liste voll zur Analyse
    count=0
# Output: Liste der Impulslaengen   

#----------------------------- Pulsliste nach Sync und Daten durchsuchen  ----------------------------
# Input: puls_length_raw (Liste der Impulslaengen aus rxpulse)
 
def sniff():
  global puls_length_raw               # globale Liste der Impulslaengen Low
  nix="*"
  posi=[]
  list_binary=[]
  prot_pattern=[]
  data_raw=[]

  sync=max(puls_length_raw)            # Sync Impuls
  tol=toleranz/100

  for n in range(len(puls_length_raw)):     # Sync Impulse suchen
    if puls_length_raw[n]>(sync*(1-tol)):
      posi.append(n)
  
  if len(posi)>=2 and len(posi)<5:    # Anzahl Sync Impule in der Liste   
    anz_posi=len(posi)-1

    for segment in range(anz_posi):   # einzelne Segmente
      list_binary=[]
      ready=0                         # jedes Segment analysieren
      data_raw=puls_length_raw[(posi[segment]+1):(posi[segment+1])]
      if len(data_raw)<15:continue
      short_low= min(data_raw)        # kurzer Puls pro Segment
      long_low = max(data_raw)        # langer puls
      for n in range(len(data_raw)):  # Liste nach kurz oder lang durchsuchen

        if data_raw[n]<short_low*(1+2*tol):
          list_binary.append(0)            # Null in Liste 
        elif data_raw[n]>long_low*(1-tol):
          list_binary.append(1)            # Eins in Liste
        else:
          ready=1
          break                            # Puls nicht erkannt Abbruch
          

#     Vergleich prot_pattern und Items aus config - Protokoll Name suchen  
      if ready==0 and len(list_binary)>15:       
        prot_length=len(list_binary)       # Laenge des Protokolls
        prot_pattern= sync,short_low,long_low,prot_length
        #print(prot_pattern)
        prot_dec=nix
        for i in protokolle.items():       # Patter vergleichen mit Eintraegen in rx433_config.py protokolle
          if prot_pattern[0]> i[1][0]*(1-tol) and prot_pattern[0]< i[1][0]*(1+tol) and prot_pattern[3] == i[1][3]: 
              prot_dec = i[0]              # Protokoll Name gefunden
              #print(prot_dec)
              return prot_pattern,prot_dec,list_binary  # return Protokoll Name und Bitliste, bei Fehler "*"
       #return Werte als DICT
        
  return prot_pattern,nix,list_binary
#Output:   Protokoll Pattern sync,short_low,long_low,prot_length  und  list_binary als 0 1   
 #-----------------------------------------------------------------------------------------  

def analyse():

  global list_binary
  
  prot_pattern,prot_dec,list_binary=sniff() # Dekodiertes Protokoll als Liste
  
  if prot_pattern != [] and debug=="on":
    list_str=[str(i) for i in list_binary]  # Puls Liste als String
    list_str="".join(list_str)
    sniff_out=prot_pattern,list_str,prot_dec
    
    print("--> ",json.dumps(sniff_out))     # Raw Daten
    
  if prot_dec!="*":                         # nicht * dh Protokoll erkannt
    bef=prot_dec+".dekode(list_binary)"     # erkanntes Protokoll in bef
    prot_dict_str=eval(bef)                 # eval => ausfueren von String bef als Befehl, Dekodierung
    if debug=="on":
        print("==> ",prot_dict_str)         # decodierte Daten
        
 #  Daten aufbereiten  mit config Daten----------------------------  
    if prot_dict_str!="error" and prot_dict_str!="repeat":      # no Repeat and no error in Decode

      prot_dict=json.loads(prot_dict_str)
      for uname in devices:
        dev=devices[uname]
        if dev["prot"]==prot_dict["prot"] and dev["addr"]==prot_dict["addr"]: # Match Receive Prot with config
           
          if "state" in prot_dict:            # ist state im output des Dec Moduls 
              if prot_dict["state"] in dev:   # ist der state auch in config              
                  state=dev[prot_dict["state"]]
                  prot_dict["state"]=state    # austauschen gegen Klartext aus config                 
          prot_dict.pop("prot")               # Protokollname und Adresse weg
          prot_dict.pop("addr")   
          prot_dict["device"]=uname           # austauschen gegen frindly name/item 


#------------------------------  WIFI on ------------------------------
          if socket_ip!="" or openhab_url!="":
            wifi.connect(ssid,password)
            time.sleep(0.3)
#------------------------------ Out as DICT to Socket -----------------
          if socket_ip!="":
            sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)          
            out_socket=json.dumps(prot_dict)
            try:
              #dummy=sock.sendto(out_socket.encode(),socket_ip)
              sock.connect(socket_ip)
              sock.send(out_socket.encode())
              sock.close()
            except:
              if debug=="on":print("Kein Socket erreichbar!")
            if debug=="on":
              print("Socket: ",out_socket)
          
#------------------------------ Out to OpenHAB ------------------------------ 
          if openhab_url!="":
            item=prot_dict["device"]
            if len (prot_dict)>2:
                for n in prot_dict:
                    if n !="device":
                        itemx=item+"_"+n
                        data=prot_dict[n]
                        sendToOpenhab(itemx,data)
            else:
                sendToOpenhab(item,prot_dict["state"])

                  
          if debug=="on":print(80*"-") 
          if socket_ip!="" or openhab_url!="":  
            time.sleep(0.3)        
            wifi.disconnect()    
          break
#------------------------------------  to Openhab  ---------------------------        
          
def sendToOpenhab(item,data):
    if debug=="on":
      print("OPENHAB: ","http://"+openhab_url+"/rest/items/"+item,data)
    # OpenHAB API aufrufen
    try:
      url="http://"+openhab_url+"/rest/items/"+item
      headers = {'Content-type': 'text/plain'}
      response = urequests.post(url, data=data, headers=headers) 
    except:
      if debug=="on":print("Kein OpenHab erreichbar!")
    #pprint.pprint(response.json())
#------------------------------------  Main Loop ---------------------------

import time
import json
import wifi
import esp
esp.osdebug(None)
from os import listdir
import sys
from machine import Pin,time_pulse_us
import gc

socket_ip=""
openhab_url=""
debug="off"
from RX_config import * # importiere config mit var Namen 
#wifi.connect(ssid,password)

if socket_ip!="":
  import socket
  
if openhab_url!="":
  import urequests  
  
puls_length=[]
count=0
start=time.ticks_us()
puls_length_raw=[]
list_binary=[]
for n in range(rxlen):puls_length_raw.append(0) # Liste mit 0 und Laenge rxlen

protokolle={}

sys.path.append("./RX_decoder")
dirs = listdir( "./RX_decoder")
for prot in dirs:               # aus Path rx433_protokoll Dekoder Module
  if prot[-3:]==".py":
    a=prot[:-3]                 # Name des Dekodiermoduls aus Dir rx433_protokoll
    print(a)
    locals()[a]=__import__(a)
    protokolle[a]=locals()[a].prot_pat
    # erzeuge locale Variable aus String a => 
    # import modul mit Name aus Variable a

print("Start Rx433")
rx = Pin(rx433,Pin.IN,pull=None)                 # Input Pin hochohmig
rx.irq(handler=rxpuls, trigger=Pin.IRQ_FALLING)  # Interrupt 1 -> 0 Aufruf rxpulse
gc.enable()


while True:
  try:
    time.sleep(1)
  except KeyboardInterrupt:
    rx.irq(handler=rxpuls, trigger=0) # IRQ abschalten und Exit
    raise ValueError("Programm stopp")      














































