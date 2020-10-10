import pygatt

'''
Gateway that responsible for:
    - Discovering nearby bracelets based on MAC address
    - Raise subprocesses when NEW bracelet is detected
    - Maintain the list of MAC addresses
    - Keep tracking MAC address and raised subprocesses
'''
class Gateway:

    def __init__(self, sub_proc):
        # maps mac address to pid of sub-process
        self._mac_proc_table = {}
    

    # validate if the given mac address is a bracelet
    # Arugments:
    #   - mac_addr: string, mac address
    # Return:
    #   - bool
    def _validate_mac_addr(self, mac_addr):
        pass

    # update self._mac_proc_table
    # arguments:
    #   - mac_addrs: a list of dictionaries with format: {'address': xxx.
    #   'name':}
    # return:
    #   - None
    def update_mac_table(self, mac_addrs):
        mac_addr_list = [i['address'] for i in mac_addrs]
        # remove old bracelets
        for mac_addr in self._mac_proc_table.keys():
            if mac_addr not in mac_addr_list:
                # kill the process
                pass

        # add new bracelet 
        for mac_addr in mac_addrs:
            valid_addr = self._validate_mac_addr(mac_addr)
            # new bracelet that haven't been detected yet.
            if valid_addr and mac_addr not in self._mac_proc_table.keys():
                # raise a sub-process to receive the bluetooth data
                pass
    
    # Print and return the list of mac address of connected devices
    # Arguments:
    #   - None
    # Return:
    #   - list
    def getConnectedDevice(self):
        for addr in self._mac_proc_table.keys():
            print(addr)
        return self._mac_proc_table.keys()

