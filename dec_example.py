# Example for Decoder

import json

"""Prot Pattern are the characteristic of the protokol
Length of Sync short and long bits in microseconds , protocol length in bits
thats to identify and load the right decoder.

Timings example:

Sync 
  _             
_| |____________________________

High
               
  ___________
_|           |_______

Low
                
   _____
__|     |____________

Example: Sycn=14000 Low =400  High= 1400"""

prot_pat=(14000,400,1400,24)


def dekode(li):					# li is a list of strings ['1','0','1','1' ............]
    out={}
    addr=0
    bef=[]
    
    out["prot"]="xyz"    		# Name of Protokol !!! must be the same as the filename xyz.py
	
    for n in range (11):        # decode the bits to data content
      addr+=li[11-n]*2**n
    out["addr"]=str(addr)       # put it to the out dirctory
	
								# ... may be more to decode
								
    bef=li[15]                  #
    out["state"]=str(bef)       # state put to the out dirctory
    
    output=json.dumps(out)      # return DICT as String
    return output

  

