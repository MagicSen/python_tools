##
# @file divideTrainTestSet.py
# @brief Given ratio, divid data set to train and test set.
# @author Yang Sen, magicys@qq.com
# @version 1.0.0
# @date 2017-09-09

import os,sys

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
        print "<fin_total_list> <fin_ratio> <fout_train_list> <fout_test_list>"
        sys.exit()
    file_list = getListFromFile(sys.argv[1])
    ratio = float(sys.argv[2])
    fout_train_list = open(sys.argv[3], 'w')
    fout_test_list = open(sys.argv[4], 'w')
    total_number = len(file_list)
    train_number = total_number * ratio
    for i in range(total_number):
        if i < train_number:
            fout_train_list.writelines(file_list[i] + "\n")
        else:
            fout_test_list.writelines(file_list[i] + "\n")
    fout_train_list.close()
    fout_test_list.close()
