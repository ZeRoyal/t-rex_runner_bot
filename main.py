import cv2
import numpy as np
from PIL import ImageGrab
import time
from grab_scr import grab_screen
from press_keys import PressKey, ReleaseKey, Up, Down,Left, Right
import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Conv2D, MaxPooling2D
from skimage.feature import hog






num_classes = 10

modelx = Sequential()
modelx.add(Conv2D(32, kernel_size=(3, 3),
                 activation='relu',
                 input_shape=(28, 28, 1)))
modelx.add(Conv2D(64, (3, 3), activation='relu'))
modelx.add(MaxPooling2D(pool_size=(2, 2)))
modelx.add(Dropout(0.25))
modelx.add(Flatten())
modelx.add(Dense(128, activation='relu'))
modelx.add(Dropout(0.5))
modelx.add(Dense(num_classes, activation='softmax'))


modelx.load_weights('weights.h5')


template = [cv2.imread('rex.png',0),cv2.imread('rex_duck.png',0),
            cv2.imread('c1_b.png',0), cv2.imread('c1_s.png',0), 
            cv2.imread('bird_up.png',0), cv2.imread('bird_down.png',0)]
#template=cv2.resize(template,(35,90))

def argmin(f):
    idx, m = 0, f[0]
    for i, item in enumerate(f):
        if item < m:
            idx = i
            m = item
    return idx, m

def object_type(i, f):
    n = 0
    for j, item in enumerate(f):
        n += len(item)
        if i < n:
            return j
    raise ValueError
    #return None

def main(macro = template, threshold= 0.6):
    
    last_time = time.time()
    w1, h1 = template[0].shape[::-1]
    w2, h2 = template[1].shape[::-1]
    w3, h3 = template[2].shape[::-1] 
    w4, h4 = template[3].shape[::-1] 
    w5, h5 = template[4].shape[::-1]    
    w6, h6 = template[5].shape[::-1]
    
    for i in list(range(2))[::-1]:
        print(i+1)
        time.sleep(1)
        
    while(True):

        screen = grab_screen(region=(300,350,650,540))
        screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)


        im_gray = cv2.GaussianBlur(screen, (5, 5), 0)
        ret, im_th = cv2.threshold(im_gray, 90, 255, cv2.THRESH_BINARY_INV)
        

        im, ctrs, hier = cv2.findContours(im_th.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        rects = [cv2.boundingRect(ctr) for ctr in ctrs]        
        



        res = [cv2.matchTemplate(screen,t,cv2.TM_CCOEFF_NORMED) for t in template]
        loc = [np.where(r >= threshold) for r in res]
        
        points = []
        for l in loc[2:]:
            points += zip(*l)
        #for i in range(len(template[2:])):
        #    points += zip(*loc[i])
        
        try:
            position = loc[0][1][0]
            i, closest = argmin(points)
            obj = object_type(i, map(lambda x: x[0], loc[2:]))
            #print(obj)
            d = closest[1] - position
            if obj == 2 or obj == 3:
                #print('bird', d)
                if d < 130:
                    yd = loc[0][0][0]
                    yb = closest[0]
                    h = (yd + h1) - (yb + h5)
                    #print('bird height', h, h2)
                    if h+5 < h2:
                        PressKey(Up)
                    elif h-10 < h1:
                        PressKey(Down)
                        time.sleep(0.3)
                        ReleaseKey(Down)
            else:
                if d < 180 and time.time()-last_time < 30:
                    PressKey(Up)
                    
                elif d < 185 and time.time()-last_time < 60 and time.time()-last_time > 30:
                    PressKey(Up)

                elif d < 190 and time.time()-last_time > 60:
                    PressKey(Up)                    

        except:
            pass
        
        for t, l in zip(template,loc):
            w, h = t.shape[::-1]
            for pt in zip(*l[::-1]):
                cv2.rectangle(screen, pt, (pt[0] + w, pt[1] + h), (0,0,255), 1)
        


        for rect in rects:

            cv2.rectangle(screen, (rect[0], rect[1]), (rect[0] + rect[2], rect[1] + rect[3]), (0, 255, 0), 3) 

            leng = int(rect[3] * 1.6)
            pt1 = int(rect[1] + rect[3] // 2 - leng // 2)
            pt2 = int(rect[0] + rect[2] // 2 - leng // 2)
            roi = im_th[pt1:pt1+leng, pt2:pt2+leng]
            roi = cv2.resize(roi, (28, 28))

            nbr = list(np.around(modelx.predict([roi.reshape(-1,28,28,1)])[0]))
            print(nbr)

        




        cv2.imshow('xxx',screen)
        #moves = list(np.around(modelx.predict([screen.reshape(1,100,75,1)])[0]))

        

    

        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break       
      
main()