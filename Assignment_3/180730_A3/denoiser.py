import cv2
import numpy as np
import sys

file_name = sys.argv[1]
img = cv2.imread(file_name)

def gauss_scal(x, sig):
    return np.exp(-(x**2)/(2.0*sig**2))

def gauss_mat(l, sig):
    mesh_ele = np.linspace(-(l-1)/2.0, (l-1)/2.0, l)
    x, y = np.meshgrid(mesh_ele, mesh_ele)
    kernel = np.exp(-(x**2 + y**2)/(2.0*sig**2))
    return kernel/np.sum(kernel)

def apply_bf(source, x, y, half_step, sigma_i, sigma_s):

    i_start = x-half_step
    i_stop = x+half_step+1
    j_start = y-half_step
    j_stop = y+half_step+1
    img_crop = np.copy(source[i_start:i_stop, j_start:j_stop, :])
    source_point = np.repeat([np.repeat([source[x, y, :]], img_crop.shape[1], axis=0)], img_crop.shape[0], axis=0)

    gi = gauss_scal(img_crop - source_point, sigma_i)
    gs = np.repeat(gauss_mat(2*half_step+1, sigma_s)[:, :, np.newaxis], 3, axis=2)

    filt = np.mean(gi*gs, axis=2)
    r = np.sum(filt*img_crop[:, :, 0])/np.sum(filt)
    g = np.sum(filt*img_crop[:, :, 1])/np.sum(filt)
    b = np.sum(filt*img_crop[:, :, 2])/np.sum(filt)

    return (r, g, b)

def bilateral_filter(source, half_step, sigma_i, sigma_s):
    filtered_image = np.copy(source)

    source_padded = np.zeros([source.shape[0] + 2*half_step, source.shape[1] + 2*half_step, 3])
    source_padded[half_step:source.shape[0]+half_step, half_step:source.shape[1]+half_step, :] = source

    for i in range(half_step, source.shape[0]+half_step):
        for j in range(half_step, source.shape[1]+half_step):
            filtered_image[i-half_step, j-half_step, :] = apply_bf(source_padded, i, j, half_step, sigma_i, sigma_s)
    return filtered_image

if(file_name[-5]=='2'):
    filtered_image = bilateral_filter(img, 6, 16, 7)

else:
    filtered_image = bilateral_filter(img, 5, 22, 7)

cv2.imwrite("denoised.jpg", filtered_image)