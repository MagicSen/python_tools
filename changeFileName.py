
import os,sys
import shutil

def compareFileName(str1, str2):
    num1 = int(str1.split("_")[1])
    num2 = int(str2.split("_")[1])
    return num1 - num2

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print "<fin_file_list> <fin_begin_time> <fin_out_file>"
        sys.exit()
    fin = open(sys.argv[1], 'r')
    #1496647389586767872
    #1496647396235055104

    #1496647310086767872
    #1496647337086767872
    t_sufix = "14966473"
    t_fix = "86767872"
    begin_time = int(sys.argv[2])
    out_dir = sys.argv[3]
    image_list = []
    for line in fin:
        image_name = line.strip("\n")
        image_list.append(image_name)
    image_list.sort(cmp=compareFileName)
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)

    for i in range(len(image_list)):
        print "Copy " + image_list[i]
        base_name = t_sufix + str(begin_time + i)+ t_fix + image_list[i][-4:]
        shutil.copy(image_list[i], os.path.join(out_dir, base_name))
