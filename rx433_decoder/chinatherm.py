
chinatherm_alt=""
import json
# Protokoll China Thermostat
prot_pat=(1300,300,600,33)
def dekode(li):
  global chinatherm_alt

  addr=0
  bef=0
  out={}

  out["prot"]="chinatherm"    # Thermostat aus China
  for n in range (16):   
    addr+=li[11-n]*2**n
  out["addr"]=str(addr)       #Device Adresse in dezimal
  if li[24]==0 and li[25]==1:bef=0 # state OFF
  if li[24]==1 and li[25]==0:bef=1 # state ON
  out["state"]=str(bef)
  
  output=json.dumps(out)
  if output == chinatherm_alt:    # has state changed?
   return("repeat")                # same Values return
  chinatherm_alt=output
  return output

 







