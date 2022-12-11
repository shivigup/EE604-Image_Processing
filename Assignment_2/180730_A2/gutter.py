import cv2
import numpy as np
import sys

file_name = sys.argv[1]
img = cv2.imread(file_name)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def gauss(l, sig):

    mesh_ele = np.linspace(-(l-1)/2.0, (l-1)/2.0, l)
    x, y = np.meshgrid(mesh_ele, mesh_ele)
    kernel = np.exp(-(x**2 + y**2)/(2.0*sig**2))
    return kernel/np.sum(kernel)

g_kernel = gauss(500,30)
dst = cv2.filter2D(gray,-1,g_kernel)

scaling = 0.7
threshold = 170
gamma_high = 0.5
gamma_low = 5

scaled = gray + scaling*(255 - dst)
thresh = 255*((scaled>threshold)*scaled/255.0)**gamma_high + 255*((scaled<threshold)*scaled/255.0)**gamma_low

cv2.imwrite("cleaned-gutter.jpg", thresh)