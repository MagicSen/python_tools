import cv2
import pygame
from pygame.locals import *
import os
import string
import math

class Preview():
    def __init__(self, screen, sid, list_images,append):
        self.screen = screen
        self.my_font = pygame.font.SysFont(None, 22)
        self.colors = [(0xff, 0x00, 0x00), (0x00, 0xff, 0x00)]
        self.num_pts = 2
        self.pts = [[0 for col in range(2)] for row in range(self.num_pts)]
        self.save_pts = [[0 for col in range(2)] for row in range(self.num_pts)]
        self.files = list_images
        self.curid = sid
        self.focus = 0
        self.image = None
        self.img = None
        self.img_offset = (0, 0)
        self.append = append
        self.load(self.curid)


    def set_id(self,id):
        self.focus = id

    def load(self, id):
        self.focus = 0
        print "File " + str(id) + " : " + self.files[id][0:-4] + self.append +  '.txt'

        while os.path.isfile(self.files[id][0:-4] + self.append +  '.txt'):
            id += 1
            self.curid += 1


        if os.path.isfile(self.files[id][0:-4] + self.append +  '.txt'):
            self.reset()
            self.next_img(False,self.focus,0)
        else:
            img = cv2.imread(self.files[id])
            self.img = cv2.resize(img, (640, 480))
            self.clear_pts()

    def next_img(self,is_save,focus, is_bad):
        self.curid += 1
        if self.curid >= len(self.files):
            self.curid -= 1
            print 'already the last one!!'
        else:
            if is_save is False:
                print self.curid
                self.load(self.curid)
                return
            # save the results
            if focus >= self.num_pts:
                file = open(self.files[self.curid - 1][0:-4] + self.append +  '.txt', 'w')
                if is_bad:
                    file.writelines("2 ")
                else:
                    file.writelines("1 ")
                for i in range(0, self.num_pts):
                    print self.save_pts[i]
                    if i == 0:
                        file.writelines(str(self.save_pts[i][0]) + " " + str(self.save_pts[i][1]) + " ")
                    else:
                        file.writelines(str(self.save_pts[i][0]) + " " + str(self.save_pts[i][1]) + "\n")
                file.close()
                self.load(self.curid)
            else:
                file = open(self.files[self.curid - 1][0:-4] + self.append +  '.txt', 'w')
                file.writelines("0 0 0 0 0\n")
                file.close()
                self.load(self.curid)

    def last_img(self):
        self.curid -= 1
        if self.curid < 0:
            self.curid += 1
            print 'already the first one!!'
        else:
            self.load(self.curid)

    def draw(self,cur_x, cur_y):
        img = self.img.copy()
        for i in range(0, self.num_pts):
            cv2.circle(img, (self.pts[i][0], self.pts[i][1]), 2, self.colors[i], 5)
        line_color = (0xaa, 0xaa, 0xaa)
        x1 = self.pts[0][0]
        y1 = self.pts[0][1]
        x2 = self.pts[1][0]
        y2 = self.pts[1][1]
        w = img.shape[1]
        h = img.shape[0]
        cv2.line(img, (0, cur_y), (w, cur_y), line_color, 1)
        cv2.line(img, (cur_x, 0), (cur_x, h), line_color, 1)

        if x1 > 0 and x2 > 0:
            cv2.rectangle(img, (x1, y1), (x2, y2), (255, 255, 0))
            self.save_pts[0][0] = x1
            self.save_pts[0][1] = y1
            self.save_pts[1][0] = x2
            self.save_pts[1][1] = y2

        img = pygame.image.frombuffer(img.tostring(), (640, 480), "RGB")
        self.screen.blit(img, self.img_offset, (0, 0, 640, 480))

    def click_btn(self, pos, focus):
        pt = (pos[0], pos[1])
        near = -1
        for i in range(0, self.num_pts):
            dis = (pt[0] - self.pts[i][0]) * (pt[0] - self.pts[i][0]) + (pt[1] - self.pts[i][1]) * (
            pt[1] - self.pts[i][1])
            # print dis
            if dis < 8 * 8:
                near = i
                break

        if near == -1:
            if focus >= self.num_pts:
                print "it only support 2 points"
                near = focus + 1
            else:
                near = focus + 1
                self.pts[focus][0] = pos[0] - self.img_offset[0]
                self.pts[focus][1] = pos[1] - self.img_offset[1]
        else:
            focus = near
            self.pts[focus][0] = -10
            self.pts[focus][1] = -10
        return near

    def clear_pts(self):
        self.focus = 0
        for i in range(0, self.num_pts):
            self.pts[i][0] = -10
            self.pts[i][1] = -10

    def reset(self):
        self.focus = 0
        self.image = None
        self.img = None

class LabelingTool():
    def __init__(self,start_id, list_images,append):
        self.screen = pygame.display.set_mode((640, 480))
        pygame.display.set_caption("Labeling Tool")
        self.clock = pygame.time.Clock()
        self.preview = Preview(self.screen, start_id, list_images,append)


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
                    if event.key == 114:  # R
                        self.preview.clear_pts()

                    if event.key == 115:  # S
                        focus = self.preview.focus
                        self.preview.reset()
                        self.preview.next_img(False,focus, 0)

                    if event.key == 120:  # X
                        focus = self.preview.focus
                        self.preview.reset()
                        self.preview.next_img(True,focus, 1)

                    if event.key == 110:  # N
                        focus = self.preview.focus
                        self.preview.reset()
                        self.preview.next_img(True,focus, 0)

                    if event.key == 108:  # L
                        self.preview.reset()
                        self.preview.last_img()


                elif event.type == MOUSEBUTTONDOWN:
                    backid = self.preview.click_btn(event.pos, self.preview.focus)
                    self.preview.set_id(backid)
                elif event.type == MOUSEMOTION:
                    cur_x = (event.pos)[0]
                    cur_y = (event.pos)[1]

            self.preview.draw(cur_x, cur_y)
            pygame.display.update()

def getFiles(folder,list):
    fs = os.listdir(folder)
    for f in fs:
        if os.path.isdir(folder + f):
            list = getFiles(folder + f + "\\", list)
        if f[-3:] == 'bmp':
            list.append(folder + f)
    return list

def generateTmpList(folder):
    list = []
    list = getFiles(folder, list)
    file = open(folder + "tmp_list.txt","w")
    for l in list:
        file.writelines(l + "\n")
    file.close()

def getImages(root):
    images = []
    file = open(root + "tmp_list.txt")
    lines = file.readlines()
    for i in range(0, len(lines)):
        line = lines[i].strip()
        images.append(line)
    return images

cross_a=("                        ",
         "                        ",
         "          XXXX          ",
         "          X..X          ",
         "          X..X          ",
         "          X..X          ",
         "          X..X          ",
         "          X..X          ",
         "          X..X          ",
         "          X..X          ",
         "  XXXXXXXXX..XXXXXXXXX  ",
         "  X..................X  ",
         "  X.........,........X  ",
         "  XXXXXXXXX..XXXXXXXXX  ",
         "          X..X          ",
         "          X..X          ",
         "          X..X          ",
         "          X..X          ",
         "          X..X          ",
         "          X..X          ",
         "          X..X          ",
         "          XXXX          ",
         "                        ",
         "                        ",
        )
no = ("                        ",
         "                        ",
         "         XXXXXX         ",
         "       XX......XX       ",
         "      X..........X      ",
         "     X....XXXX....X     ",
         "    X...XX    XX...X    ",
         "   X.....X      X...X   ",
         "   X..X...X      X..X   ",
         "  X...XX...X     X...X  ",
         "  X..X  X...X     X..X  ",
         "  X..X   X...X    X..X  ",
         "  X..X    X.,.X   X..X  ",
         "  X..X     X...X  X..X  ",
         "  X...X     X...XX...X  ",
         "   X..X      X...X..X   ",
         "   X...X      X.....X   ",
         "    X...XX     X...X    ",
         "     X....XXXXX...X     ",
         "      X..........X      ",
         "       XX......XX       ",
         "         XXXXXX         ",
         "                        ",
         "                        ",
        )

def setCursor(arrow):
    hotspot = None
    for y in range(len(arrow)):
        for x in range(len(arrow[y])):
            if arrow[y][x] in ['x', ',', 'O']:
                hotspot = x,y
                break
        if hotspot != None:
            break
    if hotspot == None:
        raise Exception("No hotspot specified for cursor '%s'!" %
cursorname)
    s2 = []
    for line in arrow:
        s2.append(line.replace('x', 'X').replace(',', '.').replace('O',
'o'))
    cursor, mask = pygame.cursors.compile(s2, 'X', '.', 'o')
    size = len(arrow[0]), len(arrow)
    pygame.mouse.set_cursor(size, hotspot, cursor, mask)


if __name__ == '__main__':
    root = "F:\\Data\\"
    ### step 0 : first build a temporary txt to list all of the images
    # this funciton only needs to run once
    generateTmpList(root)

    ### step 1 : using the tmp list to start labeling
    images = getImages(root)

    ### step 2 : start labeling
    start_pos = 0
    append = "_R"
    pygame.init()
#    pygame.mouse.set_cursor(*pygame.cursors.ball)
    setCursor(cross_a)
    app = LabelingTool(start_pos,images,append)
    app.run()
