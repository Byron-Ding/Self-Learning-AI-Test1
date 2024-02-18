import torch
from torch import nn
from Model import MainModel
from torch.utils.data import DataLoader, Dataset
from torch.autograd import Variable

from FontAnalysis import get_path_pairs

import os

# 定义数据集
class MyDataset(Dataset):
    def __init__(self):
        self.data = get_path_pairs()

    def __getitem__(self, index):
        data = (self.data[index][0], self.data[index][1])
        return data

    def __len__(self):
        return len(self.data)



# 实例化模型6
model = MainModel(input_size=1, hidden_size=64, output_size=1)

# 检查是否有数据集
# 如果有数据集，就加载数据集
if os.path.exists("dataset.pkl"):
    dataset = torch.load("dataset.pkl")
else:
    # 实例化数据集
    dataset = DataLoader(MyDataset(), batch_size=1, shuffle=True)
    # 保存数据集
    torch.save(dataset, "./dataset.pkl")
    print("Save dataset")

# if torch.cuda.is_available():
#     model = model.cuda()

# 定义损失函数
criterion = nn.MSELoss()

# 定义优化器
optimizer = torch.optim.SGD(model.parameters(), lr=0.01)


# model.eval()

model.eval()

eval_loss = 0
eval_acc = 0

# 测试集
for data in dataset:

    font1, font2 = data

    output = []

    for each_path in font1:
        print(each_path)
        each_path = torch.tensor(each_path, dtype=torch.float32).view(4, 1)
        # 一个一个喂给模型
        # if torch.cuda.is_available():
        #     each_path = Variable(each_path).cuda()
        # else:
        each_path = Variable(each_path)

        # 喂给模型
        each_output = model(each_path)


        # 拼接
        output.append(each_output)

    # print(output)

    output = output.view(4, -1)

    font2 = torch.tensor(font2, dtype=torch.float32).view(4, -1)

    # 计算损失
    loss = criterion(output, font2)

    eval_loss += loss.item()


torch.save(model, "model.pkl")
