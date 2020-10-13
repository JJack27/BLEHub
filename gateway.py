import pygatt

'''
Gateway that responsible for:
    - Discovering nearby bracelets based on MAC address
    - Raise subprocesses when NEW bracelet is detected
    - Maintain the list of MAC addresses
    - Keep tracking MAC address and raised subprocesses
'''
class Gateway:
    # Constructor of the Gateway
    # Arguments:
    #   - sub_proc: the subprocess to raise when new devices connected
    # Return:
    #   - Gateway
    def __init__(self, sub_proc, debug=False):
        # maps mac address to pid of sub-process
        # with the format: {mac_address: pid}
        self._mac_proc_table = {}

        # Scanner for discovering devices
        self._scanner = pygatt.GATTollBackend()
        
        # the sub-process function to raise when new deveice connected 
        self._sub_proc = sub_proc

        self._debug = debug

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
    def _update_mac_table(self, mac_addrs):
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
        if(self._debug):
            for addr in self._mac_proc_table.keys():
                print(addr)
        return self._mac_proc_table.keys()
    
    # Print and return the self._mac_proc_table
    # Arguments:
    #   - None
    # Return:
    #   - Dict
    def getMacProTable(self):
        if(self._debug):
            for addr, pid in self._mac_proc_table.items():
                print("%s %s"%(addr, pid))
        return self._mac_proc_table


    # Scanning and return all nearby devices
    # Arguments:
    #   - None
    # Returns:
    #   - List<dictionary>
    def scan(self):
        return self._scanner.scan()


    # The interface to start running the gateway
    # - Constantly discover the new devices
    # - update the self.mac_proc_table
    def run(self):
        while True:
            devices = self.scan()
            self._update_mac_table(self, devices)
