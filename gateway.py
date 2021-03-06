'''
Gateway that responsible for:
    - Discovering nearby bracelets based on MAC address
    - Raise subprocesses when NEW bracelet is detected
    - Maintain the list of MAC addresses
    - Keep tracking MAC address and raised subprocesses
'''

import pygatt
import bluepy.btle as btle
import os
import psutil
import time

class Gateway:
    # Constructor of the Gateway
    # Arguments:
    #   - sub_proc: the subprocess to raise when new devices connected
    #   - between_scan: integer, the number of seconds that main process pauses before the next scan
    # Return:
    #   - Gateway
    def __init__(self, sub_proc, between_scan=5, debug=False):
        # maps mac address to pid of sub-process
        # with the format: {mac_address: pid}
        self._mac_proc_table = {}

        # Scanner for discovering devices
        self._scanner = pygatt.GATTToolBackend()
        self._scanner.reset()     

        # the sub-process function to raise when new deveice connected 
        self._sub_proc = sub_proc

        self._debug = debug
        self._between_scan = between_scan
        self._total_rounds = 0
        self._broke_rounds = 0
    # validate if the given mac address is a bracelet
    # Arugments:
    #   - mac_addr: string, mac address
    # Return:
    #   - bool
    def _validate_mac_addr(self, mac_addr):
        test_mac_addr = ['66:55:44:33:22:11']
        if ( mac_addr.lower() in test_mac_addr):
            print("Found!")
            return True

    # update self._mac_proc_table
    # arguments:
    #   - mac_addrs: a list of dictionaries with format: {'address': xxx.
    #   'name':}
    # return:
    #   - None
    def _update_mac_table(self, mac_addrs):
        self._total_rounds += 1

        mac_addr_list = [i['address'] for i in mac_addrs]
        # remove and kill the process when the corresponding bracelet is not detected
        removing = []
        for mac_addr, pid in self._mac_proc_table.items():
            # Check if given process is a zombie process
            # print(psutil.Process(pid).status() == psutil.STATUS_ZOMBIE)
            if(psutil.Process(pid).status() == psutil.STATUS_ZOMBIE):
                
                os.waitpid(pid, 0)
                removing.append(mac_addr)
                if(self._debug):
                    print("Process (%s) is killed!"%pid)
        if(len(removing) > 0):
            self._broke_rounds += 1

        if(self._debug):
            print("Round %d, %s. (%d/%d, %f)" %
            (self._total_rounds, str(bool(len(removing))), 
            self._total_rounds, self._broke_rounds,
            self._total_rounds / self._broke_rounds))
        
        for addr in removing:
            self._mac_proc_table.pop(addr)
        
       
        # add new bracelet 
        for mac_addr in mac_addr_list:
            valid_addr = self._validate_mac_addr(mac_addr)
            # new bracelet that haven't been detected yet.
            if valid_addr and mac_addr not in self._mac_proc_table.keys():
                # raise a sub-process to receive the bluetooth data
                pid = os.fork()
                
                if(pid == 0):
                    # in sub-process
                    self._sub_proc(mac_addr)
                else:
                    # in parent process
                    # update self._mac_proc_table
                    self._mac_proc_table[mac_addr] = pid
        
        
        # Sleep for X seconds, then continue scanning. Default = 10
        time.sleep(self._between_scan)
                    
    # Print and return the list of mac address of connected devices
    # Arguments:
    #   - None
    # Return:
    #   - list
    def get_connected_device(self):
        if(self._debug):
            for addr in self._mac_proc_table.keys():
                print(addr)
        return self._mac_proc_table.keys()
    
    # Print and return the self._mac_proc_table
    # Arguments:
    #   - None
    # Return:
    #   - Dict
    def get_mac_proc_table(self):
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
        print("Scanning...")
        return self._scanner.scan()
    

    # The interface to start running the gateway
    # - Constantly discover the new devices
    # - update the self.mac_proc_table
    def run(self):
        self._scanner.start()
        while True:
            if(self._debug):
                print("=============")
                self.get_mac_proc_table()
            if(self._mac_proc_table == {}):
                devices = self.scan()
                self._update_mac_table(devices)
            if(self._debug):
                print("found %d devices" % len(devices))
            
            #self._update_mac_table(devices)
