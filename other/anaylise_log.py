##
# @file anaylise_log.py
# @brief Anaylise the caffe printing log.
# @author Yang Sen, magicys@qq.com
# @version 1.0.0
# @date 2016-03-23
# Copyright(C)
# For free
# All right reserved
# 
import os,sys

def divideLogByKeyWords(fin_lines):
    total_iterator = {}
    i = 0
    while i < len(fin_lines):
        line = fin_lines[i]
        if "Iteration" in line:
            str_title = line.strip("\n").split(" ")
            iterator_num = int(str_title[5].strip(","))
            if not total_iterator.has_key(iterator_num):
                total_iterator[iterator_num] = {"test": None, "train": None}
            if "Testing" in line:
                accuracy = fin_lines[i+1].strip("\n").split("=")[-1]
                loss1 = fin_lines[i+2].strip("\n").split("(")[0].split("=")[-1]
                loss2 = fin_lines[i+3].strip("\n").split("(")[0].split("=")[-1]
                loss3 = fin_lines[i+4].strip("\n").split("(")[0].split("=")[-1]
                recall = fin_lines[i+5].strip("\n").split("=")[-1]
                total_iterator[iterator_num]["test"] = {"accuracy": accuracy, "loss1": loss1, "loss2": loss2, "loss3": loss3, "recall": recall}
                i = i + 6
            else:
                loss1 = fin_lines[i+1].strip("\n").split("(")[0].split("=")[-1]
                loss2 = fin_lines[i+2].strip("\n").split("(")[0].split("=")[-1]
                loss3 = fin_lines[i+3].strip("\n").split("(")[0].split("=")[-1]
                total_iterator[iterator_num]["train"] = {"loss1": loss1, "loss2": loss2, "loss3": loss3}
                if iterator_num/1000 == 900:
                    i = i + 7
                else:
                    i = i + 5
        else:
            i = i + 1
    return total_iterator

def getInformationFromType(iterator_lines, flag_type):
    flag_title = flag_type.strip(" ").split("_")
    information_detail = {}
    keys = iterator_lines.keys()
    for key in keys:
        if iterator_lines.has_key(key) and iterator_lines[key][flag_title[0]] != None:
            if flag_title[1] == "loss":
                information_detail[key] = str(iterator_lines[key][flag_title[0]]["loss1"]) + "\t" + str(iterator_lines[key][flag_title[0]]["loss2"]) + "\t" + str(iterator_lines[key][flag_title[0]]["loss3"])
            else:
                information_detail[key] = iterator_lines[key][flag_title[0]]["accuracy"] + "\t" + iterator_lines[key][flag_title[0]]["recall"]
    return information_detail


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print "<fin_log_file> <fout_file> <flag_type>"
        sys.exit()
    fin_file_lines = open(sys.argv[1], 'r').readlines()
    fout_file = open(sys.argv[2], 'w')
    flag_type = sys.argv[3]
    iterator_lines = divideLogByKeyWords(fin_file_lines)
    information_detail = getInformationFromType(iterator_lines, flag_type)
    keys = sorted(information_detail.keys())
    for key in keys:
        fout_file.write(str(key)+ "\t" + str(information_detail[key]) + "\n")
    fout_file.close()
