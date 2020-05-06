


def connect(ssid,password):
    import network
    import time
    import machine

    ip        = "192.168.10.200"
    subnet    = '255.255.255.0'
    gateway   = '192.168.10.1'
    dns       = '8.8.8.8'
    #ssid      = "Aschi"
    #password  =  "2482694733144611"
    station = network.WLAN(network.STA_IF)  # Now the File exist so make Connection 

    if station.isconnected() == True:
      print("Schon verbunden")
      return

    station.active(True)
    if len(ip) > 7:     # mit fester IP
       station.ifconfig((ip,subnet,gateway,dns))
    station.connect(ssid,password)
    station.isconnected()
    count=0
    while not station.isconnected():
      time.sleep(0.1)
      print("*",end="")
      count+=1
      if count> 100: # Error open connection from File
        break
    print(station.ifconfig())

def disconnect():
    import network
    station = network.WLAN(network.STA_IF)
    station.disconnect()
    station.active(False)
    print("WiFi off!")








