import numpy as np
import scipy.cluster.vq as scv
import matplotlib.pyplot as plt
from matplotlib import cm
import csv
import pandas as pd
import glob
import os.path

import gradcam_extractor as ge

red_count, orange_count, yellow_count, remainder_count = 0, 0, 0, 0

def lacunarity(img, sz):

    global red_count, orange_count, yellow_count, remainder_count

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
                    color_counts(img[k][l])
                    if k == i:
                        if l == j:
                            if color_comparison(img[k][l], img[k][l+1]): count += 1
                            if color_comparison(img[k][l], img[k+1][l]): count += 1
                            if color_comparison(img[k][l], img[k+1][l+1]): count += 1
                        elif l == j+sz-1:
                            if color_comparison(img[k][l], img[k][l-1]): count += 1
                            if color_comparison(img[k][l], img[k+1][l-1]): count += 1
                            if color_comparison(img[k][l], img[k+1][l]): count += 1
                        elif sz > 2:
                            if color_comparison(img[k][l], img[k][l-1]): count += 1
                            if color_comparison(img[k][l], img[k+1][l-1]): count += 1
                            if color_comparison(img[k][l], img[k+1][l]): count += 1
                            if color_comparison(img[k][l], img[k+1][l+1]): count += 1
                            if color_comparison(img[k][l], img[k][l+1]): count += 1
                    elif k == i+sz-1:
                        if l == j:
                            if color_comparison(img[k][l], img[k-1][l]): count += 1
                            if color_comparison(img[k][l], img[k-1][l+1]): count += 1
                            if color_comparison(img[k][l], img[k][l+1]): count += 1
                        elif l == j+sz-1:
                            if color_comparison(img[k][l], img[k-1][l-1]): count += 1
                            if color_comparison(img[k][l], img[k-1][l]): count += 1
                            if color_comparison(img[k][l], img[k][l-1]): count += 1
                        elif sz > 2:
                            if color_comparison(img[k][l], img[k][l-1]): count += 1
                            if color_comparison(img[k][l], img[k-1][l-1]): count += 1
                            if color_comparison(img[k][l], img[k-1][l]): count += 1
                            if color_comparison(img[k][l], img[k-1][l+1]): count += 1
                            if color_comparison(img[k][l], img[k][l+1]): count += 1
                    elif sz > 2:
                        if l == j:
                            if color_comparison(img[k][l], img[k+1][l]): count += 1
                            if color_comparison(img[k][l], img[k+1][l+1]): count += 1
                            if color_comparison(img[k][l], img[k][l+1]): count += 1
                            if color_comparison(img[k][l], img[k-1][l+1]): count += 1
                            if color_comparison(img[k][l], img[k-1][l]): count += 1
                        elif l == j+sz-1:
                            if color_comparison(img[k][l], img[k+1][l]): count += 1
                            if color_comparison(img[k][l], img[k+1][l-1]): count += 1
                            if color_comparison(img[k][l], img[k][l-1]): count += 1
                            if color_comparison(img[k][l], img[k-1][l-1]): count += 1
                            if color_comparison(img[k][l], img[k-1][l]): count += 1
                        else:
                            if color_comparison(img[k][l], img[k-1][l-1]): count += 1
                            if color_comparison(img[k][l], img[k-1][l]): count += 1
                            if color_comparison(img[k][l], img[k-1][l+1]): count += 1
                            if color_comparison(img[k][l], img[k][l-1]): count += 1
                            if color_comparison(img[k][l], img[k][l+1]): count += 1
                            if color_comparison(img[k][l], img[k+1][l-1]): count += 1
                            if color_comparison(img[k][l], img[k+1][l]): count += 1
                            if color_comparison(img[k][l], img[k+1][l+1]): count += 1

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
    
    # print('\nLacunarity with size {}x{}'.format(sz, sz))
    # print('------------------------------')
    if sz > 2:
        for i in range(0,9):
            # print("Square or pixel in the image with {} different neighbors: {}".format(i, totals[i]))
            mult1 += i * totals[i]
            mult2 += i**2 * totals[i]
        
        m1 = (1/(len(img)*len(img))) * mult1
        m2 = (1/(len(img)*len(img))) * mult2

    else:
        # for j in range(0,5):
        #     if j == 0:
        #         print("Squares(set of 4 pixels in the image) with {} different neighbors: {}".format(j, totals[j]))
        #     else:
        #         print("Squares(set of 4 pixels in the image) with {} different neighbors: {}".format((j+1)*2+2, totals[j]))
        m1 = (1/(len(img)*len(img)/4)) * (0 * totals[0] + 6 * totals[1] + 8 * totals[2] + 10 * totals[3] + 12 * totals[4])
        m2 = (1/(len(img)*len(img)/4)) * (0**2 * totals[0] + 6**2 * totals[1] + 8**2 * totals[2] + 10**2 * totals[3] + 12**2 * totals[4])
    
    if m1 == 0:
        lacunarity = m2
    elif m2 == 0:
        lacunarity = 0
    else:
        lacunarity = m2/m1**2

    return lacunarity


def color_comparison(main, neighbor):

    if main >= 0.86:
        if neighbor < 0.86: return True
        else: return False
    elif main < 0.86 and main >= 0.75:
        if neighbor >= 0.86 or neighbor < 0.75: return True
        else: return False
    elif main < 0.75 and main >= 0.55:
        if neighbor >= 0.75 or neighbor < 0.55: return True
        else: return False
    else:
        if neighbor >= 0.55: return True
        else: return False


def color_counts(main):
    global red_count, orange_count, yellow_count, remainder_count

    if main >= 0.86:
        red_count += 1
    elif main < 0.86 and main >= 0.75:
        orange_count += 1
    elif main < 0.75 and main >= 0.55:
        yellow_count += 1
    else:
        remainder_count += 1


def empty_globals():
    global red_count, orange_count, yellow_count, remainder_count
    red_count, orange_count, yellow_count, remainder_count = 0, 0, 0, 0


# red >= 0.86
# 0.86 > orange >= 0.75
# 0.75 > yellow >= 0.55


def colormap2arr(arr,cmap):    
    # http://stackoverflow.com/questions/3720840/how-to-reverse-color-map-image-to-scalar-values/3722674#3722674
    gradient=cmap(np.linspace(0.0,1.0,100))

    # Reshape arr to something like (240*240, 4), all the 4-tuples in a long list...
    arr2=arr.reshape((arr.shape[0]*arr.shape[1],arr.shape[2]))
    
    # CHANGED: The image does not bring the alpha value and for this function it is needed
    ones = np.ones(arr.shape[0]*arr.shape[1])
    arr2 = np.column_stack((arr2, ones))

    # Use vector quantization to shift the values in arr2 to the nearest point in
    # the code book (gradient).
    code,dist=scv.vq(arr2,gradient)

    # code is an array of length arr2 (240*240), holding the code book index for
    # each observation. (arr2 are the "observations".)
    # Scale the values so they are from 0 to 1.
    values=code.astype('float')/gradient.shape[0]

    # Reshape values back to (240,240)
    values=values.reshape(arr.shape[0],arr.shape[1])
    values=values[::-1]
    return values


if __name__ == '__main__':
    ge.gradcam_extractor()

    csv_files = glob.glob(os.path.join('./results/', '*.csv'))
    
    for name in csv_files:
        col_list = ["Image", "Label", "Layer", "Prediction", "Heatmap", "Success"]
        df = pd.read_csv("./results/{}".format(name[10:]), usecols=col_list)
        ind = 0
        header = False
        for heatmap in df["Heatmap"]:
            with open('results/Lacunarity_study_{}'.format(name[10:]), 'a', newline='') as file:
                writer = csv.writer(file)

                if type(heatmap) == str:
                    colors = plt.imread('./results/{}/heatmaps/{}'.format(name[10:-4], heatmap))
                    print('Image {} processed!'.format(heatmap))
                    example=colormap2arr(colors, cm.jet)

                    lacu2 = lacunarity(example, 2)
                    lacu4 = lacunarity(example, 4)
                    empty_globals()
                    lacu8 = lacunarity(example, 8)
                
                    pix_sum = red_count + orange_count + yellow_count + remainder_count

                    lacu2 = str(lacu2).replace('.', ',')
                    lacu4 = str(lacu4).replace('.', ',')
                    lacu8 = str(lacu8).replace('.', ',')
                    pix_sum = str(pix_sum).replace('.', ',')
                    red_pixels = str(red_count).replace('.', ',')
                    orange_pixels = str(orange_count).replace('.', ',')
                    yellow_pixels = str(yellow_count).replace('.', ',')
                    remainder_pixels = str(remainder_count).replace('.', ',')

                    label = heatmap.split("_")[0][4:]
                    prediction = heatmap.split("_")[-1].replace(".png","")

                    if label == prediction:
                        success = True
                    else:
                        success = False


                    if ind == 0 and header is False:
                        header = True
                        writer.writerow(["Image", "Prediction", "2x2 Lacunarity", "4x4 Lacunarity", "8x8 Lacunarity", "Red pixels", "Orange pixels", "Yellow pixels", "Remainder pixels", "Pixel sum"])

                    if ind > 0 and ind % 5 == 0:
                        writer.writerow(["\n"])

                    writer.writerow(["{}".format(heatmap), success, lacu2, lacu4, lacu8, red_pixels, orange_pixels, yellow_pixels, remainder_pixels, pix_sum])
                                
                    ind = ind + 1

                else:
                    writer.writerow(["\n"])
                    writer.writerow(["\n"])
                    writer.writerow(["\n"])
                    writer.writerow(["\n"])
            