import sys

import cv2
import math
import numpy as np
from PyQt5.QtWidgets import QApplication
import main_window

###################################################
def Wrap_Image(img, wrap_line, img_line):
    global map_x, map_y
    
    map_x = np.zeros((height, width), dtype=np.float32)
    map_y = np.zeros((height, width), dtype=np.float32)
    

    src_wrap = np.zeros((height, width, channels), dtype=np.uint8)

    for i in range(height):
        for j in range(width):
            
            
            weightsum = 0.0
            u, v, weight = 0, 0, 0
            psu = [0, 0]
            for index in range(len(wrap_line)):
                X = [i, j]

                X_P = np.array(X)-np.array(wrap_line[index].start_point)

                Q_P = wrap_line[index].vector

                u = np.dot(X_P, Q_P)/wrap_line[index].square_length

                V_Q_P = wrap_line[index].perpendicular

                v = np.dot(X_P, V_Q_P)/wrap_line[index].length

                img_Q_P = img_line[index].vector

                V_img_Q_P = img_line[index].perpendicular

                X_new = np.array(img_line[index].start_point)+np.array(u)*np.array(img_Q_P)+np.array(v)*np.array(V_img_Q_P)/img_line[index].length
                if u<0:
                    dist = np.sqrt(np.sum(np.square(X_new - np.array(img_line[index].start_point))))
                elif u>1:
                    dist = np.sqrt(np.sum(np.square(X_new - np.array(img_line[index].end_point))))
                else:
                    dist = abs(v)

                weight = math.pow(math.pow(wrap_line[index].length, 0)/(1+dist), 2)
                psu = np.array(psu) + np.array(X_new)*weight
                weightsum = weightsum + weight
            map_x[i, j] = ((np.array(psu)/weightsum)[0])
            map_y[i, j] = ((np.array(psu)/weightsum)[1])
            if map_x[i, j] < 0:
                map_x[i, j] = 0
            elif map_x[i, j] >= height:
                map_x[i, j] = height-1
            if map_y[i, j] < 0:
                map_y[i, j] = 0
            elif map_y[i, j] >= width:
                map_y[i, j] = width-1
            src_wrap[i, j, :] = img[math.floor(map_x[i, j]), math.floor(map_y[i, j]), :]
                
    return src_wrap

#################################################


class Line(object):
    def __init__(self, start_point, end_point):
        self.start_point = start_point 
        self.end_point = end_point
        self.vector = end_point - start_point
        self.perpendicular = np.array([self.vector[1], -self.vector[0]])
        self.square_length = np.sum(np.square(self.vector))
        self.length = math.hypot(self.vector[0], self.vector[1])

####################################################################
def Draw_Feature_Line(event, x, y, flags, param):
    img = param[1]
    point = param[2]
    line = param[3]
    if event == cv2.EVENT_LBUTTONDOWN:
        point.append(np.array([y, x]))
        if len(point)%2==0:
            cv2.arrowedLine(img, (point[-2][1], point[-2][0]), (x, y), (255, 255, 255), 2)
            line.append(Line(point[-2], np.array([y, x])))
            cv2.imshow(param[0], img)


###################################################
def Call_Wrap_Image():
    print('please wait, warping...')
    wrap_img1 = Wrap_Image(img1, wrap_line, src_line)
    cv2.imshow("a1", wrap_img1)
    wrap_img2 = Wrap_Image(img2, wrap_line, dst_line)
    cv2.imshow("a2", wrap_img2)
    tt = np.zeros((height, width, channels), dtype=np.uint8)
    for i in range(height):
        for j in range(width):
            tt[i, j, :] = (1-alpha)*wrap_img1[i, j, :]+alpha*wrap_img2[i, j, :]
    cv2.imshow("a3", tt)

#######################################################
def Wrap_Feature_Line():
    global wrap_point, wrap_line
    wrap_point, wrap_line = [], []

    if (len(src_line)!=0) and (len(src_line)==len(dst_line)):
        for index in range(len(src_line)):
            wrap_start = src_line[index].start_point*(1-alpha) + dst_line[index].start_point*alpha
            wrap_end = src_line[index].end_point*(1-alpha) + dst_line[index].end_point*alpha
            wrap_point.append(np.array(wrap_start))
            wrap_point.append(np.array(wrap_end))
            wrap_line.append(Line(wrap_start, wrap_end))
    else:
        print("error")

##########################################



###########################################################
def Animation():
    global alpha, animation
    print('please wait, creating video...')
    if len(animation) != 50:
        animation = []
        for index in range(50):
            print(index)
            alpha = 0.02*(index+1)
            Wrap_Feature_Line()
            wrap_img1 = Wrap_Image(img1, wrap_line, src_line)
            wrap_img2 = Wrap_Image(img2, wrap_line, dst_line)
            tt = np.zeros((height, width, channels), dtype=np.uint8)
            for i in range(height):
                for j in range(width):
                    tt[i, j, :] = (1-alpha)*wrap_img1[i, j, :]+alpha*wrap_img2[i, j, :]
            animation.append(tt)
    

    out=cv2.VideoWriter('myvideo.avi',cv2.VideoWriter_fourcc(*'mp4v'), 1, (width, height))

    for i in range(len(animation)):
        out.write(animation[i])

    out.release()

##############################################################



def main():
    
    app = QApplication(sys.argv)
    window = main_window.MainWindow()

    global img1, img2, height, width, channels, im_dst, im_wrap
    
    img1 = cv2.imread('./image/youngEW.jpg')#
    img2 = cv2.imread('./image/oldEW.jpg')#
    height, width, channels = img1.shape
    
    im_wrap = np.zeros((height, width, channels), dtype=np.uint8)
    
    param = ["Source Image", img1.copy(), src_point, src_line]
    cv2.namedWindow("Source Image")
    cv2.setMouseCallback("Source Image", Draw_Feature_Line, param=param)
    cv2.imshow("Source Image", img1)
    
    param = ["Destination Image", img2.copy(), dst_point, dst_line]
    cv2.namedWindow("Destination Image")
    cv2.setMouseCallback("Destination Image", Draw_Feature_Line, param=param)
    cv2.imshow("Destination Image", img2)
    
    window.WrapFeatureLine.clicked.connect(Wrap_Feature_Line)
    window.WrapImage.clicked.connect(Call_Wrap_Image)
    window.Animation.clicked.connect(Animation)
    
    window.show()
    return app.exec_()

src_point, src_line = [], []
dst_point, dst_line = [], []
wrap_point, wrap_line = [], []
map_x, map_y = [], []
img1, img2 = [], []
im_temp = []
im_wrap = []
animation = []
alpha = 0.5
height, width, channels = 0, 0, 0

if __name__ == '__main__':
    main()
