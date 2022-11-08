import cv2
import glob
import numpy as np
import os

#Turns images into video
img_array = []
files = sorted(glob.glob('images\*.jpg'), key=os.path.getmtime)
for filename in files:
    img = cv2.imread(filename)
    height, width, layers = img.shape
    size = (width,height)
    img_array.append(img)

out = cv2.VideoWriter('project.mp4',cv2.VideoWriter_fourcc(*'DIVX'), 60, size)

for i in range(len(img_array)):
    out.write(img_array[i])
out.release()