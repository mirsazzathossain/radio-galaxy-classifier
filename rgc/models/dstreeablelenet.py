"""Steerable Group CNN for Image Classification."""

__author__ = "Mir Sazzat Hossain"

import torch
import torch.nn as nn
import torch.nn.functional as F
from e2cnn import gspaces
from e2cnn import nn as e2nn


class DSteerableLeNet(nn.Module):
    """Steerable CNN for image classification."""

    def __init__(
        self, imsize: int = 151, kernel_size: int = 5, N: int = 16, pre_training: bool = False, num_classes: int = 2
    ) -> None:
        """
        Initialize the network.

        :param imsize: size of the input image
        :type imsize: int
        :param kernel_size: size of the convolutional kernel
        :type kernel_size: int
        :param N: number of rotations
        :type N: int
        :param pre_training: whether to use pre-training or not
        :type pre_training: bool
        :param num_classes: number of classes for classification
        :type num_classes: int
        """
        super().__init__()
        self.imsize = imsize
        self.kernel_size = kernel_size
        self.N = N
        self.pre_training = pre_training

        z = 0.5 * (self.imsize - 2)
        z = int(0.5 * (z - 2))

        self.r2_act = gspaces.FlipRot2dOnR2(self.N)

        in_type = e2nn.FieldType(self.r2_act, [self.r2_act.trivial_repr])
        self.input_type = in_type

        out_type = e2nn.FieldType(self.r2_act, 6 * [self.r2_act.regular_repr])
        self.mask = e2nn.MaskModule(in_type, self.imsize, margin=1)
        self.conv1 = e2nn.R2Conv(in_type, out_type, kernel_size=self.kernel_size, padding=1, bias=False)
        self.relu1 = e2nn.ReLU(out_type, inplace=True)
        self.pool1 = e2nn.PointwiseMaxPoolAntialiased(out_type, kernel_size=2)
        self.drop1 = e2nn.PointwiseDropout(out_type, p=0.5)

        in_type = self.pool1.out_type
        out_type = e2nn.FieldType(self.r2_act, 16 * [self.r2_act.regular_repr])
        self.conv2 = e2nn.R2Conv(in_type, out_type, kernel_size=self.kernel_size, padding=1, bias=False)
        self.relu2 = e2nn.ReLU(out_type, inplace=True)
        self.pool2 = e2nn.PointwiseMaxPoolAntialiased(out_type, kernel_size=2)
        self.drop2 = e2nn.PointwiseDropout(out_type, p=0.5)

        self.gpool = e2nn.GroupPooling(out_type)

        self.fc = nn.Linear(16 * z * z, 2048)
        self.fc1 = nn.Linear(16 * z * z, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, num_classes)
        self.drop = nn.Dropout(p=0.5)

        # dummy parameter for tracking device
        self.dummy = nn.Parameter(torch.empty(0))

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Forward pass of the network.

        :param x: input tensor
        :type x: torch.Tensor
        """
        x = e2nn.GeometricTensor(x, self.input_type)

        x = self.conv1(x)
        x = self.relu1(x)
        x = self.pool1(x)
        x = self.drop1(x)

        x = self.conv2(x)
        x = self.relu2(x)
        x = self.pool2(x)
        x = self.drop2(x)

        x = self.gpool(x)
        x = x.tensor

        x = x.view(x.size()[0], -1)

        if self.pre_training:
            x = self.fc(x)
        else:
            x = F.relu(self.fc1(x))
            x = F.relu(self.fc2(x))
            x = self.drop(x)
            x = self.fc3(x)

        return x
