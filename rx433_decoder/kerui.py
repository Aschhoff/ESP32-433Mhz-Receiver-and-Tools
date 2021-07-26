""" ev1527 Protokoll
popular for cheap contacts or switches with HS1527 chip

Timings:

Sync 
  _1             31
_| |____________________________

High
       3         1
  ___________
_|           |_______

Low
     1           3
   _____
__|     |____________

Example: Sycn=14000 Low =450  High= 1350

Bits are invers 0 is 1 and 1 is 0 
Protokol length = 24
Bits 0 to 19 Address  1 2 4 8 ....2**18
Bits 20 to 23 State   1 2 4 8
"""
import json

prot_pat=(9600,300,950,24)

def dekode(li):
    out={}
    addr=0
    state=0
    
    out["prot"]="kerui"        # Name of Protokol
    #for n in range (20):
    #  addr+=li[19-n]*2**n
    for n in range (20):
      addr+=(not li[n])*2**n    # Bits are invers 0 is 1 and 1 is 0 
    out["addr"]=str(addr)       # Device Address in dezimal
    
    for n in range (4):
      state+=(not li[20+n])*2**(n)
    out["state"]=str(state)      # State bits 20 21 22 23 to dezimal  0 to 15
    
    output=json.dumps(out)      # return DICT as String

    return output

  

