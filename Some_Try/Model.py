import torch
import MemoryNetwork

# 定义模型
# 1. 继承 torch.nn.Module
# 2. 定义 __init__ 方法
# 3. 定义 forward 方法
# 4. 定义模型参数
# 5. 定义模型结构
#
class MainModel(torch.nn.Module):

    # 默认input 有两个向量
    # 第一个是当前点斜率向量，第二个向量指向下一个点的坐标
    def __init__(self,
                 input_size: int,
                 hidden_size: int,
                 output_size: int
                 ):

        super(MainModel, self).__init__()

        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size


        # 这个两个 LSTM 模仿短期记忆

        # 第一层 使用一个 循环神经网络
        self.rnn_block1 = torch.nn.LSTMCell(input_size=self.input_size,
                                            hidden_size=self.hidden_size,
                                           )

        self.rnn_block2 = torch.nn.LSTMCell(input_size=self.hidden_size,
                                            hidden_size=self.hidden_size,
                                           )


        # 输出层
        self.output = torch.nn.Linear(self.hidden_size, self.output_size)

        # h1 + c1
        self.memory_module = MemoryNetwork.MemoryNetwork(input_size=self.hidden_size * 2)


    def forward(self, x):
        # 传入的x 是一个向量，包含两个向量
        # 第一个是当前点斜率向量，第二个向量指向下一个点的坐标
        # 这里的x 是一个向量，包含两个向量
        # 第一个是当前点斜率向量，第二个向量指向下一个点的坐标
        # x = torch.tensor([1.0, 1.0, 2.0, 2.0])

        h0 = torch.randn(x.size(0), self.hidden_size, dtype=torch.float32)
        c0 = torch.randn(x.size(0), self.hidden_size, dtype=torch.float32)

        # 第一层 LSTM
        h1, c1 = self.rnn_block1(x, (h0, c0))

        # 组合h1 和 c1，线性拼接
        h1_c1 = torch.cat((h1, c1), 1)

        # 传入记忆网络
        h1_c1 = self.memory_module(h1_c1)
        # 分割h1 和 c1
        h1, c1 = torch.split(h1_c1, [self.hidden_size, self.hidden_size], dim=1)

        # 把h1 和 c1 传入第二层 LSTM
        h2, c2 = self.rnn_block2(h1, (h1, c1))

        # 输出层
        output = self.output(h2)

        return output

