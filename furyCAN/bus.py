import os
import can
import time
import datetime

can.rc['interface'] = 'socketcan'
can.rc['channel'] = 'can0'
can.rc['bitrate'] = 250000  # 250k bits/s

idList = [
    0x203,  # 安全回路状态, 油门深度, 刹车深度, 控制状态标志, 给定转矩
    0x186040f3,  # 电压, 电流, SoC
    0x186240f3,  # 电池最高温度
    0x180,  # 转角, 转速, 有效位
    0x204,  # 姿态信息
    0x186140f3,  # 电池单体状态
    0x186340f4,  # 继电器状态, 充电状态信息  # FIXME: change to from VCU
]
# a list of read function name string
readSwitch = {
    hex(idList[i]): 'read_' + str(hex(idList[i])) for i in range(len(idList))
}
idMask = 0x1FFFFFFF
# big-endian (low bit first)
allFlagContent = [
    'acReliableFlag',
    'acBrReliableFlag',
    'startFlag',
    'runFlag',
    'driveReadyFlag',
    'SafetyFlag',
    'brFlag',
    'zfAllowFlag',
    'ycAllowFlag'
]

mcMessageContent = [
    'mcReady',
    'ycReady',
    'resolverFlag',
    'currentOverloadFlag',
    'voltageOverloadFlag',
    'ctlPointFlag',
    'voltageUnderloadFlag',
    'powerLimitFlag',
    'mcTempFlag',
    'motorTempFlag'
]


class CAN(object):
    """
    fury CAN Bus
    """

    def __init__(self):
        while True:
            os.system('sudo ip link set ' + can.rc['channel'] + ' type can bitrate ' + str(can.rc['bitrate']))
            os.system('sudo ifconfig ' + can.rc['channel'] + ' up')
            try:
                # turn on the network or will get bug: Network down
                self.bus = can.interface.Bus()
            except OSError:
                # wait for 5s and try again
                os.system('date')
                time.sleep(5)
            else:
                break
        self.bus.set_filters([{'can_id': item, 'can_mask': idMask} for item in idList])
        self.state = {}

    def kill(self):
        self.bus.shutdown()
        # turn down the network
        os.system('sudo ifconfig ' + can.rc['channel'] + ' down')

    def decode(self):
        """
        return the `arbitration id` and 8 item `decimal number list` of a CAN message

        `big-endian` (low bit first)
        """
        # wait indefinitely when no message
        msg = self.bus.recv()
        data = [int(str(bit)) for bit in msg.data]
        return hex(msg.arbitration_id), data  # hex() return a str

    def read(self, id, data):
        """
        switch to read function by `arbitration id`
        """
        if id in readSwitch.keys():
            eval('self.' + readSwitch[id])(data)

    def read_0x203(self, data):
        """
        0: vcuFlag

        when vcuFlag is 1:
            1: allFlag (H),
            2: allFlag (L),
            3: acFinal,
            4: brFinal,
            5: finalSendTorque (H),
            6: finalSendTorque (L),
            7: gear

        when vcuFlag is 2:
            1: rotateSpeed (H),
            2: rotateSpeed (L),
            3: mcMessage1,
            4: mcMessage2,
            5: mcuTemp,
            6: motorTemp,
            7: AIRFlag

        when vcuFlag is 3:
            1: dcMainVoltage (H),
            2: dcMainVoltage (L),
            3: dcMainCurrent (H),
            4: dcMainCurrent (L),
            5: acCurrent (H),
            6: acCurrent (L)

        allFlag:
            (H)
                7: ycAllowFlag,
            (L)
                0: zfAllowFlag
                1: brFlag,
                2: SafetyFlag,
                3: driveReadyFlag,
                4: runFlag,
                5: startFlag,
                6: acBrReliableFlag,
                7: acReliableFlag,
        """
        if data[0] == 1:
            # allFlag
            allFlag = bin(data[1] * 256 + data[2])[2:]
            # complete the bits if the binary number is shorter than allFlagContent
            # FIXME: check if works
            allFlag = allFlag[::-1] + '0' * (len(allFlagContent) - len(allFlag))
            for i in range(len(allFlagContent)):
                self.state[allFlagContent[i]] = allFlag[i]
            # TODO: maybe can be deleted
            # allFlagList = [int(item) for item in allFlag]
            # for i in range(16 - len(allFlag)):
            #     allFlagList.insert(0, 0)
            # allFlagList = allFlagList[::-1]
            # for i in range(len(allFlagContent)):
            #     self.state[allFlagContent[i]] = allFlagList[i]

            self.state['acFinal'] = data[3]
            self.state['brFinal'] = data[4]
            self.state['finalSendTorque'] = data[5] * 256 + data[6]  # ‰
            self.state['gear'] = data[7]
        elif data[0] == 2:
            self.state['rotateSpeed'] = (data[1] * 256 + data[2]) / 2 - 10000  # rpm
            # 0.0157 is a total argument
            self.state['speed'] = self.state['rotateSpeed'] * 0.0157  # km/h
            # mcMessages
            mcMessage = bin(data[3] * 256 + data[4])[2:]
            # complete the bits if the binary number is shorter than mcMessageContent
            # FIXME: check if works
            mcMessage = '0' * (len(mcMessageContent) - len(mcMessage)) + mcMessage
            for i in range(len(mcMessageContent)):
                self.state[mcMessageContent[i]] = mcMessage[i]

            self.state['mcuTemp'] = data[5] - 50  # ℃
            self.state['motorTemp'] = data[6] - 50  # ℃
            self.state['AIRFlag'] = data[7]
        elif data[0] == 3:
            self.state['dcMainVoltage'] = (data[1] * 256 + data[2]) / 10  # V
            self.state['dcMainCurrent'] = (data[3] * 256 + data[4]) / 10 - 1600  # A
            self.state['acCurrent'] = (data[5] * 256 + data[6]) / 10 - 1600  # A
            self.state['power'] = self.state['acCurrent'] * self.state['dcMainVoltage'] / 1000  # kW

    def read_0x186040f3(self, data):
        """
        电压, 电流, SoC

        0: batVoltage (H)
        1: batVoltage (L)
        2: batCurrent (H)
        3: batCurrent (L)
        4: batSoc
        """
        self.state['batVoltage'] = (data[0] * 256 + data[1]) / 10  # V
        self.state['batCurrent'] = (data[2] * 256 + data[3]) / 10 - 1000  # A
        self.state['batSoc'] = data[4]  # %

    def read_0x186240f3(self, data):
        """
        电池最高温度

        0: batMaxTemp
        """
        self.state['batMaxTemp'] = data[0] - 40  # ℃

    def read_0x180(self, data):
        """
        转角, 转速, 有效位
        """
        self.state['steeringWheelAngle'] = 0  # TODO: to be finished

    def read_0x204(self, data):
        """
        姿态信息
        """
        pass

    def read_0x186140f3(self, data):
        """
        电池单体状态

        0: batMaxCellVolt (H)
        1: batMaxCellVolt (L)
        """
        self.state['batMaxCellVolt'] = data[0] * 256 + data[1]  # mV

    def read_0x186340f4(self, data):
        """
        继电器状态, 充电状态信息
        """
        pass


if __name__ == "__main__":
    can1 = CAN()
    # last = datetime.datetime.now().microsecond
    while True:
        id, data = can1.decode()
        can1.read(id, data)
        # can1.state['time'] = datetime.datetime.now()
        # now = datetime.datetime.now().microsecond
        i = os.system('clear')
        # print(((now - last)**2)**0.5)
        # last = now
        for item in can1.state:
            print(str(item) + ': ' + str(can1.state[item]))
