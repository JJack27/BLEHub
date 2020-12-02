'''
Gateway that responsible for:
    - Discovering nearby bracelets based on MAC address
    - Raise subprocesses when NEW bracelet is detected
    - Maintain the list of MAC addresses
    - Keep tracking MAC address and raised subprocesses
'''

import pygatt
import bluepy.btle as btle
import multiprocessing
import psutil
import time
from multiprocessing import Process, Event
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
        # self._scanner = pygatt.GATTToolBackend()
        # self._scanner.reset()     
        self._scanner = btle.Scanner()

        # the sub-process function to raise when new deveice connected 
        self._sub_proc = sub_proc

        self._debug = debug
        self._between_scan = between_scan

    # validate if the given mac address is a bracelet
    # Arugments:
    #   - mac_addr: string, mac address
    # Return:
    #   - bool
    def _validate_mac_addr(self, mac_addr):
        test_mac_addr = ['c7:36:e0:31:ab:ae']
        if (self._debug and mac_addr.lower() in test_mac_addr):
            return True

    # update self._mac_proc_table
    # arguments:
    #   - mac_addrs: a list of dictionaries with format: {'address': xxx.
    #   'name':}
    # return:
    #   - None
    def _update_mac_table(self, mac_addrs):
        mac_addr_list = [i['address'] for i in mac_addrs]
        # remove and kill the process when the corresponding bracelet is not detected
        removing = []
        for mac_addr, pid in self._mac_proc_table.items():
            # Check if given process is a zombie process
            '''
            # print(psutil.Process(pid).status() == psutil.STATUS_ZOMBIE)
            if(psutil.Process(pid).status() == psutil.STATUS_ZOMBIE):
                os.waitpid(pid, 0)
                removing.append(mac_addr)
                if(self._debug):
                    print("Process (%s) is killed!"%pid)
            '''
            if(not pid.is_alive()):
                pid.terminate()
                pid.join()
                removing.append(mac_addr)
                if(self._debug):
                    print("Process (%s) is killed!"%pid)
        for addr in removing:
            self._mac_proc_table.pop(addr)
        
       
        # add new bracelet 
        for mac_addr in mac_addr_list:
            valid_addr = self._validate_mac_addr(mac_addr)
            # new bracelet that haven't been detected yet.
            if valid_addr and mac_addr not in self._mac_proc_table.keys():
                # raise a sub-process to receive the bluetooth data
                proc = multiprocessing.Process(target=self._sub_proc, args=(mac_addr))
                self._mac_proc_table[mac_addr] = proc
                self._mac_proc_table[mac_addr].start()
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
        return self._scanner.scan(5.0)
    

    # The interface to start running the gateway
    # - Constantly discover the new devices
    # - update the self.mac_proc_table
    def run(self):
        self._scanner.start()
        while True:
            if(self._debug):
                print("=============")
                self.get_mac_proc_table()
            devices = self.scan()
            if(self._debug):
                print("found %d devices" % len(devices))
            
            self._update_mac_table(devices)
