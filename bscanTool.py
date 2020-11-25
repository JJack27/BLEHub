from bluepy.btle import Scanner, DefaultDelegate

scanner = Scanner()

devices = scanner.scan(10)
for dev in devices:
    print("Devices %s (%s)" %(dev.addr, dev.addrType))
    for (adtype, desc, value) in dev.getScanData():
        print("%s = %s" %(desc, value))
