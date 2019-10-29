import os
import can


os.system('sudo ip link set can0 type can bitrate 500000')  # 500k bitrate
os.system('sudo ifconfig can0 up')

# socketcan_native
# can0 = can.interface.Bus(channel='can0', bustype='socketcan_ctypes')
can0 = can.interface.Bus(channel='can0', bustype='socketcan')

for msg in can0:
    msgdata = ','.join(str(i) for i in msg.data)
    print(msgdata)
    print("id is " + str(msg.arbitration_id))

    # DEBUG: send back
    # myId = 0x121
    # can0.send(can.Message(arbitration_id=myId, data=msg.data))

if msg is None:
    print('Timeout occurred, no message.')

os.system('sudo ifconfig can0 down')
