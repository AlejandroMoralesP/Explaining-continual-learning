import numpy as np
import random

def lacunarity2(img):
    count = 0
    totals = [0] * 5

    for i in range(0,len(img),2):
        for j in range(0,len(img[0]),2):
            for k in range(i,i+2,1):
                for l in range(j,j+2,1):
                    if k < i+1:
                        if l < j+1:
                            if img[k][l] != img[k][l+1]: count += 1
                            if img[k][l] != img[k+1][l]: count += 1
                            if img[k][l] != img[k+1][l+1]: count += 1
                        else:
                            if img[k][l] != img[k][l-1]: count += 1
                            if img[k][l] != img[k+1][l-1]: count += 1
                            if img[k][l] != img[k+1][l]: count += 1
                    else:
                        if l < j+1:
                            if img[k][l] != img[k-1][l]: count += 1
                            if img[k][l] != img[k-1][l+1]: count += 1
                            if img[k][l] != img[k][l+1]: count += 1
                        else:
                            if img[k][l] != img[k-1][l-1]: count += 1
                            if img[k][l] != img[k-1][l]: count += 1
                            if img[k][l] != img[k][l-1]: count += 1

            print("Square with {} different neighbors".format(count))
            if count == 0:
                totals[0] = totals[0]+1
            elif count == 6:
                totals[1] = totals[1]+1
            elif count == 8:
                totals[2] = totals[2]+1
            elif count == 10:
                totals[3] = totals[3]+1
            elif count == 12:
                totals[4] = totals[4]+1

            count = 0
    
    m1 = (1/(sum( [ len(i) for i in img])/4))  * (0 * totals[0] + 6 * totals[1] + 8 * totals[2] + 10 * totals[3] + 12 * totals[4])
    m2 = (1/(sum( [ len(i) for i in img])/4))  * (0**2 * totals[0] + 6**2 * totals[1] + 8**2 * totals[2] + 10**2 * totals[3] + 12**2 * totals[4])
    
    lacunarity = m2/m1**2
    print(lacunarity)

a = np.zeros(shape=(6,6))

var = 0
for i in range(len(a)):
    for j in range(len(a[0])):
        a[i][j] = random.randint(1,2)
        print(a[i][j])
    
    print("")


lacunarity2(a)


