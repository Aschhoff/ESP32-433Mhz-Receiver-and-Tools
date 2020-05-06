# Detlev Aschhoff info@vmais.de
# 433 RC Remote for Quigg GT 7000, Tevion, GT-FSI-04
#
# first 12 bit = Adresse   0 to 11
# 12,13 Units 0=00 1=10 2=11 3=01  4 to 7 same wiith dim bit 16
# 14 Command to all units
# 15 1 = on    0 = off    oder Dimmer up/ down
# 16 0= Switch    1 = Dimmer
# 17 allways 0
# 18 set with unit why ?????
# 19 even partity = 1
#
# zero    -------
#      --|
#
# one         --
#      -------|
# Sycn=80000, short=700 long=1400 microsek# Dekoder Quigg 7000 Protokoll
import json
prot_pat=(80000,700,1400,20)
def dekode(li):
    addr=0
    parity=li[:19].count(1)%2           # parity even 0
    if li[19]== parity:return "error"   # li[19] = 1 if parity even
    
    out={}
    out["prot"]="quigg7000" # Name of Protokol
    for n in range (12):    # Adresse in dezimal
      addr+=li[11-n]*2**n
    out["addr"]=str(addr)
    
    if li[12]==0 and li[13]==0:unit=1
    if li[12]==1 and li[13]==0:unit=2
    if li[12]==1 and li[13]==1:unit=3
    if li[12]==0 and li[13]==1:unit=4
    out["unit"]=str(unit)
    
    state=li[15]
    out["state"]=str(state)
    
    output=json.dumps(out)
    return output
  


