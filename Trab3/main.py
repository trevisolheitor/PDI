#===============================================================================
# Exemplo: implementação do efeito bloom
#-------------------------------------------------------------------------------
# Alunos: Guilherme Koller e Heitor Derder Trevisol
# Universidade Tecnológica Federal do Paraná
#===============================================================================

import sys
import timeit
import numpy as np
import cv2
import math

#===============================================================================

INPUT_IMAGE =  'print.jpeg'
THRESHOLD = 0.68

#===============================================================================


#===============================================================================

def main ():

    # Abre a imagem
	img = cv2.imread (INPUT_IMAGE, cv2.IMREAD_COLOR)
	if img is None:
		print ('Erro abrindo a imagem.\n')
		sys.exit ()

    # É uma boa prática manter o shape com 3 valores, independente da imagem ser
    # colorida ou não. Também já convertemos para float32.
	img = img.astype (np.float32) / 255.0
	img_bright_pass = img.copy()
	
	for x, linha in enumerate(img):
		for y, coluna in enumerate(linha):
			flag = 0
			for i in range(0,3):
				if (img[x][y][i] >= THRESHOLD):
					flag = 1
			if (flag == 0):								
				for i in range(0,3):
					img_bright_pass[x][y][i] = 0.0
					
	cv2.imshow("Ori", img)				
	cv2.imshow("BP", img_bright_pass)
	sigma = 2
	gaussian_bloom_mask = cv2.GaussianBlur(img_bright_pass, (0,0), sigma)
	
	for i in range(2, 5):
		name = "i" + str(i)
		gaussian_bloom_mask = gaussian_bloom_mask + cv2.GaussianBlur(img_bright_pass, (0,0), sigma)
		sigma = sigma*2
	
	cv2.imshow("Bloom Gauss Mask", gaussian_bloom_mask)
	img_gaussian_bloom = img*0.9 + gaussian_bloom_mask*0.1
	cv2.imshow("Bloom Gauss", img_gaussian_bloom)
 
	kernel_size = 30
	img_box_blur_mask = cv2.blur(img_bright_pass, (kernel_size, kernel_size))
	for i in range(2,5):
		img_box_blur_mask = img_box_blur_mask + cv2.blur(img_bright_pass, (kernel_size, kernel_size))
	
	img_bloom = img*0.9 + img_box_blur_mask*0.1
	
	cv2.imshow("Bloom Box Mask", img_box_blur_mask)
	cv2.imshow("Bloom Box Blur", img_bloom)
	
	cv2.waitKey()
	exit()
	


if __name__ == '__main__':
    main ()

#===============================================================================
