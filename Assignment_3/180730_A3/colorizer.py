import cv2
import numpy as np
import sys

file_name_1 = sys.argv[1]
file_name_2 = sys.argv[2]
file_name_3 = sys.argv[3]

Y = cv2.imread(file_name_1)
Cb = cv2.imread(file_name_2)
Cr = cv2.imread(file_name_3)

gray_Cb = cv2.cvtColor(Cb, cv2.COLOR_BGR2GRAY)
gray_Cr = cv2.cvtColor(Cr, cv2.COLOR_BGR2GRAY)
gray_Y = cv2.cvtColor(Y, cv2.COLOR_BGR2GRAY)

def gauss_mat(l, sig):
    mesh_ele = np.linspace(-(l-1)/2.0, (l-1)/2.0, l)
    x, y = np.meshgrid(mesh_ele, mesh_ele)
    kernel = np.exp(-(x**2 + y**2)/(2.0*sig**2))
    return kernel/np.sum(kernel)

def gauss_scal(x, sig):
    return np.exp(-(x**2)/(2.0*sig**2))

def apply_bu(source, img, x, y, half_step, sigma_i, sigma_s):

    i_start = x-half_step
    i_stop = x+half_step+1
    j_start = y-half_step
    j_stop = y+half_step+1
    source_crop = np.copy(source[i_start:i_stop, j_start:j_stop])
    img_crop = np.copy(img[i_start:i_stop, j_start:j_stop])
    source_point = source[x, y]
    #source_point = np.repeat([np.repeat([source[x, y]], source_crop.shape[1], axis=0)], source_crop.shape[0], axis=0)

    gi = gauss_scal(source_crop - source_point, sigma_i)
    gs = gauss_mat(2*half_step+1, sigma_s)

    filt = gi*gs
    #print(filt.shape, img_crop.shape)
    return np.sum(filt*img_crop)/np.sum(filt)

def bilateral_upsampler(source, img, half_step, sigma_i, sigma_s):
    upsampled_image = np.copy(source)
    img_resized = np.array(cv2.resize(img, (source.shape[1], source.shape[0])))

    img_padded = np.zeros([source.shape[0] + 2*half_step, source.shape[1] + 2*half_step])
    img_padded[half_step:source.shape[0]+half_step, half_step:source.shape[1]+half_step] = img_resized

    source_padded = np.zeros([source.shape[0] + 2*half_step, source.shape[1] + 2*half_step])
    source_padded[half_step:source.shape[0]+half_step, half_step:source.shape[1]+half_step] = source

    for i in range(half_step, source.shape[0]+half_step):
        for j in range(half_step, source.shape[1]+half_step):
          upsampled_image[i-half_step, j-half_step] = int(apply_bu(source_padded, img_padded, i, j, half_step, sigma_i, sigma_s))
    return upsampled_image

Cb_upsampled = bilateral_upsampler(gray_Y, gray_Cb, 5, 10, 5)
Cr_upsampled = bilateral_upsampler(gray_Y, gray_Cr, 5, 10, 5)

YCrCb = np.stack([gray_Y, Cr_upsampled, Cb_upsampled], axis=2)
img_bgr = cv2.cvtColor(YCrCb, cv2.COLOR_YCrCb2BGR)

cv2.imwrite("flyingelephant.jpg", img_bgr)