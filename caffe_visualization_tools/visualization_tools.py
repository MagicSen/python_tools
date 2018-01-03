##
# @file visualization_tools.py
# @brief This tools is for caffe model visualization.
# @author Yang Sen, magicys@qq.com
# @version 1.0.0
# @date 2017-01-04
# Copyright(C)
# For free
# All right reserved
# 

import numpy as np
import matplotlib.pyplot as plt
import sys
import caffe
import os
import pylab

# set the plot enviroment
plt.rcParams['figure.figsize'] = (10,10)
plt.rcParams['image.interpolation'] = 'nearest'
plt.rcParams['image.cmap'] = 'gray'

##
# @brief vis_square function which you can preview convolution kernels and the convolution results.
#
# @param data
# @param name
#
# @return 
def vis_square(data, name):
    """Take an array of shape (n, height, width) or (n, height, width, 3)
       and visualize each (height, width) thing in a grid of size approx. sqrt(n) by sqrt(n)"""
    
    # normalize data for display
    data = (data - data.min()) / (data.max() - data.min())
    
    # force the number of filters to be square
    n = int(np.ceil(np.sqrt(data.shape[0])))
    padding = (((0, n ** 2 - data.shape[0]),
               (0, 1), (0, 1))                 # add some space between filters
               + ((0, 0),) * (data.ndim - 3))  # don't pad the last dimension (if there is one)
    data = np.pad(data, padding, mode='constant', constant_values=1)  # pad with ones (white)
    
    # tile the filters into an image
    data = data.reshape((n, n) + data.shape[1:]).transpose((0, 2, 1, 3) + tuple(range(4, data.ndim + 1)))
    data = data.reshape((n * data.shape[1], n * data.shape[3]) + data.shape[4:])
#    pylab.show()    
    plt.figure(name)
    plt.imshow(data); plt.axis('off')


def lookNetDetail(net, layers_name_all=None):
    # Get all layers' name
    if layers_name_all == None:
        layers_name_all = net.params.keys()
    for layer_name in layers_name_all:
        data_shape = net.blobs[layer_name].data.shape
        filter_shape = net.params[layer_name][0].data.shape
        if len(filter_shape) == 2:
            data = net.blobs[layer_name].data[0]
            filter_data = net.params[layer_name][0].data
            #plt.figure(layer_name)
            #plt.imshow(filter_data); plt.axis('off')
            plt.figure(layer_name + "_result")
            plt.plot(data)
            print "========================================="
            print "Layer name: " + layer_name
            print "Layer Shape: " + str(filter_shape)
            print "Data Shape: " + str(data_shape)
            print "========================================="
            pylab.show()    
        elif len(filter_shape) == 4:
            maps_number = data_shape[1]
            data = net.blobs[layer_name].data[0,:maps_number]
            filter_data = net.params[layer_name][0].data
            filter_maps_number = filter_shape[0]
            filter_data = filter_data.transpose(1, 0, 2, 3)[0, :filter_maps_number]
            vis_square(filter_data, layer_name)
            vis_square(data, layer_name+ "_result")
            print "========================================="
            print "Layer name: " + layer_name
            print "Layer Shape: " + str(filter_shape)
            print "Data Shape: " + str(data_shape)
            print "========================================="
            pylab.show()    
        else:
            return

##
# @brief createInputForLayer Create net input from image
#
# @param input_image_path
# @param net_type: ==0[skeleton(1, 2, 96, 96)]
#                  ==1[detection(1, 2, 120, 160)]
# @return 
def createInputForLayer(input_image_path, net_type):
    if not os.path.exists(input_image_path):
        return None
    # Create input image
    image = caffe.io.load_image(input_image_path, color=False)
    print "Input image size: " + str(image.shape)
    if net_type == 0:
        # Flip
        image = np.fliplr(image);
        image_left = image[0:,0:96,0]
        image_right = image[0:,96: , 0]
        image_all = np.zeros([2,96,96])
        image_all[0, :, :] = image_left
        image_all[1, :, :] = image_right
        return image_all
    elif net_type == 1:
        return image
    else:
        return image


    

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print "<caffe_define_prototxt> <caffe_model> <input_image_data>"
        sys.exit()
    model_def = sys.argv[1]
    model_weights = sys.argv[2]
    input_image_path = sys.argv[3]
    if os.path.exists(model_def) and os.path.exists(model_weights):
        print 'Caffe model found.'
    else:
        print 'Cound not find the caffe model.'
        sys.exit()
    # Set running environment
    caffe.set_device(0)
    caffe.set_mode_gpu()
    net = caffe.Net(model_def, model_weights, caffe.TEST)
    # Create input data
    image = createInputForLayer(input_image_path, 0)
    # Show the input data
    for i in range(0, image.shape[0]):
        plt.figure("Image Channels " + str(i))
        plt.imshow(image[i, :]); plt.axis('off')
    pylab.show()    
    # Set the net and run the nets 
    net.blobs['pair_data'].data[0] = image
    net.forward()
    # Set the layer which you want to watch
    layers_name_all = ['ippal', 'fcpal']
    lookNetDetail(net, layers_name_all)

    # Example for change the layer data: "ippal"
    # Change the layer data and rerun
    plt.figure("After Changed ippal")
    conv_str = 'ippal'
    feat = net.blobs[conv_str].data[0]
    feat[3] = 0
    feat[8] = 0
    feat[14] = 0
    feat[166] = 0
    feat[168] = 0
    plt.plot(feat.flat)
    print net.blobs[conv_str].data.shape
    pylab.show()
    # Change the net data
    net.blobs['ippal'].data[0] = feat
    net.forward(None, 'fcpal', 'prob2')
    lookNetDetail(net, layers_name_all)









