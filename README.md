# ESP32-433Mhz-Receiver-and-Tools  

ESP32 433Mhz Receiver written in micropython and Tools for Windows  
  
I used a ESP32 development board and a SRX882 receiver. Any other will be good.  
There are lots of tutorial to connect it to the board. 
  
This is not only a simple receiving program.  
**It transmit the results to UDP socket or to OpenHab.**   

Here you can develop and implement your own decoder.
You can configure the decoder output to a user friendly name or OpenHab Item  
Config for SSID, Password, UDP socket IP and OpenHab URL
  
**Install:**  
Copy the files rx433_ESP.py wifi.py and rx433_config.py to ESP32
Make a directory rx433_decoder and copy the decoder files.

## Windows Tools 
connect the ESP32 via USB and be sure to enable Debug=on in the config file!  

**ESP_Config_Editor**

Loads the config file via USB from ESP32. You can edit and save it back.

**ESP32_Sniffer**

The tool received the 433Mhz results via USB and show the raw data and the decoded data  
You get a list of devices and address in your surrounding, thats usefull to create  
the config file.


