import serial
from serial.tools import list_ports
import time


class COM:
    def __init__(self, port):
        self.ser = serial.Serial()
        self.port = port
        self.pid_cp_data = None

    def open(self):
        self.ser.port = self.port  # 设置端口号
        self.ser.baudrate = 115200  # 设置波特率
        self.ser.bytesize = 8  # 设置数据位
        self.ser.stopbits = 1  # 设置停止位
        self.ser.parity = serial.PARITY_NONE  # 设置校验位
        self.ser.open()  # 打开串口,要找到对的串口号才会成功
        if self.ser.isOpen():
            print("串口打开成功")
        else:
            print("串口打开失败")

    def close(self):
        self.ser.close()
        if self.ser.isOpen():
            print("串口关闭失败")
        else:
            print("串口关闭成功")

    def send(self, data):
        if self.ser.isOpen():
            data = data.encode('utf-8')
            self.ser.write(data)
            # print("发送成功")
        else:
            # print("发送失败")
            return None

    def read(self):
        n = self.ser.inWaiting()
        if n == 0:
            return None
        data = self.ser.read(n)
        try:
            return str(data, 'utf-8')
        except UnicodeDecodeError:
            return None

    def readForThread(self):
        while True:
            receive_data = self.ser.readline().decode('utf-8')
            if receive_data is not None:
                if receive_data.find('central point') != -1:
                    self.pid_cp_data = receive_data
                else:
                    print(receive_data)
