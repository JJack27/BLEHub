import pygatt

def connectDevice(macAddr):
    adapter = pygatt.GATTToolBackend()
    try:
        adapter.start()
        device = adapter.connect('5C:17:CF:0E:D0:74')
        
        print("device connected")
        while True:
            # should receiving data
            pass
    finally:
        adapter.stop()

def main():
    # find all devices that are matching with mac address pattern
    adapterScan = pygatt.GATTToolBackend()
    devices = adapterScan.scan()
    for device in devices:
        print(device)
main()
