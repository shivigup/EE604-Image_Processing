import cv2
import numpy as np
import sys

file_name = sys.argv[1]
img = cv2.imread(file_name)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

gray = gray*255.0/np.max(gray)

def hist(img, k=0.05):
  flat = img.flatten()
  histogram = np.zeros(256)
  for pix in flat:
    histogram[pix]+=1
  
  cum = np.zeros(256)
  cum[0] = histogram[0]

  for i in range(1, 256):
    cum[i] = histogram[i] + cum[i-1]

  cum = cum.astype('uint8')

  img_new = k*cum[flat] + (1-k)*flat
  img_new = np.reshape(img_new, img.shape)

  return img_new

gray = gray.astype('uint8')
eq = hist(gray)

cctv_s = file_name[-9:]
cv2.imwrite("enhanced-" + cctv_s, eq)