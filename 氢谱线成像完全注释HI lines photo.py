#!/usr/bin/env python
# coding: utf-8

# In[ ]:

#作者：hank、一起去上学、wri
# -*- coding: utf-8 -*-
title='C11\'s Shot'
num=30 #形成20个像素，也是文件的个数，观测点的个数,横排，从左到右
hang=6 #行
lie=5 #列
H21=1420.40575177 #氢谱线频率
c=299792.458 #光速


# In[ ]:


import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


# In[ ]:


tp=np.zeros(num)
# 提前生成元素个数为num的数组，用来记录num个观测文件观测到的信号功率
tip=np.zeros(num) 
# 提前生成元素个数为num的数组，用来num个观测文件的多普勒频移，
# 频移的话可以用来算银河系里氢原子相对我们的运动速度，悬臂成像可能也是用这个数据做的

for i in range(1,num+1): # i从1到num进行循环，即依次对num个文件进行读取
    f1 = np.loadtxt('F:\\RadioAstro\号角\Sagi_Photo\C12\\%d.txt' % i,skiprows=1) 
    # i会取代%d，即为文件的名字为1.txt,2.txt。。。。。
    # loadtxt方法将取读txt文件的内容，生成多维数组，也可视为矩阵，如下所示；skiprows=1为跳过txt第一行，即不取读。
    # 下面左边是频率，右边是信号强度，即取读到的txt文本中的内容
    # [[1.41800000e+03 1.75199500e-02]
    # [1.41800977e+03 1.96757570e-02]
    # [1.41801953e+03 2.03458950e-02]
    # ...
    # [1.42797070e+03 1.79514570e-02]
    # [1.42798047e+03 1.85912490e-02]
    # [1.42799023e+03 1.88292690e-02]]
    
    freq=f1[:,0]
    # f1是一个矩阵，这种写法即读取第0列所有行的内容
    # 读取矩阵的第0列的全部内容，即把所有采样频率取读为一个数组
    power1=f1[:,1]
    # 读取矩阵的第1列的全部内容，即把所有信号强度取读为一个数组
    b=sum(power1[44:214])/170
    #b=sum(power1[94:127])/33
    # b就是背景噪声，看看哪一段没有信号，取个平均当做背景噪声，这里取得是第94个频率点到第127个频率点之间的信号强度平均，因为这一段是底噪
    # 你得打开sdrsharp导出的txt文件，看看有多少行数据，即采样数。可以设置的，就是那个插件中的采样数，有512,1024之类的那个选项
    # 看看哪里的信号比较平滑，可以取个平均做底噪，当然，你也可以自己看个底噪的数值，直接设置一个值
    
    power2=[k-b for k in power1]
    # 就是把power1中的信号强度都减去b这个低噪，只留下信号的净强度
    # 去底噪，由于电压不稳定，频谱会上下起伏，去底噪是为了对齐，即每个频谱都减去自身的底噪，得到没有底噪的频谱
    for j in range(3,len(power2)):#小问题，前三个鬼子无法检测
        if power2[j]-abs(sum(power2[j-3:j-1]))/3>0.00006: #：0.00006
            power2[j]=sum(power2[j-3:j-1])/3
    tp[i-1]=sum(power2[897:1750])
    #tp[i-1]=sum(power2[85:96])
    # 取tp的第i-1个元素来储存一个文件信号的功率
    # 积分，这一段是有信号的区域，你得看看自己的信号集中在第几个采样频率附近，然后积分。
    # 可以涵盖范围宽一些，这样就不会错过有信号的区域
    
    tip[i-1]=(1-H21/freq[power2.index(max(power2[897:1750]))])*c
    #tip[i-1]=(1-H21/freq[power2.index(max(power2[85:96]))])*c
    # 取tp的第i-1个元素来储存一个文件的频移量
    # 取一个文件中的信号最强点，找出它对应的频率，然后算出频移量


# In[ ]:


tp=tp.reshape((hang,lie))
# 把tp这个含有20个元素的数组转为4×5的矩阵
# 该矩阵每一个元素记录了一个文件(一次观测)对应的信号功率
tip=tip.reshape((hang,lie))
# 把tip这个含有20个元素的数组转为4×5的矩阵
# 该矩阵每一个元素记录了一个文件(一次观测)对应的频移量

# 下面就是seaborn，matplotlib库的内容了，可以百度一下，就是用这个库画热图
# 如果不够明显的话，可以用10logP，P为功率，即把功率转为dB的形式再成像
f, (ax1,ax2) = plt.subplots(figsize = (8, 12),nrows=2)
sns.heatmap(tp,ax=ax1,vmin=0.005,vmax=0.03,center=0.03)
ax1.set_title(title,fontsize=58,fontstyle='italic',fontweight='bold')
# 图片的名字
sns.heatmap(tip,ax=ax2,vmin=15,vmax=40,center=40,
            annot=True,annot_kws={'size':14})
f.savefig(title, bbox_inches='tight')
# 图片的名字
# 程序在哪个目录下执行，就生成图片在那个目录下了

