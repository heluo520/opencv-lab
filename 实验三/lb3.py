import cv2
import mediapipe as mp
import numpy as np
def get_str_hands(up_fingers):
    # 规则 up_fingers为在凸包外的点
    if len(up_fingers)==5 and up_fingers[0]==4 and up_fingers[1]==8 and up_fingers[2]==12 and up_fingers[3]==16 and up_fingers[4]==20:
        str_hands = "5"
    elif len(up_fingers)==4 and up_fingers[0]==8 and up_fingers[1]==12 and up_fingers[2]==16 and up_fingers[3]==20:
        str_hands = "4"
    elif len(up_fingers)==3 and up_fingers[0]==12 and up_fingers[1]==16 and up_fingers[2]==20:
        str_hands = "3"
    elif len(up_fingers)==2 and up_fingers[0]==8 and up_fingers[1]==12:
        str_hands = "2"
    elif len(up_fingers)==1 and up_fingers[0]==8:
        str_hands = "1"
    elif len(up_fingers)==0:
        str_hands = "0"
    else:
        str_hands = ""
    return str_hands

def do_main(image,mp_hands,mp_drawing):
    H, W, C = image.shape
    img_bgr = image.copy()
    img_RGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # 分析
    results = mp_hands.process(img_RGB)
    if results.multi_hand_landmarks is not None:
        # 第一个手部全部点的信息
        myHand = results.multi_hand_landmarks[0]
        # 画出点并实线连接
        mp_drawing.draw_landmarks(
            img_bgr,
            myHand,
            mp.solutions.hands.HAND_CONNECTIONS
        )
        # 采集全部关键点坐标
        list = []
        for i in range(21):
            x = myHand.landmark[i].x*W
            y = myHand.landmark[i].y*H
            list.append([int(x),int(y)])
        # 构造凸包点
        list = np.array(list,dtype=np.int32)
        index = [0,1,2,3,6,10,14,19,18,17,10]
        hull = cv2.convexHull(list[index,:])
        # 绘制凸包
        cv2.polylines(img_bgr,[hull],True,(0,255,0),2)
        # 查找外部的点数
        out_i = [4,8,12,16,20]
        up_fingers = [] #存储不在凸包中的点
        for i in out_i:
            pt = (int(list[i][0]),int(list[i][1]))
            # 判断out_i中的点是否在凸包中
            dist = cv2.pointPolygonTest(hull,pt,True)
            if dist < 0:
                up_fingers.append(i)
        # 获得对应的手势数字字符串形式
        str_hands = get_str_hands(up_fingers)
        print("手势为：",str_hands)
        # 输出数组字符到图片
        cv2.putText(img_bgr,' %s'%(str_hands),(90,90),cv2.FONT_HERSHEY_SIMPLEX,3,(0,0,255),4,cv2.LINE_AA)
        # 用黄色标出在凸包外面的点
        for i in out_i:
            x_out = myHand.landmark[i].x*W
            y_out = myHand.landmark[i].y*H
            cv2.circle(img_bgr,(int(x_out),int(y_out)),3,(0,255,255),-1)
        cv2.imshow("hands",img_bgr)
        cv2.waitKey(0)


if __name__=="__main__":
    # 绘图工具
    mp_drawing = mp.solutions.drawing_utils
    # 手对象
    mp_hands = mp.solutions.hands.Hands(
        static_image_mode=True,
        max_num_hands=1,
        min_detection_confidence=0.5)
    for i in range(4):
        image = cv2.imread(f"./test4/hand{i+1}.png")
        do_main(image,mp_hands,mp_drawing)


    # 自己画点
    # cv2.imwrite('6_hands.png',img_bgr)
    # for id, lm in enumerate(myHand.landmark):
    #     cx, cy = int(lm.x * W), int(lm.y * H)
    #     cv2.circle(img=img_bgr, center=(cx, cy), radius=4, color=(0,0,255), thickness=-1)
    # cv2.imwrite("5_detected.png", img_bgr)
