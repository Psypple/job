# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rc("font",family='FangSong')

w=7.5#电极半宽（微米）
l=1000#腔长（微米）
x=[50,100,150,200,252]
y1=[32,32,32,32,33]
y2=[1000/(3000-1750),153/150,150/150,158/150,150/150]

for i in range(5):
    y1[i]=y1[i]/(10*w)
    y2[i]=y2[i]/(l*1e-3)
    
a=15#字体大小
plt.figure(figsize=[9,6])
fig,ax1=plt.subplots()#双y轴
ax2=ax1.twinx()
plt.title('脊形15μm',size=20)
ax1.plot(x,y1,label='阈值电流（kA/cm^2）',color='red')
ax2.plot(x,y2,label='效率(W/A)',color='blue')
ax1.set_xlabel("残余层厚度（nm）",size=a)
ax1.set_ylabel('阈值电流（kA/cm^2）',color='red',size=a)#y轴注释
ax2.set_ylabel('效率(W/A)',color='blue',size=a)
ax1.tick_params(labelsize=a)#坐标轴数字大小
ax2.tick_params(labelsize=a)
#plt.legend(prop=font1)
plt.show()