import torch

# 这是一个GoogLeNet Inception模块

# ##### 暂时用不到

# 基础通用卷积层
class BasicConv2d(torch.nn.Module):

    def __init__(self,
                 in_channels: int,  # 输入通道数
                 out_channels: int, # 输出通道数
                 **kwargs
                 ):
        # 初始化
        super(BasicConv2d, self).__init__()

        # 定义卷积层
        self.conv = torch.nn.Conv2d(in_channels, out_channels, **kwargs)
        # 定义 批归一化 层，映射到一个区间，防止极端值
        self.bn = torch.nn.BatchNorm2d(out_channels)


    def forward(self, x):
        # 前向传播
        # 先卷积
        x = self.conv(x)
        # 再批归一化 加快收敛
        x = self.bn(x)

        # 激活函数
        x = torch.nn.functional.relu(x, inplace=True)

        return x




class InceptionGoogLeNet(torch.nn.Module):


    def __init__(self,
                 in_channels: int,
                 pool_features: int,
                 ):

        super(InceptionGoogLeNet, self).__init__()

        # 1 * 1 卷积层
        self.branch1x1 = BasicConv2d(in_channels, 64, kernel_size=1)

