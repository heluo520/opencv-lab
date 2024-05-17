import cv2
import numpy as np
for i in range(4):
    o = cv2.imread(f"./test3/lab3/{i}.jpg",1)
    img = cv2.resize(o,(0,0),fx=0.4,fy=0.4)
    cv2.imshow("img",img)
    hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    # cv2.imshow("hsv",hsv)
    lower_orange = np.array([90,30,50])
    upper_orange = np.array([135,255,255])
    # 获取棋子的掩膜
    mask = cv2.inRange(hsv,lower_orange,upper_orange)
    # cv2.imshow("mask",mask)
    # qizi = cv2.bitwise_and(img,img,mask=mask)
    # cv2.imshow("qizi",qizi)
    # 获取掩膜的轮廓
    contours,_ = cv2.findContours(mask,cv2.RETR_LIST,cv2.CHAIN_APPROX_NONE)
    # n = len(contours)
    # print(n)

    # 合并两个矩形轮廓的坐标形成一个大轮廓坐标，大矩形包围整个棋子
    # 获得生成矩形包围各个轮廓的矩形坐标与宽高
    x1,y1,w1,h1 = cv2.boundingRect(contours[0])
    x2,y2,w2,h2 = cv2.boundingRect(contours[1])
    x_max = max(x1,x2,x1+w1,x2+w2)
    x_min = min(x1,x2,x1+w1,x2+w2)
    y_max = max(y1,y2,y1+h1,y2+h2)
    y_min = min(y1,y2,y1+h1,y2+h2)
    brcnt = np.array([[[x_min,y_min]],[[x_max,y_min]],[[x_max,y_max]],[[x_min,y_max]]])
    # 画出大轮廓
    cv2.drawContours(img,[brcnt],-1,(0,0,0),2)
    cv2.imshow("result",img)
    cv2.waitKey(0)
cv2.destroyAllWindows()
