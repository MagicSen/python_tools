##
# @file drawListTools.py
# @brief Draw Image from Rect
# @author Yang Sen, magicys@qq.com
# @version 1.0.0
# @date 2017-11-27

import sys, os
import random
import cv2
import numpy as np  


def getListFromFile(file_name, ignore_last_str):
    if not os.path.exists(file_name):
        print "Error: File is not exists."
        return []
    list_file = open(file_name, 'r')
    list_all = []
    for line in list_file:
        item = line.strip("\n").strip(' ')
        if len(item) != 0:
            if len(ignore_last_str) == 0:
                list_all.append(item)
            elif ignore_last_str not in item:
                list_all.append(item)
    list_file.close()
    return list_all

def getRectFromList(txt):
    fin = open(txt, 'r')
    lines = fin.readlines()
    fin.close()
    #line = lines[1]
    line = lines[0]
    str_title = line.strip("\n").split(' ')
    if int(str_title[0]) == 0:
        return [0, 0, 0, 0]
    x = int(128 * float(str_title[1]))
    y = int(96 * float(str_title[2]))
    width = int(128 * float(str_title[3]))
    height = int(96 * float(str_title[4]))
    return [x, y, width, height]

if __name__ == "__main__":
    if(len(sys.argv) < 2):
        print "<fin_input_image_list>"
        sys.exit()
    source_list_file = sys.argv[1]
    source_list = getListFromFile(source_list_file, "")
    for item in source_list:
        image_left = item + "0.png"
        image_right = item + "1.png"
        txt_left = item + "0.txt"
        txt_right = item + "1.txt"
        left_rect = getRectFromList(txt_left)
        right_rect = getRectFromList(txt_right)
        if left_rect[0] == 0 and left_rect[2] == 0:
            continue
        print item
        left_img = cv2.imread(image_left,1)
        right_img = cv2.imread(image_right,1)
        cv2.rectangle(left_img, (left_rect[0], left_rect[1]), (left_rect[2], left_rect[3]), (0, 255, 0), 3)  
        cv2.rectangle(right_img, (right_rect[0], right_rect[1]), (right_rect[2], right_rect[3]), (0, 255, 0), 3)  
        left_img=cv2.resize(left_img,(640,480),interpolation=cv2.INTER_CUBIC)
        right_img=cv2.resize(right_img,(640,480),interpolation=cv2.INTER_CUBIC)
        cv2.imshow('left image', left_img)  
        cv2.imshow('right image', right_img)  
        cv2.waitKey(0)  
