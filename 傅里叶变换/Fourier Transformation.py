import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from matrix import matrix
k0=1
N=100
n=100

#导入电场实空间数组
E=matrix('shikongjian.jpg')
'''for i in range(N+1): #test
    E0=[]
    for j in range(N+1):
        E0.append(np.exp(-0.1*np.sqrt((i-N/2)**2+(j-N/2)**2))*np.cos(k0*np.sqrt((i-N/2)**2+(j-N/2)**2)))
    E.append(E0)'''
plt.figure(figsize=[10,10])
plt.imshow(E, cmap='hot', origin='low')
plt.title('Real Space',fontsize=50)
#plt.colorbar(shrink=.83)
plt.xlabel('x',fontsize=30)
plt.ylabel('y',fontsize=30)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)

def changex(temp, position):#放缩坐标
    return round((temp-n/2)*np.pi/(n*k0),2)
def changey(temp, position):
    return round((temp-n/2)*np.pi/(n*k0),2)
kx=[]
ky=[]
for i in range(n+1):
    kx.append(-np.pi*(2*i-n)/n)#最大傅里叶波矢不能超过最小分辨率的倒数
    ky.append(-np.pi*(2*i-n)/n)
Ek=[]
for i in range(n+1):
    Ek0=[]
    for j in range(n+1):
        Ek0.append(0)
    Ek.append(Ek0)
for i in range(n+1):
    for j in range(n+1):
        jifen=0
        kxx=kx[i]
        kyy=ky[j]
        for p in range(N+1):
            for q in range(N+1):
                jifen=jifen+np.sin(kxx*(p-N/2)+kyy*(q-N/2))*E[p][q]
        Ek[i][j]=abs(jifen)
plt.figure(figsize=[10,10])
plt.gca().xaxis.set_major_formatter(FuncFormatter(changex))#放缩坐标
plt.gca().yaxis.set_major_formatter(FuncFormatter(changey))
plt.imshow(Ek, cmap='hot', origin="lower")
plt.title('Fourier Space',fontsize=50)
#plt.colorbar(shrink=.83)
plt.xlabel('kx/k0',fontsize=30)
plt.ylabel('ky/k0',fontsize=30)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
