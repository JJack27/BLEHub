import pygatt
import struct
adapter = pygatt.GATTToolBackend()

def print_data(handle, value):
    print("Received data: %s" % struct.unpack('f', value)[0])


try:
    adapter.start()
    device = adapter.connect('c7:36:e0:31:ab:ae',
            address_type=pygatt.BLEAddressType.random)
    print(device)

    #device.subscribe('401dc6f1-3f8d-11e5-afbb-0002a5d5c51b', callback=print_data)
    while True:
        value = device.char_read('401dc6f1-3f8d-11e5-afbb-0002a5d5c51b')
        print(struct.unpack('f', value)[0])
finally:
    adapter.stop()

                    
