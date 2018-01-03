##
# @file CreateSquenceImage.py
# @brief Divide list to subsequence and shuffle
# @author Yang Sen, magicys@qq.com
# @version 1.0.0
# @date 2017-08-31

import sys, os
import random

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

def dividListToSubList(list_all):
    list_subdir_dict = {}
    for name in list_all:
        dir_name = os.path.dirname(name)
        if dir_name not in list_subdir_dict:
            list_subdir_dict[dir_name] = []
        list_subdir_dict[dir_name].append(name)
    return list_subdir_dict

def cutSequence(list_subdir_dict, sequence_length, is_shuffle):
    list_subdir_dict_cut_sequence = []
    key_all = list_subdir_dict.keys()
    for key in key_all:
        subdir_list = list_subdir_dict[key]
        begin_index = 0
        while begin_index < len(subdir_list):
            sequence_len = random.choice(sequence_length)
            end_index = min(begin_index + sequence_len, len(subdir_list))
            list_temp = subdir_list[begin_index:end_index]
            list_subdir_dict_cut_sequence.append(list_temp)
            begin_index = end_index
    if is_shuffle:
        random.shuffle(list_subdir_dict_cut_sequence)
    return list_subdir_dict_cut_sequence

def writeListToFile(shuffle_list, shuffle_list_file):
    fout = open(shuffle_list_file, 'w')
    for i in range(0, len(shuffle_list)):
        for j in range(0, len(shuffle_list[i])):
            if j == 0:
                fout.writelines(shuffle_list[i][j] + "\t" + "0" + "\n")
            else:
                fout.writelines(shuffle_list[i][j] + "\t" + "1" + "\n")
    fout.close()

if __name__ == "__main__":
    if(len(sys.argv) < 3):
        print "<fin_input_image_list> <fout_input_image_list>"
        sys.exit()
    source_list_file = sys.argv[1]
    shuffle_list_file = sys.argv[2]
    ignore_last_str = "_1.png"
    sequence_length = [5, 6, 7, 8, 9, 10]
    #sequence_length = [2]
    is_shuffle = True
    list_all = getListFromFile(source_list_file, ignore_last_str) 
    list_subdir_dict = dividListToSubList(list_all)
    list_subdir_dict_cut_sequence = cutSequence(list_subdir_dict, sequence_length, is_shuffle) 
    writeListToFile(list_subdir_dict_cut_sequence, shuffle_list_file)
