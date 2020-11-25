import bluepy.btle as btle
import struct


class MyDelegate(btle.DefaultDelegate):
    def __init__(self):
        btle.DefaultDelegate.__init__(self)

    def handleNotification(self, cHandle, data):
        print(struct.unpack('f', data))

print("Connecting to device...")
p = btle.Peripheral('c7:36:e0:31:ab:ae', btle.ADDR_TYPE_RANDOM)
print("connected!")

p.setDelegate(MyDelegate())

svc = p.getServiceByUUID('401dc6f0-3f8d-11e5-afbb-0002a5d5c51b')
ch = svc.getCharacteristics('401dc6f1-3f8d-11e5-afbb-0002a5d5c51b')[0]
print("characteristics")

while True:
    #if p.waitForNotifications(5.0):
    #    print("got it~!")
    #    continue
    #print("waiting")
    print(ch.read())
