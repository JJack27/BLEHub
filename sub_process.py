'''
Function run as a sub process
@author: yizhou
@date: 2020/11/27 12:55
@last-update: 2020/11/27 12:55
'''

import os
import struct
import bluepy.btle as btle
import time
# The sub-process to be raised after a new device is connected
def sub_proc(mac_addr, debug=False):
    
    print("Initializing subprocess (%s) with mac address: %s" % (os.getpid(), mac_addr))
    #try:
    if(True):
        peripheral = btle.Peripheral(mac_addr, btle.ADDR_TYPE_PUBLIC)
        
    
        print("Device (%s) connected! " % mac_addr)
         
        # TODO: Need to customize the service and characteristics
        service = peripheral.getServiceByUUID("49535343-fe7d-4ae5-8fa9-9fafd205e455")
        print(service)
        chara =    service.getCharacteristics("49535343-1e4d-4bd9-ba61-23c647249616")
        print(chara)
        with open("result.csv", "w") as f:
            while True:
                time.sleep(0.1)
                #print("%s = %f" %(mac_addr, struct.unpack('f', chara.read())[0]))
                print(struct.unpack('i', chara.read()))
                #f.writeline(str(chara.read()))
    #except Exception as e:
    #    print("Error from sub-process: ", end="")
    #    print(e)
    else:
        quit()
