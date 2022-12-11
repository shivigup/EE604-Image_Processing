import cv2
import numpy as np
import sys

x_centers = np.array([30, 90, 150])
x_leftmost = np.array([35, 285])
y_centers = np.array(range(30, 300, 60))

def make_circle(A, Ox, Oy):
  r = 25
  for y in range(-r, r+1):
    X_range = int(np.sqrt(r**2 - y**2))
    for x in range(-X_range, X_range+1):
      A[Oy+y, Ox+x] = 255
  return A

def zero(A, digit):
  n = x_leftmost[digit]
  for j in y_centers:
    A = make_circle(A, n + x_centers[0], j)
    A = make_circle(A, n + x_centers[2], j)
  A = make_circle(A, n + x_centers[1], y_centers[0])
  A = make_circle(A, n + x_centers[1], y_centers[4])
  return A

def one(A, digit):
  n = x_leftmost[digit]
  for j in y_centers:
    A = make_circle(A, n + x_centers[1], j)
  return A;

def two(A, digit):
  n = x_leftmost[digit]
  for j in y_centers[[0, 2, 4]]:
    for i in x_centers:
      A = make_circle(A, n + i, j)
  A = make_circle(A, n+x_centers[2], y_centers[1])
  A = make_circle(A, n+x_centers[0], y_centers[3])
  return A;

def three(A, digit):
  n = x_leftmost[digit]
  for j in y_centers[[0, 2, 4]]:
    for i in x_centers:
      A = make_circle(A, n + i, j)
  A = make_circle(A, n+x_centers[2], y_centers[1])
  A = make_circle(A, n+x_centers[2], y_centers[3])
  return A;

def four(A, digit):
  n = x_leftmost[digit]
  for j in y_centers:
    A = make_circle(A, n + x_centers[2], j)
  A = make_circle(A, n+x_centers[0], y_centers[2])
  A = make_circle(A, n+x_centers[1], y_centers[2])
  A = make_circle(A, n+x_centers[0], y_centers[0])
  A = make_circle(A, n+x_centers[0], y_centers[1])
  return A;

def five(A, digit):
  n = x_leftmost[digit]
  for j in y_centers[[0, 2, 4]]:
    for i in x_centers:
      A = make_circle(A, n + i, j)
  A = make_circle(A, n+x_centers[0], y_centers[1])
  A = make_circle(A, n+x_centers[2], y_centers[3])
  return A;

def six(A, digit):
  n = x_leftmost[digit]
  for j in y_centers[[0, 2, 4]]:
    for i in x_centers:
      A = make_circle(A, n + i, j)
  A = make_circle(A, n+x_centers[0], y_centers[1])
  A = make_circle(A, n+x_centers[2], y_centers[3])
  A = make_circle(A, n+x_centers[0], y_centers[3])
  return A;

def seven(A, digit):
  n = x_leftmost[digit]
  for j in y_centers:
    A = make_circle(A, n + x_centers[2], j)
  A = make_circle(A, n+x_centers[0], y_centers[0])
  A = make_circle(A, n+x_centers[1], y_centers[0])
  return A;

def eight(A, digit):
  n = x_leftmost[digit]
  for j in y_centers:
    A = make_circle(A, n + x_centers[0], j)
    A = make_circle(A, n + x_centers[2], j)
  A = make_circle(A, n + x_centers[1], y_centers[0])
  A = make_circle(A, n + x_centers[1], y_centers[2])
  A = make_circle(A, n + x_centers[1], y_centers[4])
  return A

def nine(A, digit):
  n = x_leftmost[digit]
  for j in y_centers[[0, 2, 4]]:
    for i in x_centers:
      A = make_circle(A, n + i, j)
  A = make_circle(A, n+x_centers[0], y_centers[1])
  A = make_circle(A, n+x_centers[2], y_centers[1])
  A = make_circle(A, n+x_centers[2], y_centers[3])
  return A;

def generate_image(x):
  digits = np.zeros(2)
  digits[1] = x%10
  x = (int)(x/10)
  digits[0] = x%10
  A = np.zeros((300, 500))
  for i in range(2):
    if(digits[i]==0):
      A = zero(A, i)
    if(digits[i]==1):
      A = one(A, i)
    if(digits[i]==2):
      A = two(A, i)
    if(digits[i]==3):
      A = three(A, i)
    if(digits[i]==4):
      A = four(A, i)
    if(digits[i]==5):
      A = five(A, i)
    if(digits[i]==6):
      A = six(A, i)
    if(digits[i]==7):
      A = seven(A, i)
    if(digits[i]==8):
      A = eight(A, i)
    if(digits[i]==9):
      A = nine(A, i)
  return A

num = int(sys.argv[1])

A = generate_image(num)

cv2.imwrite("dotmatrix.jpg", A)