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

def so_fundo(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HLS) 
    back = cv2.imread("fundo.png", cv2.IMREAD_COLOR)
    back = cv2.resize(back, (img.shape[1], img.shape[0]))
    mask = cv2.inRange(hsv, (36, 70, 70), (70, 255,255))
    mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

    fundo_verde = np.where(mask==(255,255,255), img, mask)
    #back = np.where(mask==(255,255,255), back, mask)

    # cv2.imshow("back", back)
    # cv2.waitKey()
    # cv2.destroyAllWindows()  

    return fundo_verde, back

      

def gradiente(img):
    imagegray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    lap = cv2.Laplacian(imagegray, cv2.CV_64F)
    lap = np.uint8(np.absolute(lap))
    return lap
    #cv2.imshow("Laplacian", lap)
    #cv2.waitKey()
    #cv2.destroyAllWindows()


def mistura(img, back, index):
    img_out = img.copy() 
    img_out = cv2.cvtColor(img_out, cv2.COLOR_BGR2HSV)
    back = cv2.cvtColor(back, cv2.COLOR_BGR2HSV)
   
#    grad = grad/255.0
#	Tentativa de remover o verde, não fico legal, talvez não seja isso o que deve ser feito
#    img[:,:,1] = np.where(grad==0, img[:,:,1], 0)
    for iy, y in enumerate(img):
        for ix, x in enumerate(y):
            img_out[iy][ix][0] = (img_out[iy][ix][0]*(1-index[iy][ix])) + back[iy][ix][0]*(index[iy][ix])
    
#    dst = cv2.addWeighted(img, (1.0-grad), back, grad, 0.0)
    img_out = cv2.cvtColor(img_out, cv2.COLOR_HSV2BGR)

    # cv2.imshow("add", img_out)
    # cv2.waitKey()
    # cv2.destroyAllWindows()
    return img_out

def green_index_mask(img):
    hls = cv2.cvtColor(img, cv2.COLOR_BGR2HLS)    
            
    H, L, S = cv2.split(hls)
    mask = np.zeros_like(H, dtype=np.float32)
    mask_h = np.zeros_like(H, dtype=np.float32)
    mask_l = np.zeros_like(L, dtype=np.float32)
    mask_s = np.zeros_like(S, dtype=np.float32)
#===============================================================================            
    peak_green = 60
    peak_lower_bound = peak_green - 30
    peak_upper_bound = peak_green + 30
    ramp_lower_bound = peak_green - 40
    ramp_upper_bound = peak_green + 40   
    
    H_ramp_up = (H >= ramp_lower_bound) & (H < peak_lower_bound)
    mask_h[H_ramp_up] = (H[H_ramp_up] - ramp_lower_bound)/(peak_lower_bound - ramp_lower_bound)
    
    H_peak = (H >= peak_lower_bound) & (H <= peak_upper_bound)
    mask_h[H_peak] = 1.0
    
    H_ramp_down = (H > peak_upper_bound) & (H <= ramp_upper_bound)
    mask_h[H_ramp_down] = (ramp_upper_bound - H[H_ramp_down])/(ramp_upper_bound - peak_upper_bound)      
#===============================================================================    
    sat_threshold = 50
       
    sat_ramp = (S >= (sat_threshold-10)) & (S < sat_threshold)
    mask_s[sat_ramp] = (S[sat_ramp] - (sat_threshold-10))/(sat_threshold - (sat_threshold-10))
    
    sat_peak = (S >= sat_threshold)
    mask_s[sat_peak] = 1.0
#===============================================================================    
    lum_peak_lower_bound = 100
    lum_peak_upper_bound = 180
    lum_ramp_lower_bound = 50
    lum_ramp_upper_bound = 230
    
    
    L_ramp_up = (L >= lum_ramp_lower_bound) & (L < lum_peak_lower_bound)
    mask_l[L_ramp_up] = (L[L_ramp_up] - lum_ramp_lower_bound)/(lum_peak_lower_bound - lum_ramp_lower_bound)
    
    L_peak = (L >= lum_peak_lower_bound) & (L <= lum_peak_upper_bound)
    mask_l[L_peak] = 1.0
    
    L_ramp_down = (L > lum_peak_upper_bound) & (L <= lum_ramp_upper_bound)
    mask_l[L_ramp_down] = (lum_ramp_upper_bound - L[L_ramp_down])/(lum_ramp_upper_bound - lum_peak_upper_bound)    
#===============================================================================    
    mask = mask_h#*mask_l*mask_s

#    mask = cv2.resize(mask, (int(mask.shape[1]*0.7), int(mask.shape[0]*0.7))) 
    # cv2.imshow("green_index", mask)
    # cv2.waitKey()
    # cv2.destroyAllWindows()   
    
    return mask         	
    
    
def greenes(img): #calcula a verdicidade de cada pixel
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HLS)

    back = cv2.imread("fundo.png", cv2.IMREAD_COLOR)
    back = cv2.resize(back, (img.shape[1], img.shape[0]))

    mask = cv2.inRange(hsv, (36, 70, 50), (70, 255,255))
    mask =~ mask
    mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

    res = np.where(mask==(255,255,255), img, back)
    
    #res = cv2.resize(res, (int(res.shape[1]*0.7), int(res.shape[0]*0.7))) 
    # cv2.imshow("hsv", res)
    # cv2.waitKey()
    # cv2.destroyAllWindows()
    return res

def verdisse(img, index):
    kernel = np.array([[1, 1, 1], 
                       [1, 1, 1], 
                       [1, 1, 1]], dtype=np.uint8)
    h = cv2.erode(index, kernel, iterations=1) # para tentar tirar ruido
    h = index - h
    spill = h > 0
    img[spill, 1] = (img[spill,1]*0.5).astype(np.uint8)
    cv2.imshow("verdisse", img)
    cv2.waitKey()
    cv2.destroyAllWindows()
    return img


def main():
    images = open_all_images(INPUT_FOLDER)
    for img, filename in images:
        index = green_index_mask(img)
        #expected = filename.split('.')[0]
        #img = verdisse(img, index)
        #simples = greenes(img)
        # cv2.imwrite("simples/simples"+filename, simples)
        fundo_verde, back = so_fundo(img)
        #grad = gradiente(fundo_verde)
        # cv2.imwrite("gradiente/gradiente"+filename, grad)
        #mist = mistura(simples, back, grad)
        mist = mistura(img, back, index)
        cv2.imwrite("mistura/mistura"+filename, mist)
    
    


if __name__ == "__main__":
    main()
