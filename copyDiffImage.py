##
# @file copyDiffImage.py
# @brief Given two list, write diff list to file.
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
    if len(sys.argv) < 4:
        print "<fin_base_list> <fin_base_list2> <fout_diff_list>"
        sys.exit()
    list_1 = getListFromFile(sys.argv[1])
    list_2 = getListFromFile(sys.argv[2])
    list_diff = []
    for item1 in list_1:
        if item1 not in list_2:
            print item1
            list_diff.append(item1)
    fout = open(sys.argv[3], 'w')
    for item in list_diff:
        fout.writelines(item + "\n")
    fout.close()



