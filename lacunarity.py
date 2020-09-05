import numpy as np
import random


def lacunarity(img, sz):

    count = 0
    if sz == 2:
        totals = [0] * 5
    elif sz > 2:
        totals = [0] * 9
    else:
        print("Size error")

    for i in range(0,len(img),sz):
        for j in range(0,len(img[0]),sz):
            for k in range(i,i+sz,1):
                for l in range(j,j+sz,1):
                    if k == i:
                        if l == j:
                            if img[k][l] != img[k][l+1]: count += 1
                            if img[k][l] != img[k+1][l]: count += 1
                            if img[k][l] != img[k+1][l+1]: count += 1
                        elif l == j+sz-1:
                            if img[k][l] != img[k][l-1]: count += 1
                            if img[k][l] != img[k+1][l-1]: count += 1
                            if img[k][l] != img[k+1][l]: count += 1
                        elif sz > 2:
                            if img[k][l] != img[k][l-1]: count += 1
                            if img[k][l] != img[k+1][l-1]: count += 1
                            if img[k][l] != img[k+1][l]: count += 1
                            if img[k][l] != img[k+1][l+1]: count += 1
                            if img[k][l] != img[k][l+1]: count += 1
                    elif k == i+sz-1:
                        if l == j:
                            if img[k][l] != img[k-1][l]: count += 1
                            if img[k][l] != img[k-1][l+1]: count += 1
                            if img[k][l] != img[k][l+1]: count += 1
                        elif l == j+sz-1:
                            if img[k][l] != img[k-1][l-1]: count += 1
                            if img[k][l] != img[k-1][l]: count += 1
                            if img[k][l] != img[k][l-1]: count += 1
                        elif sz > 2:
                            if img[k][l] != img[k][l-1]: count += 1
                            if img[k][l] != img[k-1][l-1]: count += 1
                            if img[k][l] != img[k-1][l]: count += 1
                            if img[k][l] != img[k-1][l+1]: count += 1
                            if img[k][l] != img[k][l+1]: count += 1
                    elif sz > 2:
                        if l == j:
                            if img[k][l] != img[k+1][l]: count += 1
                            if img[k][l] != img[k+1][l+1]: count += 1
                            if img[k][l] != img[k][l+1]: count += 1
                            if img[k][l] != img[k-1][l+1]: count += 1
                            if img[k][l] != img[k-1][l]: count += 1
                        elif l == j+sz-1:
                            if img[k][l] != img[k+1][l]: count += 1
                            if img[k][l] != img[k+1][l-1]: count += 1
                            if img[k][l] != img[k][l-1]: count += 1
                            if img[k][l] != img[k-1][l-1]: count += 1
                            if img[k][l] != img[k-1][l]: count += 1
                        else:
                            if img[k][l] != img[k-1][l-1]: count += 1
                            if img[k][l] != img[k-1][l]: count += 1
                            if img[k][l] != img[k-1][l+1]: count += 1
                            if img[k][l] != img[k][l-1]: count += 1
                            if img[k][l] != img[k][l+1]: count += 1
                            if img[k][l] != img[k+1][l-1]: count += 1
                            if img[k][l] != img[k+1][l]: count += 1
                            if img[k][l] != img[k+1][l+1]: count += 1

                        if sz > 2:
                            for m in range(0,9):
                                if count == m:
                                    totals[m] = totals[m]+1
                            
                            count = 0
            if sz == 2:
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

    mult1, mult2, m1, m2 = 0, 0, 0, 0

    if sz > 2:
        for i in range(0,9):
            print("Squares with {} different neighbors: {}".format(i, totals[i]))
            mult1 += i * totals[i]
            mult2 += i**2 * totals[i]
        
        m1 = (1/(sum( [ len(i) for i in img])/4)) * mult1
        m2 = (1/(sum( [ len(i) for i in img])/4)) * mult2

    else:
        m1 = (1/(sum( [ len(i) for i in img])/4))  * (0 * totals[0] + 6 * totals[1] + 8 * totals[2] + 10 * totals[3] + 12 * totals[4])
        m2 = (1/(sum( [ len(i) for i in img])/4))  * (0**2 * totals[0] + 6**2 * totals[1] + 8**2 * totals[2] + 10**2 * totals[3] + 12**2 * totals[4])
    
    lacunarity = m2/m1**2
    print(lacunarity)

a = np.zeros(shape=(6,6))

var = 0
for i in range(len(a)):
    for j in range(len(a[0])):
        a[i][j] = random.randint(1,5)
        print(a[i][j])
    
    print("")


lacunarity(a, 2)
lacunarity(a, 3)

