import cv2
import numpy as np
import sys

file_name = sys.argv[1]
img = cv2.imread(file_name)

def gauss(l, sig):

    mesh_ele = np.linspace(-(l-1)/2.0, (l-1)/2.0, l)
    x, y = np.meshgrid(mesh_ele, mesh_ele)

    kernel = np.exp(-(x**2 + y**2)/(2.0*sig**2))

    return kernel/np.sum(kernel)

g_kernel = gauss(3, 0.5)

dst = cv2.filter2D(img,-1,g_kernel)
edges = cv2.Canny(dst, 120, 170, apertureSize=3)
lines = cv2.HoughLines(edges, 1, np.pi/180, 85)

lines = lines[lines[:, 0, 0].argsort()]

i = 0
n = lines.shape[0]

while i<n:
  j = i+1
  sum_r = lines[i][0][0]
  sum_theta = lines[i][0][1]
  while (j<n and np.abs(lines[j][0][0] - lines[i][0][0])<30 and np.abs(lines[j][0][1] - lines[i][0][1])<0.85):
    sum_r+=lines[j][0][0]
    sum_theta+=lines[j][0][1]
    j+=1
    
  if(j-i>0):
    r = sum_r/(1.0*(j-i))
    theta = sum_theta/(1.0*(j-i))

    a = np.cos(theta)
    b = np.sin(theta)
 
    x0 = a*r
    y0 = b*r
 
    x1 = int(x0 + 1000*(-b))
    y1 = int(y0 + 1000*(a))
 
    x2 = int(x0 - 1000*(-b))
    y2 = int(y0 - 1000*(a))
 
    cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)

  i = j

tiles_s = file_name[-10:]
cv2.imwrite("robolin-" + tiles_s, img)