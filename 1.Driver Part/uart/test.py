from com import COM
import time

def test():
    com = COM()
    send_data = "93 77 478 576\0"
    print(send_data)
    com.open()
    com.send(send_data)
    time.sleep(0.5)
    com.close()

def send():
    com = COM()
    while True:
        send_data = '111'
        print(send_data)
        com.open()
        com.send(send_data)
        time.sleep(0.5)
        com.close()

if __name__ == "__main__":
    # test()
    send()
