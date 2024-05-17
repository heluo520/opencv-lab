import cv2
import numpy as np
cap = cv2.VideoCapture('./homework/coin.mp4')
if not cap.isOpened():
    print("读取视频失败")
else:
    while True:
        retval,o = cap.read()
        if not retval:
            print("读取图像失败")
            break
        else:
            img = cv2.resize(o,(0,0),fx=0.5,fy=0.5)
            cv2.imshow("o",img)
            # 高斯降噪
            img = cv2.GaussianBlur(img,(5,5),0,0)
            hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
            lower_orange = np.array([0,0,170])
            upper_orange = np.array([180,255,255])
            mask = cv2.inRange(hsv,lower_orange,upper_orange)
            contours,_ = cv2.findContours(mask,cv2.RETR_LIST,cv2.CHAIN_APPROX_NONE)
            cv2.drawContours(img,contours,-1,(0,0,255),2)
            # 统计圆个数
            num = 0
            # 遍历轮廓判断是否符合圆形，为了减小其它影响
            for i in range(len(contours)):
                # 获取最小拟合的圆的圆心
                center, radius = cv2.minEnclosingCircle(contours[i])
                # 计算面积与周长
                area = cv2.contourArea(contours[i])
                perimeter = cv2.arcLength(contours[i], True)
                # 去除不符合的
                if area==0 or perimeter==0:
                    continue
                # 判断是否是圆形
                circularity = 4 * np.pi * area / (perimeter ** 2)
                if circularity > 0.88:
                    # 是圆则标出序号
                    num = num+1
                    cv2.putText(img,f'#{num}',(int(center[0]),int(center[1])),cv2.FONT_HERSHEY_SIMPLEX,2,(0,255,0),3)
            cv2.imshow("res",img)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
cap.release()
cv2.destroyAllWindows()
