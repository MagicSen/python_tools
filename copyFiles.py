##
# @file copyImage.py
# @brief Copy image from one dir to another
# @author Yang Sen, magicys@qq.com
# @version 1.0.0
# @date 2017-09-10

import os,sys
import shutil

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
    if len(sys.argv) < 5:
        print "<fin_file_list> <fin_file_suffix> <fin_file_dir> <fout_file_dir>"
        sys.exit()
    list_1 = getListFromFile(sys.argv[1])
    file_suffix = "." + sys.argv[2]
    file_dir = sys.argv[3]
    fout_dir = sys.argv[4]
    if not os.path.exists(fout_dir):
        os.mkdir(fout_dir)
    for item in list_1:
        file_name = os.path.join(file_dir, item + file_suffix)
        file_out_name = os.path.join(fout_dir, item + file_suffix)
        shutil.copy(file_name, file_out_name)
