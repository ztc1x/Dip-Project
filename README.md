# Dip-Project


##第三方依赖 

numpy 
scipy 
sklearn 
progressbar  


## 使用方法

首先将`test5w.data`和`train11w.data`放入`./data`文件夹  
 
```
python preprocess.py  #产生数据并保存到./features文件夹，需要运行一小会儿
python train.py
```


## 改变feature

修改每个变量X(DIP_ad_format.pdf中所述)在`preprocess.py`中对应一个`handle_X`函数  