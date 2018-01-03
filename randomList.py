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

if __name__ == "__main__":
    if(len(sys.argv) < 3):
        print "<fin_input_image_list> <fout_list_name>"
        sys.exit()
    source_list_file = sys.argv[1]
    source_list = getListFromFile(source_list_file, "")
    fout = open(sys.argv[2], 'w')
    random.shuffle(source_list)
    for item in source_list:
        fout.writelines(item.strip("\n") + "\n")
    fout.close()
