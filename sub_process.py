'''
Function run as a sub process
@author: yizhou
@date: 2020/11/27 12:55
@last-update: 2020/11/27 12:55
'''

import os
import struct
import bluepy.btle as btle

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