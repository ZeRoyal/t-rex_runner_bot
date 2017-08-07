import cv2
import numpy as np
from PIL import ImageGrab
import time
from grab_scr import grab_screen
from press_keys import PressKey, ReleaseKey, Up, Down,Left, Right

template = [cv2.imread('rex.png',0),cv2.imread('rex_duck.png',0),
            cv2.imread('c1_b.png',0), cv2.imread('c1_s.png',0), 
            cv2.imread('bird_up.png',0), cv2.imread('bird_down.png',0)]

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
    return None    

def merge(a, e):
    r = list(a[0])
    for a1, a2 in zip(a[:-1], a[1:]):
        if a2[0] - a1[0] < e:
            r[2] = a2[0] - r[0] + a2[2]
        else:
            break
    return r

def main(macro = template, threshold= 0.6):
    last_time = time.time()
    w1, h1 = template[0].shape[::-1]
    w2, h2 = template[1].shape[::-1]
    w3, h3 = template[2].shape[::-1] 
    w4, h4 = template[3].shape[::-1] 
    w5, h5 = template[4].shape[::-1]    
    w6, h6 = template[5].shape[::-1]
    
    x_prev = None
    nframes = 0
    x0 = 100
    front = 80
    
    while(True):
        #screen = grab_screen(region=(300,350,650,540))
        screen = grab_screen(region=(300,450,750,550))
        screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
        
        im_gray = cv2.GaussianBlur(screen, (5, 5), 0)
        _, im_th = cv2.threshold(im_gray, 90, 255, cv2.THRESH_BINARY_INV)
        _, ctrs, _ = cv2.findContours(im_th.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        rects = [cv2.boundingRect(ctr) for ctr in ctrs]

        rects = list(filter(lambda x: x[0] > front, rects))
        rects.sort(key=lambda x: x[0])
        
        res = [cv2.matchTemplate(screen,t,cv2.TM_CCOEFF_NORMED) for t in template]
        loc = [np.where(r >= threshold) for r in res]
        
        points = []
        for l in loc[2:]:
            points += zip(*l)
        
        nframes += 1
        
        try:
            position = loc[0][1][0]
            i, closest = argmin(points)
            x = rects[0][0]
            if x_prev is None:
                x_prev = x
            else:
                dist = x_prev - x
                if dist < 0:
                    nframes = 0
                    x_prev = x
                elif dist > x0:
                    v = dist / nframes
                    nframes = 0
                    x_prev = x
                    print('current speed', v)
            
            obj = object_type(i, map(lambda x: x[0], loc[2:]))
            d = closest[1] - position
            if obj == 2 or obj == 3:
                k = 50.0 / 120.0
                r = 130 + (time.time() - last_time) * k
                if d < r:
                    yd = loc[0][0][0]
                    yb = closest[0]
                    h = (yd + h1) - (yb + h5)
                    if h+5 < h2:
                        PressKey(Up)
                    elif h-10 < h1:
                        PressKey(Down)
                        time.sleep(0.3)
                        ReleaseKey(Down)
            else:
                k = 50.0 / 120.0
                r = 177 + (time.time() - last_time) * k
                if d < r:
                    PressKey(Up)                   
        except:
            pass

        if len(rects) > 0:
            rect = merge(rects, 50)
            cv2.rectangle(screen, (rect[0], rect[1]), (rect[0] + rect[2], rect[1] + rect[3]), (0, 255, 0), 3)
        
        if x_prev is not None:
            cv2.rectangle(screen, (x, 0), (x_prev, 100), (0, 255, 0), 3)
        
        cv2.imshow('xxx', screen)

        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
        
main()