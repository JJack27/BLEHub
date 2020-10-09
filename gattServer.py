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
    except:
        adapter.stop()
    finally:
        adapter.stop()

def main():
    # find all devices that are matching with mac address pattern
    adapterScan = pygatt.GATTToolBackend()
    print(adapterScan.scan())

main()
