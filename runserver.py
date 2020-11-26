'''
The script to run the BLE hub.
The BLE hub will act as a BLE client. Listening to GATT broadcasts.
@author: yizhou
@date: 2020/11/23 12:18
@last-update: 2020/11/23 12:18
'''
from gateway import Gateway
import os
import sys
import struct
import bluepy.btle as btle

'''
class MyDelegate(btle.DefaultDelegate):
    def __init__(self):
        btle.DefaultDelegate.__init__(self)
'''
    
# The sub-process to be raised after a new device is connected
def sub_proc(mac_addr, debug=False):
    if(debug):
        print("Initializing subprocess (%s) with mac address: %s" % (os.getpid(), mac_addr))
    try:
        peripheral = btle.Peripheral(mac_addr, btle.ADDR_TYPE_RANDOM)
        
        if(debug):
            print("Device (mac_addr) connected! " % mac_addr)
        
        # TODO: Need to customize the service and characteristics
        service = peripheral.getServiceByUUID('401dc6f0-3f8d-11e5-afbb-0002a5d5c51b')
        chara = service.getCharacteristics('401dc6f1-3f8d-11e5-afbb-0002a5d5c51b')[0]
        
        while True:

            print("%s = %f" %(mac_addr, struct.unpack('f', chara.read())[0]))
            

    except Exception as e:
        print("Error from sub-process: ", end="")
        print(e)
    finally:
        quit()


def main(*args):
    print("Starting Gateway...")
    gateway = Gateway(sub_proc, True)
    gateway.run()
    
if __name__ == '__main__':
    main()
