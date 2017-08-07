import cv2
import numpy as np
from matplotlib import pyplot as plt
from PIL import ImageGrab
import time
from grab_scr import grab_screen



'''img_rgb = cv2.imread('test.png')
img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
template = cv2.imread('3.png',0)
w, h = template.shape[::-1]
res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)

cv2.imwrite('check.png',res)
pt = cv2.minMaxLoc(res)[-1]
#threshold = 0.8
#loc = np.where( res >= threshold)

#for pt in zip(*loc[::-1]):
#    cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)

cv2.imwrite('res.png',img_rgb)'''


img_rgb = cv2.imread('test2.png')
img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

threshold = 0.4

template = cv2.imread('2.png',0)
template=cv2.resize(template,(30,40))
w, h = template.shape[::-1]


res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)

loc = np.where( res >= threshold)

for pt in zip(*loc[::-1]):
    print (pt)
    cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
cv2.imwrite('res.png',img_rgb)
