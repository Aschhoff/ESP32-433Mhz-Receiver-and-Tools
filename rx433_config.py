


# Config for rx433_pi_auto.py

rx433=15            # Pin Schema  BCM!!!!  not GPIO  15 for ESP
toleranz=25         # Toleranz der Pulse in %
rxlen=103           # Laenge der einzulesenden Liste bzw Pulse

debug="on"          # "on" printet alle Protokolle Daten usw

ssid      = "your Router"
password  =  "xxxxxxxxxx"

#openhab_url="http://192.168.10.xxx/items/" # for OPENHAB
#socket_ip=("192.168.10.43",8888)           # UDP Socket   8888 for ESP



# Item/ Username  (Protokoll,  Addresse Keys as value to replace in text)
devices={"Therm01":{"prot":"ws1700","addr":"1328"},
         "Tswitch":{"prot":"chinatherm","addr":"43936","0":"off","1":"on"},
         "QUIGG":{"prot":"quigg7000","addr":"2816"},
         "Window":{"prot":"ev1527", "addr":"30164", "7":"close", "5":"open"},
         "Bell":{"prot":"ev1527", "addr":"535723", "2":"A", "8":"B", "1":"C", "4":"D"}
       }








