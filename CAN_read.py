import socket
import threading
import time
from .oncar import bus


# initial socket server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('0.0.0.0', 8080))
s.listen(5)


def tcplink(sock, addr):
    can1 = bus.CAN()
    switch = 0
    last = time.time()
    # to collect all state data, read for a while
    while time.time() - last < 0.2:
        id, data = can1.decode()
        can1.read(id, data)
        switch = 1
    if switch:
        sock.send(str(can1.state).encode('utf-8'))
    sock.close()
    can1.bus.shutdown()


while True:
    # 接受一个新连接:
    sock, addr = s.accept()
    # 创建新线程来处理TCP连接:
    t = threading.Thread(target=tcplink, args=(sock, addr))
    t.start()
