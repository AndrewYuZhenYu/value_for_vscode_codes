# ==========================================
# 步骤 2：安装和导入库
# (请确保已安装：pip install torch torchvision matplotlib numpy)
# ==========================================
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
import matplotlib.pyplot as plt
import torch.nn.functional as F

# ==========================================
# 步骤 3：设置超参数与固定随机种子
# ==========================================
n_epochs = 3
batch_size_train = 64
batch_size_test = 1000
learning_rate = 0.01
momentum = 0.5
log_interval = 10
random_seed = 1

# 固定随机种子，保证实验结果可复现
torch.manual_seed(random_seed)

# ==========================================
# 步骤 4：数据预处理 + 加载 MNIST 数据集
# ==========================================
# 定义数据处理流程 (转为张量 + 归一化)
transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.1307,), (0.3081,))
])

# 加载训练集
train_loader = DataLoader(
    datasets.MNIST(
        root='./data/', train=True, download=True, transform=transform
    ),
    batch_size=batch_size_train, shuffle=True
)

# 加载测试集
test_loader = DataLoader(
    datasets.MNIST(
        root='./data/', train=False, download=True, transform=transform
    ),
    batch_size=batch_size_test, shuffle=True
)

# ==========================================
# 步骤 5 & 6：查看数据形状与可视化手写数字样本
# ==========================================
examples = enumerate(test_loader)
batch_idx, (example_data, example_targets) = next(examples)

# 打印数据形状和前10个标签
print("数据形状：", example_data.shape)
print("前10个样本标签：", example_targets[:10].numpy())

# 画出前25张图直观查看数据集
plt.figure(figsize=(8,8))
for i in range(25):
    plt.subplot(5,5,i+1)
    plt.tight_layout()
    plt.imshow(example_data[i][0], cmap='gray', interpolation='none')
    plt.title("Label:{}".format(example_targets[i]))
    plt.xticks([])
    plt.yticks([])
plt.show()

# ==========================================
# 步骤 7：搭建 CNN 模型
# ==========================================
class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(1, 10, kernel_size=5)
        self.conv2 = nn.Conv2d(10, 20, kernel_size=5)
        self.conv2_drop = nn.Dropout2d()
        self.fc1 = nn.Linear(320, 50)
        self.fc2 = nn.Linear(50, 10)

    def forward(self, x):
        x = F.relu(F.max_pool2d(self.conv1(x), 2))
        x = F.relu(F.max_pool2d(self.conv2_drop(self.conv2(x)), 2))
        x = x.view(-1, 320)
        x = F.relu(self.fc1(x))
        x = F.dropout(x, training=self.training)
        x = self.fc2(x)
        return F.log_softmax(x, dim=1)

# 初始化模型与优化器
network = Net()
optimizer = optim.SGD(network.parameters(), lr=learning_rate, momentum=momentum)

# ==========================================
# 步骤 8：初始化损失与准确率记录列表
# ==========================================
train_losses = []
train_counter = []
test_losses = []
train_accs = []    # 训练准确率
test_accs = []     # 测试准确率
test_counter = [i * len(train_loader.dataset) for i in range(n_epochs + 1)]

# ==========================================
# 步骤 9：定义训练函数
# ==========================================
def train(epoch):
    network.train()
    train_loss = 0
    correct = 0  # 用来统计正确个数
    total = 0    # 用来统计总样本数
    
    for batch_idx, (data, target) in enumerate(train_loader):
        optimizer.zero_grad()
        output = network(data)
        loss = F.nll_loss(output, target)
        loss.backward()
        optimizer.step()
        
        # 统计损失
        train_loss += loss.item()
        
        # 计算当前 batch 的准确率
        pred = output.data.max(1, keepdim=True)[1]
        correct += pred.eq(target.data.view_as(pred)).sum().item()
        total += target.size(0)
        
        if batch_idx % log_interval == 0:
            accuracy = 100.0 * correct / total
            print('Train Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}\tAccuracy: {:.2f}%'.format(
                epoch, batch_idx * len(data), len(train_loader.dataset),
                100. * batch_idx / len(train_loader), loss.item(), accuracy))
            train_losses.append(loss.item())
            train_accs.append(accuracy)
            train_counter.append(
                (batch_idx * 64) + ((epoch - 1) * len(train_loader.dataset)))
    
    # 保存模型
    torch.save(network.state_dict(), './model.pth')

# ==========================================
# 步骤 10：定义测试函数
# ==========================================
def test():
    network.eval()
    test_loss = 0
    correct = 0
    with torch.no_grad():
        for data, target in test_loader:
            output = network(data)
            test_loss += F.nll_loss(output, target, reduction='sum').item()
            pred = output.data.max(1, keepdim=True)[1]
            correct += pred.eq(target.data.view_as(pred)).sum()
            
    test_loss /= len(test_loader.dataset)
    test_losses.append(test_loss)
    test_acc = 100. * correct / len(test_loader.dataset)
    test_accs.append(test_acc) 
    print('\nTest set: Avg. loss: {:.4f}, Accuracy: {}/{} ({:.2f}%)\n'.format(
        test_loss, correct, len(test_loader.dataset),
        100. * correct / len(test_loader.dataset)))

# ==========================================
# 步骤 11：开始训练与测试
# ==========================================
# 初始测试（未训练前的基准）
test()

# 循环训练3轮
for epoch in range(1, n_epochs + 1):
    train(epoch)
    test()

# ==========================================
# 步骤 12：绘制训练曲线 (Loss 与 Accuracy)
# ==========================================
plt.figure(figsize=(12, 5))  # 设置整体画布大小

# 第一张图： Loss 曲线
plt.subplot(1, 2, 1)
plt.plot(train_counter, train_losses, color='blue')
plt.scatter(test_counter, test_losses, color='red')
plt.legend(['Train Loss', 'Test Loss'], loc='upper right')
plt.xlabel('number of training examples seen')
plt.ylabel('negative log likelihood loss')
plt.title('Train & Test Loss')

# 第二张图： Accuracy 曲线
plt.subplot(1, 2, 2)
plt.plot(train_counter, train_accs, color='green', label='Train Accuracy')
plt.scatter(test_counter, test_accs, color='orange', label='Test Accuracy')
plt.legend(loc='lower right')
plt.xlabel('number of training examples')
plt.ylabel('Accuracy (%)')
plt.title('Train & Test Accuracy')

plt.tight_layout()
plt.show()

# ==========================================
# 步骤 13：可视化模型预测结果
# ==========================================
with torch.no_grad():
    output = network(example_data)
    
plt.figure(figsize=(8,5))
for i in range(6):
    plt.subplot(2,3,i+1)
    plt.tight_layout()
    plt.imshow(example_data[i][0], cmap='gray', interpolation='none')
    plt.title("Prediction: {}".format(
        output.data.max(1, keepdim=True)[1][i].item()))
    plt.xticks([])
    plt.yticks([])
plt.show()