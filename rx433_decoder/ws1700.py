
import json
ws1700_alt=""
#Dekoder ws1700 Protokoll Pearl Thermometer
prot_pat=(9000,1900,3800,36)
def dekode(li):
    global ws1700_alt
    addr=0
    temp=0
    hum=0
    bat=0
    out={}
    header_soll=[0,1,0,1]
    if li[0:4]==header_soll:    # if right Header of  ws1700 Protokoll
        out["prot"]="ws1700"
        for n in range (4,12): 
          addr+=li[11-n]*2**n   # Adresse umwandeln bits in dezimal                
        out["addr"]=str(addr) 

        bat=li[12]
        out["bat"]=str(bat)

        tempbin=li[16:28]       # Temp umwandeln bits in dezimal  
        for n in range (0,12):
          temp+=tempbin[11-n]*2**n
        out["temp"]=str(temp/10) 

        humbin=li[28:]          # Hum umwandeln bits in dezimal 
        for n in range (0,8):
          hum+=humbin[7-n]*2**n   
        out["hum"]=str(hum) 

        output=json.dumps(out)
        
        if output == ws1700_alt:         # has state changed?
          return("repeat")                # same Values return
        ws1700_alt=output
        return output
    return "error"
   




