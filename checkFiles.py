import sys,os
import GetFolderData
import shutil
import time

def isAvailable(base_name):
    left_image = base_name + "_0.png"
    right_image = base_name + "_1.png"

    left_txt = base_name + "_0.txt"
    right_txt = base_name + "_1.txt"
    if os.path.exists(left_image) and os.path.exists(right_image) and os.path.exists(left_txt) and os.path.exists(right_txt):
        return True
    else:
        return False

def checkTxt(file_name):
    fin = open(file_name, 'r')
    num = 0
    for line in fin:
        if "-1" in line:
            num = num + 1
    if num == 22 or num == 44 or num == 0:
        return False
    else:
        return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "<fin_dir>"
        sys.exit()
    fin_dir = sys.argv[1]
    file_all = GetFolderData.getFileListFromFolder(fin_dir)
    file_base_name = []
    for item in file_all:
        if item[-5:] == "1.png":
            file_base_name.append(item[0:-6])
    total_not_available = 0
    total = 0
    for base_name in file_base_name:
        if isAvailable(base_name):
            total = total + 1
            if checkTxt(base_name + "_0.txt") or checkTxt(base_name + "_1.txt"):
                print base_name
                total_not_available = total_not_available + 1
    print "Total: " + str(total)
    print "Total not available " + str(total_not_available)

