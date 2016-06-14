# Dip-Project


## 小组成员和分工

赵晟佳	训练模型  
杨凯峪	搭建系统，使用除图像和自然语言之外的特征训练一个baseline模型  
张天成	提取广告文本中的特征  
王呈瑞 	提取图像数据中的特征 


## 第三方依赖 

```
numpy  
scipy  
sklearn  
progressbar    
```


## 文件

```
preprocess.py   #产生数据并保存到./features文件夹  
train.py        #训练线性SVM  
X.pickle        #特征X所有可能的取值组成的有序列表，被用于onehot encoding  
predictions.txt #测试集上的预测结果
```


## 使用方法

1. 将`test5w.data`和`train11w.data`放入`./data`文件夹  
2. 在命令行中执行以下命令：
```
python preprocess.py 
python train.py 
```


## 特征提取

DIP_ad_format.pdf中所述的每个特征`X`在`preprocess.py`中有一个对应的`handle_X`函数，它负责特征`X`的编码。   
我们所提交的baseline模型中所用的特征提取方法几乎全是onehot encodeing，除了以下几处特殊处理： 

```
qq_md5:             不用 
image_url:          不用
page_url:           不用
标题及描述:           不用
category_id:        从MS Excel文档中提取三个层级的category_id，以及这类广告是否被允许出现在一、二、三类广告位上  
year:               根据出生日期计算现在的年龄，并且分到小孩、青年、中年、老年四个类别中  
handle_imp_time:    转化为具体的日期时间后只保留小时  
```


## 性能

使用除图像和自然语言之外的特征训练的线性SVM在训练集上的准确率是`72.5%`在交叉验证中是`70.2%`，在测试集上的准确率也是`70%`左右。