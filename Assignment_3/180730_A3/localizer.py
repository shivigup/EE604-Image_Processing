import cv2
import numpy as np
import sys

file_name = sys.argv[1]
img = cv2.imread(file_name)
img = img[:, :, [2, 1, 0]] 

features_1 = np.array([240.11127273, 226.99272727,  21.15781818,  13.37527273])
features_2 = np.array([207.74244444,  31.52266667, 202.022     ,  42.56866667])
features_3 = np.array([ 19.22068966,  15.00765086, 225.55096983, 236.22758621])

def get_features(img):
  f1 = np.mean(img[:,:,0] - img[:,:,1])
  f2 = np.mean(img[:,:,1] - img[:,:,2])
  f3 = np.mean(img[:,:,2] - img[:,:,0])
  f4 = np.mean(2*img[:,:,1] - img[:,:,0] - img[:,:,1])
  return np.array([f1, f2, f3, f4])

features = get_features(img)

dist = np.array([np.linalg.norm(features - features_1), np.linalg.norm(features - features_2), np.linalg.norm(features - features_3)])
print(1+np.argmin(dist))