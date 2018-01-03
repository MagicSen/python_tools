#coding=utf-8
##
# @file getInformationFromJson.py
# @brief AI Challenger Data Process program: get information from json file.
# @author Yang Sen, magicys@qq.com
# @version 1.0.0
# @date 2017-09-06
# Copyright(C)
# For free
# All right reserved
# 

import os,sys
import json
import shutil

def listToStr(list_a):
    list_str = []
    for item in list_a:
        list_str.append(str(item))
    return list_str

def listListToFile(list_list, file_name):
    fout = open(file_name, 'w')
    for item in list_list:
        fout.writelines(" ".join(listToStr(item)) + "\n")
    fout.close()

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print "<fin_json_file> <fout_detection_rect_dir> <fout_human_joint_dir>"
        sys.exit()
    json_file = sys.argv[1]
    detection_rect_dir = sys.argv[2]
    human_joint_dir = sys.argv[3]
    if not os.path.exists(detection_rect_dir):
        os.mkdir(detection_rect_dir)
    if not os.path.exists(human_joint_dir):
        os.mkdir(human_joint_dir)
    json_file_ = file(json_file)
    json_detail = json.load(json_file_)
    print "Total image dataset number: " + str(len(json_detail))
    number = 1
    static_inf = {}
    for image_detail in json_detail:
        image_name = image_detail['image_id']
        txt_name = image_name.split('.')[0] + ".txt"
        human_keys = image_detail['human_annotations'].keys()
        human_rect_list = []
        human_joint_list = []
        for human in human_keys:
            human_rect_list.append(image_detail['human_annotations'][human])
            human_joint_list.append(image_detail['keypoint_annotations'][human])
        listListToFile(human_rect_list, os.path.join(detection_rect_dir, txt_name))
        listListToFile(human_joint_list, os.path.join(human_joint_dir, txt_name))
        print "Number: " + str(number) + " "+ image_name + " Human number: " + str(len(human_rect_list))
        if not static_inf.has_key(len(human_rect_list)):
            static_inf[len(human_rect_list)] = 0
        static_inf[len(human_rect_list)] = static_inf[len(human_rect_list)] + 1
        number = number + 1
    static_out = open("static.txt",'w')
    keys = static_inf.keys()
    for key in keys:
        static_out.writelines(str(key) + ": " + str(static_inf[key]) + " " + str(float(static_inf[key])/number) + "\n")
    static_out.close()
