##
# @file createFlipImage.py
# @brief Create flip image and label
# @author Yang Sen, magicys@qq.com
# @version 1.0.0
# @date 2017-11-29


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
    line = lines[1]
    str_title = line.strip("\n").split(' ')
    if int(str_title[0]) == 0:
        return [0, 0, 0, 0]
    return [float(str_title[1]), float(str_title[2]), float(str_title[3]), float(str_title[4])]

def getFlipRect(rect):
    width = rect[2] - rect[0]
    height = rect[3] - rect[1]
    return [1 - rect[0] - width, rect[1], 1 - rect[0], rect[3]]

def rectToString(rect):
    return str(rect[0]) + " " + str(rect[1]) + " " + str(rect[2]) + " " + str(rect[3])

def rectLeftToFile(rect, file_name):
    rect_new = getFlipRect(rect)
    rect_str = rectToString(rect_new)
    fin = open(file_name, 'w')
    fin.writelines("1 " + rect_str + "\n0 0 0 0 0\n0 0 0 0 0\n0 0 0 0 0")
    fin.close()

if __name__ == "__main__":
    if(len(sys.argv) < 3):
        print "<fin_input_image_list> <fout_folder>"
        sys.exit()
    source_list_file = sys.argv[1]
    fout_dir = sys.argv[2]
    if not os.path.exists(fout_dir):
        os.mkdir(fout_dir)
    source_list = getListFromFile(source_list_file, "")
    for item in source_list:
        print item
        base_dir = os.path.join(fout_dir, os.path.dirname(item))
        if not os.path.exists(base_dir):
            os.makedirs(base_dir)
        base_name = os.path.basename(item)
        new_item = os.path.join(base_dir, base_name)

        image_left = item + "0.png"
        image_right = item + "1.png"
        txt_left = item + "0.txt"
        txt_right = item + "1.txt"

        new_image_left = new_item + "0.png"
        new_image_right = new_item + "1.png"
        new_txt_left = new_item + "0.txt"
        new_txt_right = new_item + "1.txt"

        left_rect = getRectFromList(txt_left)
        right_rect = getRectFromList(txt_right)
        rectLeftToFile(left_rect, new_txt_left)
        rectLeftToFile(right_rect, new_txt_right)

        left_img = cv2.imread(image_left,0)
        right_img = cv2.imread(image_right,0)


        left_img_flip = cv2.flip(left_img, 1)
        right_img_flip = cv2.flip(right_img, 1)
        cv2.imwrite(new_image_left, left_img_flip)
        cv2.imwrite(new_image_right, right_img_flip)
