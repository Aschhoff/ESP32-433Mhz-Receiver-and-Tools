

#Config for RX433_ESP.py

rx433=22          # GPIO
toleranz=25       # Toleranz der Pulse in %
rxlen=44          # Laenge der einzulesenden Liste bzw Pulse

debug="on"        # "on" printet alle Protokolle Daten usw

# WiFi -------------------------
ssid      = "Aschi"
password  = "2482694733144611"

# for static IP
ip        = "192.168.10.200"
subnet    = "255.255.255.0"
gateway   = "192.168.10.1"
dns       = "8.8.8.8"

#openhab_url="192.168.10.xxx:8080/items/" # for OPENHAB
#socket_ip=("192.168.10.26",8888)          # TCP Socket on Port  8888 

# Devices ----------------------

devices={"Therm01":{"prot":"ws1700","addr":"1328"},
         "Tswitch":{"prot":"chinatherm","addr":"43936","0":"off","1":"on"},
         "QUIGG":{"prot":"quigg7000","addr":"2816"},
         "Window":{"prot":"ev1527", "addr":"30164", "7":"close", "5":"open"},
         "Bell":{"prot":"ev1527", "addr":"535723", "2":"A", "8":"B", "1":"C", "4":"D"}
       }


























