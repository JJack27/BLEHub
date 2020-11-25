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
#import pygatt Deprecated
import bluepy.btle as btle

'''
class MyDelegate(btle.DefaultDelegate):
    def __init__(self):
        btle.DefaultDelegate.__init__(self)
'''
    

def sub_proc(mac_addr):

    print("Initialized subprocess (%s) with mac address: %s" %
            (os.getpid(), mac_addr))
    
    try:
        #adapter.start()
        peripheral = btle.Peripheral(mac_addr, btle.ADDR_TYPE_RANDOM)
        
        print("Adapter for %s started!"%mac_addr)
        
        service = peripheral.getServiceByUUID('401dc6f0-3f8d-11e5-afbb-0002a5d5c51b')
        chara = service.getCharacteristics('401dc6f1-3f8d-11e5-afbb-0002a5d5c51b')[0]
        
        while True:
            #print("%s = %f" %(mac_addr, struct.unpack('f', chara.read())))
            print(struct.unpack('f', chara.read()))
            #device = adapter.connect(mac_addr)
        #print("Device (%s) is connected! Signal Strength = %d" % (mac_addr,
        #    device.get_rssi()))
    except Exception as e:
        print("Error from sub-process: ", end="")
        print(e)
    finally:
        #adapter.stop()
        quit()


def main(*args):
    print("Starting Gateway...")
    gateway = Gateway(sub_proc, True)
    gateway.run()
    
if __name__ == '__main__':
    main()
