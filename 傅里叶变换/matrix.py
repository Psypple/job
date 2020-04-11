from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
def matrix(filename):
    img=np.array(Image.open(filename))
    '''plt.figure() #test
    plt.imshow(img)
    plt.axis('off')
    plt.show()'''
    n=img.shape[0]
    img0=[]
    for i in range(n):
        img00=[]
        for j in range(n):
            img00.append(img[i,j][0])
        img0.append(img00)
    return img0