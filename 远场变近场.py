import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

tablex=pd.read_excel("xdata.xlsx")
tabley=pd.read_excel("ydata.xlsx")
thetax=tabley['thetay'].values.tolist()
thetay=tablex['thetax'].values.tolist()
intensityx=tabley['intensityy'].values.tolist()
intensityy=tablex['intensityx'].values.tolist()
lamuda=450 #nm
level=500
resolution=10

x=[]
y=[]
kx=[]
ky=[]
Ex=[]
Ey=[]
for i in range(len(thetax)):
    thetax[i]=thetax[i]*3.14/180
for i in range(len(thetay)):
    thetay[i]=thetay[i]*3.14/180

for i in range(len(thetax)):
    kx.append(2*3.14*np.sin(thetax[i])/lamuda)
for i in range(len(thetay)):
    ky.append(2*3.14*np.sin(thetay[i])/lamuda)

for i in range(len(thetax)):
    intensityx[i]=np.sqrt(intensityx[i])/np.cos(thetax[i])
for i in range(len(thetay)):
    intensityy[i]=np.sqrt(intensityy[i])/np.cos(thetay[i])

dkx=[(kx[1]-kx[0])/2]
dky=[(ky[1]-ky[0])/2]
for i in range(len(thetax)-2):
    dkx.append((kx[i+2]-kx[i])/2)
for i in range(len(thetay)-2):
    dky.append((ky[i+2]-ky[i])/2)
dkx.append((kx[len(kx)-1]-kx[len(kx)-2])/2)
dky.append((ky[len(ky)-1]-ky[len(ky)-2])/2)

for i in range(2*level):
    x.append(resolution*(i-level))
    y.append(resolution*(i-level))
for i in range(2*level):
    Ex0_real=0
    Ex0_img=0
    Ey0_real=0
    Ey0_img=0
    for j in range(len(kx)):
        Ex0_real=Ex0_real+intensityx[j]*np.sin(kx[j]*x[i])*dkx[j]
        Ex0_img=Ex0_img+intensityx[j]*np.cos(kx[j]*x[i])*dkx[j]
    for j in range(len(ky)):
        Ey0_real=Ey0_real+intensityy[j]*np.sin(ky[j]*y[i])*dky[j]
        Ey0_img=Ey0_img+intensityy[j]*np.cos(ky[j]*y[i])*dky[j]
    Ex.append(np.sqrt(Ex0_real**2+Ex0_img**2))
    Ey.append(np.sqrt(Ey0_real**2+Ey0_img**2))

Exmax=max(Ex)
Eymax=max(Ey)

for i in range(len(Ex)):
    Ex[i]=Ex[i]/Exmax
for i in range(len(Ey)):
    Ey[i]=Ey[i]/Eymax

plt.figure()
plt.plot(Ex,x)
plt.xlabel('intensity')
plt.ylabel('distance (nm)')
plt.show()

plt.figure()
plt.plot(y,Ey)
plt.xlabel('distance (nm)')
plt.ylabel('intensity')
plt.show()

Exy=[]
for i in range(2*level):
    Exy.append([])
    for j in range(2*level):
        Exy[i].append(Ex[i]*Ey[j])

plt.figure(figsize=[7,7])
plt.imshow(Exy, cmap='hot', origin="lower")
plt.xlabel('x (×10 nm)')
plt.ylabel('y (×10 nm)')
plt.show()