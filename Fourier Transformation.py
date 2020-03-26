import numpy as np
import matplotlib.pyplot as plt
k0=1/3
N=100
n=100
E=[]
for i in range(N+1):
    E0=[]
    for j in range(N+1):
        E0.append(np.cos(3*k0*np.sqrt((i-N/2)**2+(j-N/2)**2)))
    E.append(E0)
plt.figure(figsize=[10,10])
plt.imshow(E, cmap='hot', origin='low')
plt.colorbar(shrink=.83)
plt.xticks(())
plt.yticks(())
kx=[]
ky=[]
for i in range(n+1):
    kx.append(5*k0*(2*i-n)/n)
    ky.append(5*k0*(2*i-n)/n)
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
                jifen=jifen+np.cos(kxx*(p-N/2)+kyy*(q-N/2))*E[p][q]
        Ek[i][j]=jifen
plt.figure(figsize=[10,10])
plt.imshow(Ek, cmap='hot', origin='low')
plt.colorbar(shrink=.83)
plt.xticks(())
plt.yticks(())