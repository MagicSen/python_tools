##
# @file createBackgroundData.py
# @brief Create Background data
# @author Yang Sen, magicys@qq.com
# @version 1.0.0
# @date 2017-11-28

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

def createTxtLabel(file_name):
    fin = open(file_name, 'w')
    fin.writelines("0 0 0 0 0\n0 0 0 0 0\n0 0 0 0 0\n0 0 0 0 0")
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
        img_file = item.strip("\n")
        base_name = os.path.basename(img_file).split(".")[0][3:]
        txt_name = os.path.join(fout_dir, base_name + ".txt")
        resize_img_name = os.path.join(fout_dir, base_name + ".png")
        img = cv2.imread(img_file, 0)
        resize_img = cv2.resize(img,(128, 96),interpolation=cv2.INTER_NEAREST)
        cv2.imwrite(resize_img_name, resize_img)
        createTxtLabel(txt_name)
