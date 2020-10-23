# 准备数据
# 搭建网络
# 训练参数
# 全连接网络实现鸢尾花分类
from sklearn import datasets
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

# 加载数据集
x_data = datasets.load_iris().data
y_data = datasets.load_iris().target

# 打乱数据集
np.random.seed(114)
np.random.shuffle(x_data)
np.random.seed((114))
np.random.shuffle(y_data)

# 划分训练集和测试集
x_train = x_data[:-30]
x_test = x_data[-30:]
y_train = y_data[:-30]
y_test = y_data[-30:]

# 转换x的数据类型，否则后面矩阵相乘时会因数据类型不一致报错，原类型为float.64
x_train = tf.cast(x_train, tf.float32)
x_test = tf.cast(x_test, tf.float32)

# 输入和输出配对，并分batch
train_db = tf.data.Dataset.from_tensor_slices((x_train, y_train)).batch(30)
test_db = tf.data.Dataset.from_tensor_slices((x_test, y_test)).batch(30)

# 定义神经网络参数
# 截断正态分布
# 输入结点为4，输出为3
# 用tf.Variable()标记参数可训练
# 使用seed使每次生成的随机数相同
w1 = tf.Variable(tf.random.truncated_normal([4, 3], stddev=0.1, seed=1))
b1 = tf.Variable(tf.random.truncated_normal([3], stddev=0.1, seed=1))

# 一些超参数
lr = 0.1
train_loss_results = []
test_acc = []
epoch = 500
loss_all = 0

for epoch in range(epoch): #数据集级别的循环，每个epoch循环一次数据集
    for step, (x_train, y_train) in enumerate(train_db):#batch级别的循环 ，每个step循环一个batch
        with tf.GradientTape() as tape:  # with结构记录梯度信息
            y = tf.matmul(x_train, w1) + b1 # 正向传播预测
            y = tf.nn.softmax(y) # 使输出y符合概率分布
            y_ = tf.one_hot(y_train, depth=3)  # 将标签值转换为独热码格式，方便计算loss和accuracy
            loss = tf.reduce_mean(tf.square(y_ - y))  # 均方误差损失函数
            loss_all += loss.numpy()

        # 计算参数的偏导数
        grads = tape.gradient(loss, [w1, b1])
        # 更新参数，误差逆向传播
        w1.assign_sub(lr * grads[0])
        b1.assign_sub(lr * grads[1])
    # 每个epoch，打印loss信息
    print("Epoch {}, loss: {}".format(epoch, loss_all / 4))
    train_loss_results.append(loss_all / 4)  # 将4个batch的loss求平均并记录
    loss_all = 0

    # 测试正确率
    total_correct, total_number = 0, 0

    for x_test, y_test in test_db:
        # 使用训练后的参数进行预测
        y = tf.matmul(x_test, w1) + b1
        y = tf.nn.softmax(y)
        # 返回y中最大值的索引，即预测的分类
        pred = tf.argmax(y, axis=1)
        pred = tf.cast(pred, dtype=y_test.dtype)
        correct = tf.cast(tf.equal(pred, y_test), dtype=tf.int32)
        correct = tf.reduce_sum(correct)
        total_correct += int(correct)
        total_number += x_test.shape[0]
    acc = total_correct / total_number
    test_acc.append(acc)
    print("Test_acc:", acc)
    print("--------------------------")

# 绘制 loss 曲线
plt.title('Loss Function Curve')  # 图片标题
plt.xlabel('Epoch')  # x轴变量名称
plt.ylabel('Loss')  # y轴变量名称
plt.plot(train_loss_results, label="$Loss$")  # 逐点画出trian_loss_results值并连线，连线图标是Loss
plt.legend()  # 画出曲线图标
plt.show()  # 画出图像

# 绘制 Accuracy 曲线
plt.title('Acc Curve')  # 图片标题
plt.xlabel('Epoch')  # x轴变量名称
plt.ylabel('Acc')  # y轴变量名称
plt.plot(test_acc, label="$Accuracy$")  # 逐点画出test_acc值并连线，连线图标是Accuracy
plt.legend()
plt.show()
