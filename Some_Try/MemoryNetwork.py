import torch

# 模拟长时记忆

class EachMemoryLayer(torch.nn.Module):
    def __init__(self,
                 input_size: int,
                 hidden_layer_size: int,
                 ):

        super(EachMemoryLayer, self).__init__()

        self.input_size = input_size
        self.hidden_layer_size = hidden_layer_size

        # 输入 线性解析
        self.LinearLayer1 = torch.nn.Linear(self.input_size, self.hidden_layer_size)
        # 批归一化
        self.RegulationLayer1 = torch.nn.BatchNorm1d(self.hidden_layer_size)
        # 激活函数
        self.ReLU1 = torch.nn.ReLU(inplace=True)

        # 想法是根据前面的神经元的激活情况，来决定是否激活当前神经元
        # 有一个概率 p，来决定是否激活当前神经元 前面输出越大，激活的概率越大
        # 目前搁置该想法

    def forward(self, x):
        x = self.LinearLayer1(x)
        x = self.RegulationLayer1(x)
        x = self.ReLU1(x)
        return x

# 定义一个模型，用于存储记忆


class MemoryNetwork(torch.nn.Module):
    """

    """


    # input 和 我当前接收到的输入一样大
    # 注意这里的记忆网络包含Dropout层，有的神经元会激活，有的神经元没有没激活

    """
    [ Gradient x1,
      Gradient y1,
      NextPoint x1,
      NextPoint y1,
    ]  
    """


    def __init__(self,
                 input_size: int = 4,   # 也是输出的大小，因为 记忆需要反复迭代
                 ):

        super(MemoryNetwork, self).__init__()

        self.input_size: int = input_size


        # 第一层 直接输入
        self.LinearLayer1 = EachMemoryLayer(self.input_size, 64)
        # 第二层
        self.LinearLayer2 = EachMemoryLayer(64, 64)
        # 第三层
        self.LinearLayer3 = EachMemoryLayer(64, 64)

        # 准备输出
        self.LinearLayerOut = torch.nn.Linear(64, self.input_size)

        # 同时看一下是否需要继续查看记忆
        # self.LinearCheckMemory1 = torch.nn.Linear(64, 64)
        # self.LinearCheckMemory2 = torch.nn.Linear(64, 1)
        # self.SigmoidCheckMemory = torch.nn.ReLU(inplace=True)



        # 激活函数
        # self.ReLU6 = torch.nn.ReLU(inplace=True)


    def forward(self, x):

        x = self.LinearLayer1(x)
        x = self.LinearLayer2(x)
        x = self.LinearLayer3(x)
        x = self.LinearLayerOut(x)

        # 检查是否需要继续查看记忆
        # check_result = self.LinearCheckMemory1(x)
        # check_result = self.LinearCheckMemory2(x)
        # check_result = self.SigmoidCheckMemory(x)


        return x





