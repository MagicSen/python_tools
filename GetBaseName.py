##
# @file GetFolderData.py
# @brief Given a suffix and return folder's file list to a file or return a file list
# @author Yang Sen, magicys@qq.com
# @version 1.0.1
# @date 2017-02-06
# Copyright(C)
# For free
# All right reserved
# 

import sys,os


def listToStr(number_list):
    str_list = []
    for num in number_list:
        str_list.append(str(num))
    return str_list

def readLabelFile(file_name):
    if not os.path.exists(file_name):
        return []
    fin = open(file_name, 'r')
    rect_list = []
    for line in fin:
        str_title = line.strip('\n').strip(' ').split(' ')
        rect = []
        for num in str_title:
            rect.append(int(num))
        rect_list.append(rect)
    return rect_list
##
# @brief getFileListFromFolder 
# Get a file list from a given folder
# @param folder
#
# @return 
def getFileListFromFolder(folder):
    file_list = []
    for root, dirs, files in os.walk(folder, topdown=False):
        for name in files:
            file_list.append(os.path.join(root, name))
    return file_list

##
# @brief getListFromFile 
# Get a list from a file
# @param file_name 
#
# @return 
def getListFromFile(file_name):
    if not os.path.exists(file_name):
        print "Error: File is not exists."
        return []
    list_file = open(file_name, 'r')
    list_all = []
    for line in list_file:
        item = line.strip("\n").strip(' ')
        if len(item) != 0:
            list_all.append(item)
    list_file.close()
    return list_all

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print "<input_folder> <fin_file_suffix> <output_file_list>"
        sys.exit()
    file_list = getFileListFromFolder(sys.argv[1])
    suffix = sys.argv[2]
    fout = open(sys.argv[3], 'w')
    for i in range(0, len(file_list)):
        if suffix in file_list[i]:
            str_title = file_list[i].split("\\")[-1]
            fout.writelines(str_title.split('.')[0] + "\n")
    fout.close()
    print "Get files list succeed."
