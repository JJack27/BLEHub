'''
Base class abstracts a sub-process
- Connecting to the peripherals
- Connecting to the given service
- Connecting to the given characteristics
- Receiving the data from peripherals
- Holds running status of the sub-process
- You will NEED to override the self._sub_proc in order to make it work
@author: yizhou
@date: 2020/11/27 12:19
@last-update: 2020/11/27 12:19
'''
from gateway import Gateway
import os
import sys
import struct
import bluepy.btle as btle

# status of the sub process
INIT=0
RUNNING=1
ZOMBIE=2
TERMINATED=3

class BaseSubprocess:
    
    '''
    Constructor.
    Arguments:
    - mac_addr: string. The MAC address of peripherals
    - service_characteristics: dict. The UUID of service and characteristics that
      is waiting to be connected. It is in a format of: {service_id: [char1, char2, ...]}
    Throws:
    - TypeError: if arguments are not the type required
    '''
    def __init__(self, mac_addr: str, service_characteristics: dict):
        # verify the type of mac_addr
        if(mac_addr == None or type(mac_addr) != type("")):
            raise TypeError("mac_addr should be a string, get %s"%type(mac_addr))

        # verify the type of service_characteristics
        if(service_characteristics == None or type(service_characteristics) != type(service_characteristics)):
            raise TypeError("service_characteristics should be a dict, get %s" % type(service_characteristics))
        
        self._status = INIT
        self._mac_addr = mac_addr
        self._service_char = service_characteristics
        self._pid = -1


    '''
    Abstract method needs to be override.
    - mac_addr: string. The MAC address of peripherals
    - service_characteristics: dict. The UUID of service and characteristics that
      is waiting to be connected. It is in a format of: {service_id: [char1, char2, ...]}
    Throws:
    - NotImpelmentedError: when the derived class doesn't override this method
    '''
    def _sub_proc(self, mac_addr, service_char):
        raise NotImplementedError("You need to override this function to work.")

    '''
    A public interface for outer code to start the sub-process
    '''
    def run(self):
        self._status = RUNNING
        self._sub_proc(self._mac_addr, self._service_char)
