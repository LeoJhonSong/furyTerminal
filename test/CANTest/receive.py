import os
import can



os.system('sudo ip link set can0 type can bitrate 500000')
os.system('sudo ifconfig can0 up')

can0 = can.interface.Bus(channel = 'can0', bustype = 'socketcan_ctypes')# socketcan_native

#msg = can.Message(arbitration_id=0x123, data=[0, 1, 2, 3, 4, 5, 6, 7], extended_id=False)
##msg = can0.recv(10.0)
##print(msg)
i = 0x1
idd = 0x121
for msg in can0:
    print(msg.data)
    idd = idd + i
    i = i + 0x1
    
    msgs = can.Message(arbitration_id=idd, data=msg.data)
    can0.send(msgs)
    
if msg is  None:
    print('Timeout occurred, no message.')
##else:
##    msg = can.Message(arbitration_id=0x123, data=[3, 1, 4, 1, 5, 9, 2, 6], extended_id=False)
##    can0.send(msg)

os.system('sudo ifconfig can0 down')