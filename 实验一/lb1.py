import cv2
import numpy as np
# 读取视频文件，如果是使用vscode那么此路径中的./代表项目根路径，即顶级目录
cap = cv2.VideoCapture("./实验二/ball.mp4")
# 检查视频是否成功打开
if not cap.isOpened():
    print("Error: 视频打开失败")
else:
    print("Video opened successfully.")
    while True:
        retval,img = cap.read()
        if retval:
            cv2.imshow("frame",img)
            hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
            lower_orange = np.array([6, 100, 100])
            upper_orange = np.array([20, 255, 255])
            mask = cv2.inRange(hsv, lower_orange, upper_orange)
            target = cv2.bitwise_and(img,img,mask=mask)
            cv2.imshow("target",target)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        else:
            print("读取帧序列失败")
            break
# 释放资源
cap.release()
cv2.destroyAllWindows()
