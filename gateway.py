import pygatt

'''
Gateway that responsible for:
    - Discovering nearby bracelets based on MAC address
    - Raise subprocesses when NEW bracelet is detected
    - Maintain the list of MAC addresses
    - Keep tracking MAC address and raised subprocesses
'''
class Gateway:

    def __init__(self):
        # self._mac_addr = []
        
        # maps mac address to pid of sub-process
        self._mac_proc_table = {}

    def update_mac_table(self, mac_addrs):
        pass

     
