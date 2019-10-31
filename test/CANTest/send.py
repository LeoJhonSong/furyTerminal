import os
import can


# os.system('sudo ip link set can0 type can bitrate 250000')
# os.system('sudo ifconfig can0 up')

can0 = can.interface.Bus(channel='can0', bustype='socketcan_ctypes')  # socketcan_native

msg = can.Message(arbitration_id=0x123, data=[13, 1, 4, 1, 5, 9, 2, 6], extended_id=False)
can0.send(msg)

# os.system('sudo ifconfig can0 down')
