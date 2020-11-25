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
import pygatt

def sub_proc(mac_addr):
    adapter = pygatt.GATTToolBackend()

    print("Initialized subprocess (%s) with mac address: %s" %
            (os.getpid(), mac_addr))
    
    try:
        #adapter.start()
        print("Adapter for %s started!"%mac_addr)
    
        #device = adapter.connect(mac_addr)
        #print("Device (%s) is connected! Signal Strength = %d" % (mac_addr,
        #    device.get_rssi()))
    finally:
        adapter.stop()
        quit()


def main(*args):
    print("Starting Gateway...")
    gateway = Gateway(sub_proc, True)
    gateway.run()
    
if __name__ == '__main__':
    main()
