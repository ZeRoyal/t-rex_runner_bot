import cv2
import numpy as np
from PIL import ImageGrab
import time
from grab_scr import grab_screen
from press_keys import PressKey, ReleaseKey, Up, Down,Left, Right
from keys_util import key_check

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
    #jump_time = 0.56s
    #jump_height = 118
    jump = False    
    y_prev = None
    y_h = 600
    while(True):
        screen = grab_screen(region=(300,350,650,540))
        screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
        
        im_gray = cv2.GaussianBlur(screen, (5, 5), 0)
        _, im_th = cv2.threshold(im_gray, 90, 255, cv2.THRESH_BINARY_INV)
        _, ctrs, _ = cv2.findContours(im_th.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        rects = [cv2.boundingRect(ctr) for ctr in ctrs]
        rects.sort(key=lambda x: x[0])

        if jump:
            try:
                y = rects[0][1]
                if abs(y - y_start) < 5 and y_prev < y:
                    jump_time = time.time() - jump_time
                    print('jump time', jump_time)
                    print('height', y_start - y_h)
                    jump = False
                    y_h = 600
                if y < y_h:
                    y_h = y
                y_prev = y
            except:
                pass
        
        k = key_check()
        
        if 'up' in k and not jump:
            jump_time = time.time()
            y_start = rects[0][1]
            y_prev = y_start
            jump = True
            print('tstart ', jump_time, 'y_start', y_start)
        elif 'R' in k:
            jump = False
        
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

        cv2.imshow('xxx', screen)
        
main()