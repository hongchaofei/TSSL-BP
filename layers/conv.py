import math

import torch
import torch.nn as nn
import torch.nn.functional as f
import torch.nn.init as init


class ConvLayer(nn.Conv3d):
    def __init__(self, config, name, in_shape, groups=1):
        self.name = name
        self.type = config['type']
        self.batch_norm = config['batch_norm3d']
        in_features = config['in_channels']
        out_features = config['out_channels']
        kernel_size = config['kernel_size']

        if 'padding' in config:
            padding = config['padding']
        else:
            padding = 0

        if 'stride' in config:
            stride = config['stride']
        else:
            stride = 1

        if 'dilation' in config:
            dilation = config['dilation']
        else:
            dilation = 1

        if 'weight_scale' in config:
            weight_scale = config['weight_scale']
        else:
            weight_scale = 1

        # kernel
        if type(kernel_size) == int:
            kernel = (kernel_size, kernel_size, 1)
        elif len(kernel_size) == 2:
            kernel = (kernel_size[0], kernel_size[1], 1)
        else:
            raise Exception('kernelSize can only be of 1 or 2 dimension. It was: {}'.format(kernel_size.shape))

        # stride
        if type(stride) == int:
            stride = (stride, stride, 1)
        elif len(stride) == 2:
            stride = (stride[0], stride[1], 1)
        else:
            raise Exception('stride can be either int or tuple of size 2. It was: {}'.format(stride.shape))

        # padding
        if type(padding) == int:
            padding = (padding, padding, 0)
        elif len(padding) == 2:
            padding = (padding[0], padding[1], 0)
        else:
            raise Exception('padding can be either int or tuple of size 2. It was: {}'.format(padding.shape))

        # dilation
        if type(dilation) == int:
            dilation = (dilation, dilation, 1)
        elif len(dilation) == 2:
            dilation = (dilation[0], dilation[1], 1)
        else:
            raise Exception('dilation can be either int or tuple of size 2. It was: {}'.format(dilation.shape))

        # groups
        # no need to check for groups. It can only be int

        # print('inChannels :', inChannels)
        # print('outChannels:', outChannels)
        # print('kernel     :', kernel, kernelSize)
        # print('stride     :', stride)
        # print('padding    :', padding)
        # print('dilation   :', dilation)
        # print('groups     :', groups)

        super(ConvLayer, self).__init__(in_features, out_features, kernel, stride, padding, dilation, groups,
                                        bias=True)

        self.weight = torch.nn.Parameter(weight_scale * self.weight, requires_grad=True)
        self.in_shape = in_shape
        self.out_shape = [out_features, int((in_shape[1]+2*padding[0]-kernel[0])/stride[0]+1),
                          int((in_shape[2]+2*padding[1]-kernel[1])/stride[1]+1)]
        print(self.name)
        print(self.in_shape)
        print(self.out_shape)
        print(list(self.weight.shape))
        print("-----------------------------------------")

    def forward(self, x):
        return f.conv3d(x, self.weight, self.bias,
                        self.stride, self.padding, self.dilation, self.groups)

    def get_parameters(self):
        return self.weight
