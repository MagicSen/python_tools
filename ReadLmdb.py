##
# @file ReadLmdb.py
# @brief Read Lmdb image label
# @author Yang Sen, magicys@qq.com
# @version 1.0.0
# @date 2017-07-19

import sys,os
import lmdb,cv2
import caffe
import numpy as np
from matplotlib import pyplot

def returnNormalImageType(image):
    nchannels = image.shape[0]
    height = image.shape[1]
    width = image.shape[2]
    new_image = np.zeros((height, width, nchannels), dtype=np.float32)
    for h in range(0, height):
        for w in range(0, width):
            for c in range(0, nchannels):
                new_image[h][w][c] = image[c][h][w]
    return new_image

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print "<fin_lmdb_dir> <fin_type>" 
        sys.exit()

    env = lmdb.open(sys.argv[1], readonly=True)
    with env.begin() as txn:
        cursor = txn.cursor()
        for key, value in cursor:
            print key, len(value)
            datum = caffe.proto.caffe_pb2.Datum()
            datum.ParseFromString(value)  
            flat_x = np.array(datum.float_data, dtype=np.float32) 
            x = flat_x.reshape(datum.channels, datum.height, datum.width) 
            if sys.argv[2] == "data":
                x = returnNormalImageType(x)
                y = datum.label 
                cv2.imshow("Image", x / 255)
                cv2.waitKey(0)
            else:
                sys.argv[2] = "label"
                p = np.zeros((datum.height, datum.width), dtype=np.float32)
                for i in range(0, datum.channels):
                    p = p + x[i]
                cv2.imshow("Image", p)
                cv2.waitKey(0)

