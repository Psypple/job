# -*- coding: utf-8 -*-
"""
Created on Fri Sep 23 10:14:50 2022

@author: psypple
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

'''定义初始参数'''
λ=780E-9
k0=2*np.pi/λ+0j
b=1E-6 #迭代用参数，决定初始步长，太大会导致跳出波导解
δ=1E-10 #迭代用参数
ε=1E-16 #迭代用参数
iter_max=1000 #设置一个最大迭代步数

'''输入折射率和厚度'''
global n,d_m
n=[1+0j,3.38+0j,3.48+0j,3.38+0j,3.46+0j] #折射率，注意这个数组index=0时为空气，index最大时为衬底
d=[500,600,500] #每层厚度（从上往下）
d_m=d #约化为国际标准单位m
for i in range (len(d_m)):
    d_m[i]=d_m[i]/1E9

'''三层波导试探解'''
d_waveguide=600*1E-9 #波导总厚度
n1=3.38 #cladding折射率，注意只要实部
n2=3.48 #波导折射率，注意只要实部
R_square=k0**2*d_waveguide**2/4*(n2**2-n1**2)
x_0=[]
δy_even=[]
δy_odd=[]
for i in range(10000):
    x_0.append(i*np.sqrt(R_square)/10000)
    δy_even.append(abs(np.sqrt(R_square-x_0[i]**2)-x_0[i]*np.tan(x_0[i])))
    δy_odd.append(abs(np.sqrt(R_square-x_0[i]**2)+x_0[i]/np.tan(x_0[i])))
n0=[]
for i in range(9998):
    if δy_even[i+1]<δy_even[i] and δy_even[i+1]<δy_even[i+2]:
        n0.append(np.sqrt(n2**2*k0**2-4*x_0[i+1]**2/d_waveguide**2))
    if δy_odd[i+1]<δy_odd[i] and δy_odd[i+1]<δy_odd[i+2]:
        n0.append(np.sqrt(n2**2*k0**2-4*x_0[i+1]**2/d_waveguide**2))
for i in range(len(n0)):
    n0[i]=n0[i]/k0 #这里n0记录了所有的有效折射率试探解的解析解

'''传递矩阵'''
def mode_profile(β):
    layer_num=len(d)
    γ=[] #γ即生长方向的各层中光场的复波矢
    for i in range(layer_num+2):
        γ.append(np.sqrt(β**2-k0**2*n[i]**2))
    AB=[np.array([1,0])] #A和B为光场通解的系数，AB列表记录了每一层（从0层空气开始）的每一组系数[A,B]
    for i in range(layer_num): #迭代layer_num次后，AB的最后一个组[Az-1,Bz-1]其实是倒数第二层，还没有得到无限衬底的系数
        Ti=np.array([[(1+γ[i]/γ[i+1])*np.exp(γ[i+1]*d_m[i])/2 , (1-γ[i]/γ[i+1])*np.exp(γ[i+1]*d_m[i])/2],
                     [(1-γ[i]/γ[i+1])*np.exp(-γ[i+1]*d_m[i])/2 , (1+γ[i]/γ[i+1])*np.exp(-γ[i+1]*d_m[i])/2]])
        AB_i1=np.dot(Ti,AB[i])
        AB.append(AB_i1)
    Tzmin1=np.array([[(1+γ[layer_num]/γ[layer_num+1])/2 , (1-γ[layer_num]/γ[layer_num+1])/2],
                     [(1-γ[layer_num]/γ[layer_num+1])/2 , (1+γ[layer_num]/γ[layer_num+1])/2]])
    AB.append(np.dot(Tzmin1,AB[-1])) #这里加入的是无限衬底层的系数，但是参考点与前面不同，计算光场时要单独处理
    return AB[layer_num+1][0],AB,γ #输出的第一项是Az，由于设置了A0=0，因此Az=t11用于迭代求解；后两项用于计算光场

'''迭代'''
def downhill(β_init):
    β_iter=[β_init] #记录迭代中的β，最后一项是最终符合收敛条件的β，即解
    t11=abs(mode_profile(β_init)[0])
    t11_0=[t11] #记录迭代中的t11，最后一项是最终符合收敛条件的t11<δ
    δβ=b*t11
    crimdef=0 #这个参数叫做前科值，即上次的δβ过大造成t11迭代没有减小留下记录，下次迭代若成果缩小则消除记录，但当此不减半δβ
    count=0
    while t11>=δ and count<iter_max:
        count=count+1
        β_temp=[] #方便对照四个t11'中哪个是下降最快的解
        t11_1=[] #记录四个试探解的t11的模
        t11_11=mode_profile(β_iter[-1]+δβ)[0]
        t11_12=mode_profile(β_iter[-1]-δβ)[0]
        t11_13=mode_profile(β_iter[-1]+δβ*1j)[0]
        t11_14=mode_profile(β_iter[-1]-δβ*1j)[0]
        t11_1.append(abs(t11_11))
        t11_1.append(abs(t11_12))
        t11_1.append(abs(t11_13))
        t11_1.append(abs(t11_14))
        β_temp.append(β_iter[-1]+δβ)
        β_temp.append(β_iter[-1]-δβ)
        β_temp.append(β_iter[-1]+1j*δβ)
        β_temp.append(β_iter[-1]-1j*δβ)
        if min(t11_1)<t11:
            β_iter.append(β_temp[t11_1.index(min(t11_1))])
            t11=t11_1[t11_1.index(min(t11_1))]
            t11_0.append(t11)
            if crimdef==0:
                δβ=1.1*δβ
            crimdef=0
        else:
            crimdef=1
            if not δβ<ε:
                δβ=0.5*δβ
    if t11>=δ:
        print ('Failed to convert.')
    else:
        print ('Converting succeeds.')
    for i in range (len(β_iter)):
        β_iter[i]=β_iter[i]/k0
    return β_iter,t11_0 #此时输出的是有效折射率

'''主控制脚本'''
def main(neff_0): #主程序要求输入迭代初始的有效折射率，注意初始值非常关键！特别是存在高阶模时
    matrix=downhill(neff_0*k0) #导出迭代步骤数据
    β_final=matrix[0] #迭代过程中有效折射率中间数值
    t11=matrix[1] #迭代过程中t11中间数值
    main_ABγ=mode_profile(β_final[-1]*k0)
    iter_num=[]
    for i in range(len(β_final)):
        iter_num.append(i)
    # plt.figure()
    # plt.plot(iter_num,β_final)
    # plt.xlabel('iter number')
    # plt.ylabel('neff_iter')
    # plt.show()
    plt.figure()
    plt.plot(iter_num,t11)
    plt.xlabel('iter number')
    plt.ylabel('t11_iter')
    plt.yscale('log')
    plt.show()
    return main_ABγ,β_final[-1]

'''主求解程序'''
for q in range(len(n0)):
    ABγ=main(n0[q]) #把解系数导出
    AB=ABγ[0][1]
    A=[]
    B=[]
    γ=ABγ[0][2]
    for i in range(len(n)):
        A.append(AB[i][0])
        B.append(AB[i][1])
    # print ('Az=%e + %e i' %(A[-1].real,A[-1].imag)) #输出t11的值判断精确度
    print ('Bz=%e + %e i' %(B[-1].real,B[-1].imag)) #无限衬底开始处电场强度
    print ('neff=%f + %f i' %(ABγ[1].real,ABγ[1].imag))
    
    '''绘制光场'''
    t=[0] #设置边界点，计算光场
    for i in range(len(d)):
        t.append(t[i]+d[i])
    x=[] #x是坐标，用于绘制光场，单位nm
    E=[] #E是光场
    for i in range(200): #上空气层光场
        x.append(1E-9*(-199+i))
        E.append(np.exp(γ[0]*(i-199)*1E-9))
    for i in range(len(d)): #计算有限厚度层光场
        for k in range(500):
            x.append(t[i]+k*d[i]/500)
            E.append(A[i+1]*np.exp(γ[i+1]*(k*d[i]/500-d[i]))+B[i+1]*np.exp(-γ[i+1]*(k*d[i]/500-d[i])))
    for i in range(1000): #计算无限衬底光场
        x.append(t[-1]+i*1E-9)
        E.append(A[-1]*np.exp(γ[-1]*i*1E-9)+B[-1]*np.exp(-γ[-1]*i*1E-9))
    for i in range(len(x)):
        x[i]=x[i]*1E6
    E_real=[]
    E_imag=[]
    I_modal=[] #复光场的模
    for i in range(len(E)):
        E_real.append(E[i].real)
        E_imag.append(E[i].imag)
        I_modal.append(abs(E[i])**2)
    plt.figure()
    plt.plot(x,I_modal)
    plt.xlabel('Distance (μm)')
    plt.ylabel('Intensity (arb.unit)')
    plt.show()