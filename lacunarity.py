import numpy as np

def lacunarity2(img):
    count = 0

    for i in range(0,len(img),2):
        for j in range(0,len(img[0]),2):
            for k in range(i,i+2,1):
                for l in range(j,j+2,1):
                    if img[k][l] == 1:
                        count = count + 1
            print("Cuadrado con {} unos".format(count))
            count = 0
    

a = np.zeros(shape=(6,6))

var = 0
for i in range(len(a)):
    for j in range(len(a[0])):
        if i % 2 == 1:
            var = 1
        else:
            var = 0
        a[i][j] = var


lacunarity2(a)


