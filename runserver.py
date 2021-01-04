'''
The script to run the BLE hub.
The BLE hub will act as a BLE client. Listening to GATT broadcasts.
@author: yizhou
@date: 2020/11/23 12:18
@last-update: 2020/11/27 12:16
'''
from gateway import Gateway
from sub_process import sub_proc

def main(*args):
    print("Starting Gateway...")
    gateway = Gateway(sub_proc, debug=False)
    gateway.run()
    
if __name__ == '__main__':
    main()
