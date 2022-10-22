import cv2
import os.path
import os
import numpy as np
import pandas as pd
import mmcv
from PIL import Image
import os.path as osp

data_pd = pd.read_csv('./C._Diabetic_Retinopathy_Grading/2._Groundtruths/a._DRAC2022_ Diabetic_Retinopathy_Grading_Training_Labels.csv')
image_name = list(data_pd['image name'])
DR_grade = list(data_pd['DR grade'])

output_list = []
output_list_ = []

for i in range(611):
  output_list.append(image_name[i][:-4] + ".jpg")
  output_list.append("00_" + image_name[i][:-4] + ".jpg")
  output_list.append("11_" + image_name[i][:-4] + ".jpg")
  output_list.append("90_" + image_name[i][:-4] + ".jpg")
  output_list.append("180_" + image_name[i][:-4] + ".jpg")
  output_list.append("270_" + image_name[i][:-4] + ".jpg")
  for j in range(6):
    output_list_.append(DR_grade[i])

file = open('./Data/Pretrained_files.txt','w',encoding='utf-8')
for i in range(len(output_list)):
  file.write(str(output_list[i]) + ' ' + str(output_list_[i])  +'\n')
file.close()

img_dir = '/.C._Diabetic_Retinopathy_Grading/1._Original_Images/a._Training_Set'
for file in mmcv.scandir(img_dir, suffix='.png'):
  Original_image_224 = cv2.imread(img_dir + '/' + file, 1)
  Original_image_224 = Image.fromarray(Original_image_224).convert('RGB')
  Original_image_224 = Original_image_224.resize((224, 224), Image.ANTIALIAS)
  # raw 224 image saving
  Original_image_224.save(osp.join("./Data/", file.replace('.png','.jpg')))
  # Flip horizontal
  image_224_flip_left_right = Original_image_224.transpose(Image.FLIP_LEFT_RIGHT)
  image_224_flip_left_right.save(osp.join("/content/data", "00_" + file.replace('.png','.jpg')))
  # Flip vertical
  image_224_flip_top_bottom = Original_image_224.transpose(Image.FLIP_TOP_BOTTOM)
  image_224_flip_top_bottom.save(osp.join("/content/data", "11_" + file.replace('.png','.jpg')))
  # rotate 90 640 raw image saving
  image_224_90 = Original_image_224.rotate(90, expand=1)
  image_224_90.save(osp.join("/content/data", "90_" + file.replace('.png','.jpg')))
  # rotate 180 640 raw image saving
  image_224_180 = Original_image_224.rotate(180, expand=1)
  image_224_180.save(osp.join("/content/data", "180_" + file.replace('.png','.jpg')))
  # rotate 270 640 raw image saving
  image_224_270 = Original_image_224.rotate(270, expand=1)
  image_224_270.save(osp.join("/content/data", "270_" + file.replace('.png','.jpg')))

