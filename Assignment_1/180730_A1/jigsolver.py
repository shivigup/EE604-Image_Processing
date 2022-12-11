import cv2
import numpy as np
import sys

file_name = sys.argv[1]
img = cv2.imread(file_name)


img_temp = img[:, :190, :]
img_1 = img_temp[:200, :, [1, 0, 2]]
img_2_temp = img_temp[200:410, :, :]
img_2 = np.flip(img_2_temp, axis = 0)

img_3 = img[150: 330, 515:700, :]
img_3 = np.flip(img_3, axis = 1)

img_4 = img[370:, 370:, :]
img_4 = np.flip(img_4, axis = 0)

shape_1 = img_1.shape
shape_2 = img_2.shape

img_final = np.copy(img)
img_final[:shape_2[0], :shape_2[1], :] = img_2
img_final[shape_2[0]-10:shape_2[0]+shape_1[0]-10, :shape_2[1], :] = img_1
img_final[150: 330, 515:700, :] = img_3
img_final[370:, 370:, :] = img_4

img_5 = img_final[shape_2[0]+shape_1[0]-15:shape_2[0]+shape_1[0]-10, :shape_2[1], :]
img_5 = np.flip(img_5, axis = 0)
img_6 = img_final[shape_2[0]+shape_1[0]:shape_2[0]+shape_1[0]+5, :shape_2[1], :]
img_6 = np.flip(img_6, axis = 0)

img_final[shape_2[0]+shape_1[0]-10:shape_2[0]+shape_1[0]-5, :shape_2[1], :] = img_5
img_final[shape_2[0]+shape_1[0]-5:shape_2[0]+shape_1[0], :shape_2[1], :] = img_6

img_temp = np.copy(img_final[shape_2[0]+shape_1[0]-10:shape_2[0]+shape_1[0], :shape_2[1], :])

w = 5

## Smoothening

for i in range(shape_2[0]+shape_1[0]-10, shape_2[0]+shape_1[0]):
    for j in range(w, shape_2[1]):
        img_temp[i-(shape_2[0]+shape_1[0]-10), j-w, :] = np.mean(img_final[i-3:i+3, j-3:j+3, :], axis = (0, 1))

img_final[shape_2[0]+shape_1[0]-10:shape_2[0]+shape_1[0], :shape_2[1], :] = img_temp

cv2.imwrite("jigsolved.jpg", img_final)