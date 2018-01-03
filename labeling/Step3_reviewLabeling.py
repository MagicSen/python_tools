import cv2
import pygame
from pygame.locals import *
import os
import string
import math

img_width = 640
img_height = 480
ratio = 2

class Preview():
    def __init__(self, screen, sid, list_images,append,list_N,list_E,list_X):
        self.screen = screen
        self.files = list_images
        self.curid = sid
        self.image = None
        self.img = None
        self.append = append
        self.load(self.curid)
        self.list_N = list_N
        self.list_E = list_E
        self.list_X = list_X


    def load(self, id):
        print "File " + str(id) + " : " + self.files[id][0:-4] + self.append +  '.txt'
        if os.path.isfile(self.files[id][0:-4] + self.append +  '.txt'):
            img = cv2.imread(self.files[id])
            labfile = open(self.files[id][0:-4] + self.append +  '.txt','r')
            content = labfile.readlines()
            content = content[0].strip().split(" ")
            x1 = string.atoi(content[1])
            y1 = string.atoi(content[2])
            x2 = string.atoi(content[3])
            y2 = string.atoi(content[4])
            if content[0] == '1':
                cv2.rectangle(img,(x1,y1),(x2,y2),(255,255,0))
            if content[0] == '2':
                cv2.rectangle(img,(x1,y1),(x2,y2),(255,0,255))
            self.img = cv2.resize(img, (img_width * ratio, img_height * ratio))
        else:
            print "No labeling file..."

    def next_img(self,type):
        if type == "N":
            open(self.list_N,"a").writelines(self.files[self.curid][0:-4] + self.append +  '.txt\n')
        if type == "E":
            open(self.list_E,"a").writelines(self.files[self.curid][0:-4] + self.append +  '.txt\n')
        if type == "X":
            open(self.list_X,"a").writelines(self.files[self.curid][0:-4] + self.append +  '.txt\n')

        self.curid += 1
        if self.curid >= len(self.files):
            self.curid -= 1
            print 'already the last one!!'
        else:
            self.load(self.curid)

    def last_img(self):
        self.curid -= 1
        if self.curid < 0:
            self.curid += 1
            print 'already the first one!!'
        else:
            self.load(self.curid)

    def draw(self,cur_x, cur_y):
        img = pygame.image.frombuffer(self.img.tostring(), (img_width * ratio, img_height * ratio), "RGB")
        self.screen.blit(img, [0,0], (0, 0, img_width * ratio, img_height * ratio))

class LabelingTool():
    def __init__(self,start_id, list_images,append,list_N,list_E,list_X):
        self.screen = pygame.display.set_mode((img_width * ratio, img_height * ratio))
        pygame.display.set_caption("Check labeling")
        self.clock = pygame.time.Clock()
        self.preview = Preview(self.screen, start_id, list_images,append,list_N,list_E,list_X)

    def run(self):
        cur_x = 0
        cur_y = 0
        while True:
            self.screen.fill((48, 48, 48))
            # max fps limit
            self.clock.tick(30)
            for event in pygame.event.get():
                if event.type == QUIT:
                    return
                elif event.type == KEYDOWN:
                    print event.key
                    if event.key == 110:  # N, correct labeled
                        self.preview.next_img("N")
                    if event.key == 108:  # L
                        self.preview.last_img()
                    if event.key == 101:  # E, incorrect
                        self.preview.next_img("E")
                    if event.key == 120:  # X
                        self.preview.next_img("X")

            self.preview.draw(cur_x, cur_y)
            pygame.display.update()

def getFilesWithLables(folder,list):
    fs = os.listdir(folder)
    for f in fs:
        if os.path.isdir(folder + f):
            list = getFilesWithLables(folder + f + "\\", list)
        if not f[-3:] == 'png':
            continue
        if not os.path.isfile(folder + f[:-4] + "_L.txt"):
            continue
        if not os.path.isfile(folder + f[:-4] + "_R.txt"):
            continue
        list.append(folder + f)
    return list

def generateTmpList(folder):
    list = []
    list = getFilesWithLables(folder, list)
    file = open(folder + "tmp_labeled_list.txt","w")
    for l in list:
        file.writelines(l + "\n")
    file.close()

def getImages(root,filter1,filter2):
    images = []
    file = open(root + "tmp_labeled_list.txt")
    lines = file.readlines()
    for i in range(0, len(lines)):
        line = lines[i].strip()
        labelfile = open(line[:-4] + filter1 + ".txt","r")
        content = labelfile.readlines()
        content = content[0].strip().split(" ")
        if not content[0] == filter2:
            continue
        labelfile.close()
        images.append(line)
    return images

if __name__ == '__main__':
    root = "F:\\20170228_two_hand\\2017_02_28_0\\"
    ### step 0 : first build a temporary txt to list all of the images
    # this funciton only needs to run once
    generateTmpList(root)

    ### step 1 : using the tmp list to start labeling
    filter1 = "_L"
    filter2 = "1" # 0: not exists, 1: N 2: X
    list_N = root + "list_N.txt" # correct labeled
    list_E = root + "list_E.txt" # incorrect labeled
    list_X = root + "list_X.txt" # maybe correct labeled
    images = getImages(root,filter1,filter2)

    if len(images) < 1:
        print "No valid images..."
    else:
        ### step 2 : start labeling
        start_pos = 0

        pygame.init()
        app = LabelingTool(start_pos,images,filter1,list_N,list_E,list_X)
        app.run()
