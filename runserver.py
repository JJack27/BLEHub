'''
The script to run the BLE hub.
The BLE hub will act as a BLE client. Listening to GATT broadcasts.
@author: yizhou
@date: 2020/11/23 12:18
@last-update: 2020/11/23 12:18
'''
from gateway import Gateway

def sub_proc():
    print("sub_proceess function")

def main(*args):
    print("Starting Gateway...")
    gateway = Gateway(sub_proc, True)
    gateway.run()
    
if __name__ == '__main__':
    main()
