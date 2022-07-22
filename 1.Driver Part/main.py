import time
import threading
import cv2
from face_detector import FaceDetector
from uart import COM
from plot import DynamicPloter
from utils import parsePointInfo

ploter = DynamicPloter()
face_detector = FaceDetector()
cap = cv2.VideoCapture(0)
com = COM('COM13')
com.open()

ploter.init()

thrd = threading.Thread(target=com.readForThread)
thrd.setDaemon(True)
thrd.start()

while True:
    _, orig_image = cap.read()
    image = cv2.cvtColor(orig_image, cv2.COLOR_BGR2RGB)
    result = face_detector.getFaceCP(image)

    # 未检测到人脸
    if result is None:
        orig_image = cv2.resize(orig_image, None, None, fx=0.8, fy=0.8)
        cv2.imshow('face', orig_image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        continue

    # 检测到人脸
    cp, left, top, right, bottom = result

    cv2.rectangle(orig_image, (left, top), (right, bottom), (0, 255, 0), 4)
    cv2.circle(orig_image, cp, 5, (0, 255, 0), 10)


    # 合成待发送数据
    data = str(cp[0]) + '-' + str(cp[1]) + '.\r'

    # 串口发送
    com.send(data)

    # 绘图
    if com.pid_cp_data is not None:
        pid_cp = parsePointInfo(com.pid_cp_data)
        ploter.plot(pid_cp[0])

    # 显示
    orig_image = cv2.resize(orig_image, None, None, fx=0.8, fy=0.8)
    cv2.imshow('face', orig_image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    time.sleep(0.2)

cap.release()
cv2.destroyAllWindows()
com.close()