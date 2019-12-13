import socket
import threading
import time
from .oncar import bus


# initial socket server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('0.0.0.0', 8080))
s.listen(5)

stateCache = {}


def tcplink(sock, addr):
    can1 = bus.CAN()
    # restore the state
    # stateCache need to be global or a mutable object should be passed to this
    # function, otherwise the value cannot be passed on
    global stateCache
    can1.state = stateCache
    # update the state
    id, data = can1.decode()
    can1.read(id, data)
    # send latest state to client and shutdown
    sock.send(str(can1.state).encode('utf-8'))
    sock.close()
    stateCache = can1.state
    can1.bus.shutdown()


while True:
    # 接受一个新连接:
    sock, addr = s.accept()
    # 创建新线程来处理TCP连接. 此处到底最新的请求得到的到底是不是最新的数据需要再确认一下.
    t = threading.Thread(target=tcplink, args=(sock, addr))
    t.start()
