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

            print("Box with {} different neighbors".format(count))
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


def lacunaritygreater(img, sz):
    if sz < 3:
        exit()
    
    count = 0
    totals = [0] * 9

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
                        else:
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
                        else:
                            if img[k][l] != img[k][l-1]: count += 1
                            if img[k][l] != img[k-1][l-1]: count += 1
                            if img[k][l] != img[k-1][l]: count += 1
                            if img[k][l] != img[k-1][l+1]: count += 1
                            if img[k][l] != img[k][l+1]: count += 1
                    else:
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

                    for m in range(0,9):
                        if count == m:
                            totals[m] = totals[m]+1

                    count = 0

    mult1 = 0
    mult2 = 0

    for i in range(0,9):
        print("Squares with {} different neighbors: {}".format(i, totals[i]))
        mult1 += i * totals[i]
        mult2 += i**2 * totals[i]

    print("{} {}".format(mult1, mult2))
    m1 = (1/(len(img)*len(img))) * mult1
    m2 = (1/(len(img)*len(img))) * mult2
    
    lacunarity = m2/m1**2
    print(lacunarity)

a = np.zeros(shape=(6,6))

var = 0
for i in range(len(a)):
    for j in range(len(a[0])):
        a[i][j] = random.randint(1,3)
        print(a[i][j])
    
    print("")


lacunaritygreater(a, 3)


