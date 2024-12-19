#===============================================================================
# Exemplo: Chroma Key
#-------------------------------------------------------------------------------
# Autor: Bogdan T. Nassu
# Aluno: Heitor Derder Trevisol e Mayara Dal Vesco Hoger
# Universidade Tecnológica Federal do Paraná
#===============================================================================

import sys
import numpy as np
import cv2
import math
import os

INPUT_FOLDER = "img"

def open_all_images(folder):
    images = []
    for filename in os.listdir(folder):
        if filename.endswith(".png") or filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".bmp"):
            img_path = os.path.join(folder, filename)
            img = open_image(img_path)
            if img is not None:
                images.append((img, filename))
    return images

def open_image(img_name):
    img = cv2.imread (img_name, cv2.IMREAD_COLOR)
    if img is None:
        print ('Erro abrindo a imagem.\n')
        sys.exit ()
    return img#.astype (np.float32) / 255.0

def fundo(img):
    back = cv2.imread("fundo.png", cv2.IMREAD_COLOR)
    back = cv2.resize(back, (img.shape[1], img.shape[0]))

    return back

def mistura(img, back, index):
    img_out = img.copy() 
    img_out = cv2.cvtColor(img_out, cv2.COLOR_BGR2HLS)
    back = cv2.cvtColor(back, cv2.COLOR_BGR2HLS)
   
    for iy, y in enumerate(img):
        for ix, x in enumerate(y):
            if index[iy][ix] != 0:
                img_out[iy][ix][0] = (img_out[iy][ix][0]*(1-(index[iy][ix]))) + back[iy][ix][0]*(index[iy][ix])
    
    img_out = cv2.cvtColor(img_out, cv2.COLOR_HLS2BGR)
    return img_out

def green_index_mask(img):
    hls = cv2.cvtColor(img, cv2.COLOR_BGR2HLS)    
            
    H, _, _ = cv2.split(hls)
    mask_h = np.zeros_like(H, dtype=np.float32)
#===============================================================================            
    peak_green = 60
    peak_lower_bound = peak_green - 25
    peak_upper_bound = peak_green + 25
    ramp_lower_bound = peak_green - 30
    ramp_upper_bound = peak_green + 30   
    
    H_ramp_up = (H >= ramp_lower_bound) & (H < peak_lower_bound)
    mask_h[H_ramp_up] = (H[H_ramp_up] - ramp_lower_bound)/(peak_lower_bound - ramp_lower_bound)
    
    H_peak = (H >= peak_lower_bound) & (H <= peak_upper_bound)
    mask_h[H_peak] = 1.0
    
    H_ramp_down = (H > peak_upper_bound) & (H <= ramp_upper_bound)
    mask_h[H_ramp_down] = (ramp_upper_bound - H[H_ramp_down])/(ramp_upper_bound - peak_upper_bound)      
#===============================================================================       

    #mask = cv2.resize(mask_h, (int(mask_h.shape[1]*0.7), int(mask_h.shape[0]*0.7))) 
    #cv2.imshow("green_index", mask)
    #cv2.waitKey()
    #cv2.destroyAllWindows()   
    
    return mask_h      	

def main():
    images = open_all_images(INPUT_FOLDER)
    for img, filename in images:
        index = green_index_mask(img)
       # back = fundo(img)
        #mist = mistura(img, back, index)
        #cv2.imwrite("mistura/mistura"+filename, mist)

if __name__ == "__main__":
    main()
