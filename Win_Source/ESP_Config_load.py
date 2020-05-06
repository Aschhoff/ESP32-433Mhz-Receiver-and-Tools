import serial
import time
comliste=("COM2:","COM3:","COM4:","COM5:","COM6:")

def Serialon():
    global ser
    for comport in comliste:
        try:
            ser = serial.Serial(port=comport,baudrate=115200)
            serialopen=True
        except Exception as e:
            print ("error open serial port: " + str(e))
            serialopen=False            
        if serialopen == True:
            time.sleep(2)
            ESPsend(chr(3))
            if ser.inWaiting() > 1000:
                ser.read()
                return ("ok")
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

    #t=t.replace("\r","\\r")     # LF wandeln in escaped \\r

    for i in tline:
        #out=i.replace("\r","\\r")     # LF wandeln in escaped \\r
        out=i+"\\r"     # LF wandeln in escaped \\r
        ESPsend("dummy=file.write('"+out+"')") # Zeile an ESP
        time.sleep(0.05)                # sonst verschluckt sich der ESP
    ESPsend('file.close()')
    return("ok")

def ESPloadfile(filename):
    ser.reset_input_buffer()
    fileopen='file = open("'+filename+'")'
    ESPsend(fileopen)
    ser.reset_input_buffer()    
    ESPsend("file.read()")      # Kommando an ESP
    txt1=ser.readline()     # Echo vom gesendetem Befehle abholen
    txt2=ser.readline()     # Daten vom ESP
    txt=txt2.decode()
    txt=txt[1:-3]           # Zeichen ' an Anfang und 'cr lf am Ende weg
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
    txt1=ser.readline()     # Echo vom gesendetem Befehle abholen
    txt2=ser.readline()     # Daten vom ESP
    txt=txt2.decode()
    listdir=txt.split(",")  # String mit ['abc','cde'  in Liste wandeln
    return(listdir)
    