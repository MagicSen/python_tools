import cv2
import os
import string
import math
import shutil

def get_all_folders(root):
    # derive the first order folders
    folders = os.listdir(root)
    all_folders = []
    # derive sub folders
    for folder in folders:
        if not os.path.isdir(root + folder):
            continue
        sfolders = os.listdir(root + folder)
        for sfolder in sfolders:
            if not os.path.isdir(root + folder + "\\" + sfolder):
                continue
            all_folders.append(root + folder + "\\" + sfolder + "\\")

    return all_folders


# this function fetches all of the images from the server and make lists for the labelers
def fetch_list(root):
    # get all of the folders
    list_folder = get_all_folders(root)

    # count all of the images
    list_images = []
    for f in list_folder:
        files = os.listdir(f)
        for file in files:
            if not file[-5:] == '0.bmp':
                continue
            if not os.path.isfile(f + file[:-5] + "1.bmp"):
                continue
            list_images.append(f + file[:-6])

    # set the number for each text, and skip some images
    skip_step = 4
    num = 2000
    cnt = 0
    list_file = open('lists/0.txt','w')

    for i in range(0,len(list_images),skip_step):
        if cnt % num == 0:
            list_file.close()
            list_file = open('lists/' + str(cnt/num) + ".txt", 'w')
        list_file.writelines(list_images[i] + "\n")
        cnt += 1

    list_file.close()

def uploadFolder(folder_src,folder_des):
    files = os.listdir(folder_src)
    for file in files:
        if file[-3:] == "txt":
            #print folder_src + file + "  " + folder_des + file
            shutil.copyfile(folder_src + file, folder_des + file)
        elif os.path.isdir(folder_src + file):
            uploadFolder(folder_src + file + "\\",folder_des + file + "\\")


def uploadFolders(folder_src,folder_des):
    folders = os.listdir(folder_src)
    for folder in folders:
        if os.path.isdir(folder_src + folder):
            uploadFolder(folder_src + folder + "\\", folder_des + folder + "\\")

def copyFile(ori_list,des_list):
    file = open(ori_list,"r")
    content = file.readlines()
    file.close()
    file = open(des_list,"w")
    for line in content:
        temp = line.strip().split("\\")
        file.writelines(temp[-3] + "\\" + temp[-2] + "\\" + temp[-1] + "\n")
    file.close()

if __name__ == '__main__':
    # root of the data
    root = '\\\\10.0.0.202\\D_Detc_20170228_BJ_Fish_DblHands\\'
    data_root = "F:\\20170228_two_hand\\2017_02_28_0\\"

    # upload the txt
    uploadFolders(data_root,root + "Data\\")
    prefix = "2017_02_28_0"
    if not os.path.isdir(root + "Lists\\" +  prefix):
        os.mkdir(root + "Lists\\" +  prefix)
    ori_list = data_root + "\\list_N.txt"
    des_list = root + "Lists\\" + prefix + "\\list_N.txt"
    copyFile(ori_list,des_list)

    ori_list = data_root + "\\list_E.txt"
    des_list = root + "Lists\\" + prefix + "\\list_E.txt"
    copyFile(ori_list,des_list)

    ori_list = data_root + "\\list_X.txt"
    des_list = root + "Lists\\" + prefix + "\\list_X.txt"
    copyFile(ori_list,des_list)






