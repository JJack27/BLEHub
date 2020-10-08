import pygatt

adapter = pygatt.GATTToolBackend()

try:
    adapter.start()
    device = adapter.connect('5C:17:CF:0E:D0:74')
    
    print("device connected")
    while True:
        pass
except:
    adapter.stop()
finally:
    adapter.stop()
