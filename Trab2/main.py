#===============================================================================
# Exemplo: implementação de filtro da média.
#-------------------------------------------------------------------------------
# Alunos: Heitor Derder Trevisol e Mayara Dal Vesco Hoger
# Universidade Tecnológica Federal do Paraná
#===============================================================================

import sys
import timeit
import numpy as np
import cv2
import math

#===============================================================================

INPUT_IMAGE =  'tom.jpeg'

JANELA = 33
MARGEM = math.floor(JANELA/2)

#===============================================================================

def ingenuo (img_original):
	img = img_original.copy()
	for l_index, linha in enumerate(img_original):
		if l_index < MARGEM or l_index > (len(img) - MARGEM - 1):
			continue
		for c_index, coluna in enumerate(linha):
			if c_index < MARGEM or c_index > (len(linha) - MARGEM - 1):
				img[l_index][c_index] = 0 
				continue
			soma = 0
			for l in range(l_index - MARGEM, l_index + MARGEM+1):
				for c in range(c_index - MARGEM, c_index + MARGEM+1): 
					soma = soma + img_original[l][c]
			media = soma / (JANELA*JANELA)	
			img[l_index][c_index] = media
	return img
	
	
def separavel(img_original):
	img = img_original.copy()
	for l_index, linha in enumerate(img_original):
		for c_index, coluna in enumerate(linha):
			if c_index < MARGEM or c_index > (len(linha) - MARGEM - 1):
				#img[l_index][c_index] = 0 
				continue
			soma = 0
			for c in range(c_index - MARGEM, c_index + MARGEM+1): 
				soma = soma + img_original[l_index][c]
			media = soma / JANELA
			img[l_index][c_index] = media
			
	img2 = img.copy()
	for l_index, linha in enumerate(img):
		if l_index < MARGEM or l_index > (len(img) - MARGEM - 1):
			continue
		for c_index, coluna in enumerate(linha):
			if c_index < MARGEM or c_index > (len(linha) - MARGEM - 1):
				#img2[l_index][c_index] = 0 
				continue
			soma = 0
			for l in range(l_index - MARGEM, l_index + MARGEM+1): 
				soma = soma + img[l][c_index]
			media = soma / JANELA
			img2[l_index][c_index] = media			
	return img2
	
def integral(img_original):
	img_integral = img_original.copy()
	img = img_original.copy()
	for l_index, linha in enumerate(img_integral):
		for c_index, coluna in enumerate(linha):
			soma = img_integral[l_index][c_index]
			flag = 0
			if c_index - 1 >= 0:
				soma = soma + img_integral[l_index][c_index-1]
				flag = flag + 1
			if l_index - 1 >= 0:
				soma = soma + img_integral[l_index - 1][c_index]
				flag = flag + 1
			if flag == 2:
				soma = soma - img_integral[l_index - 1][c_index-1]
			img_integral[l_index][c_index] = soma
	
	for l_index, linha in enumerate(img_integral):
		for c_index, coluna in enumerate(linha):
				if (((l_index + MARGEM) > (len(img) - 1)) and ((c_index + MARGEM) > (len(linha) - 1))):
					soma = img_integral[len(img) - 1][len(linha) - 1]
				elif ((l_index + MARGEM) > (len(img) - 1)):
					soma = img_integral[len(img) - 1][c_index + MARGEM]
				elif ((c_index + MARGEM) > (len(linha) - 1)):
					soma = img_integral[l_index + MARGEM][len(linha) - 1]
				else:
					soma = img_integral[l_index + MARGEM][c_index + MARGEM]
				flag = 0
				if c_index - MARGEM > 0:
					if ((l_index + MARGEM) > (len(img) - 1)):
						soma = soma - img_integral[len(img) - 1][c_index - MARGEM - 1]
					else:
						soma = soma - img_integral[l_index + MARGEM][c_index - MARGEM - 1]
					flag = flag + 1
				if l_index - MARGEM > 0:
					if ((c_index + MARGEM) > (len(linha) - 1)):
						soma = soma - img_integral[l_index - MARGEM - 1][len(linha) - 1]
					else:
						soma = soma - img_integral[l_index - MARGEM - 1][c_index + MARGEM]
					flag = flag + 1			
				if flag == 2:
					soma = soma + img_integral[l_index - MARGEM - 1][c_index - MARGEM - 1]
				media = soma / (JANELA*JANELA)
				img[l_index][c_index] = media
				
	return img

def algoritmo_RGB(func, img_original):
	img = img_original.copy()
	for i in range(0, 3):
		img[:, :, i] =  func(img_original[:, :, i])
	img = (img*255).astype(np.uint8)
	return img, img[MARGEM:-MARGEM, MARGEM:-MARGEM, :]

def verifica_igual(img1, img2):
	flag = False
	if np.array_equal(img1, img2):
		flag = True
	else:
		for x, _ in enumerate(img1):
			for y, _ in enumerate(img1[x]):
				for z, _ in enumerate(img1[x][y]):
					if img1[x][y][z] == img2[x][y][z] or img1[x][y][z]-1 == img2[x][y][z] or img1[x][y][z]+1 == img2[x][y][z]:
						flag = True
					else:
						flag = False
						break
	return flag

#===============================================================================

def main ():

    # Abre a imagem em escala de cinza.
	img = cv2.imread (INPUT_IMAGE, cv2.IMREAD_COLOR)
	if img is None:
		print ('Erro abrindo a imagem.\n')
		sys.exit ()

    # É uma boa prática manter o shape com 3 valores, independente da imagem ser
    # colorida ou não. Também já convertemos para float32.
	img = img.astype (np.float32) / 255.0

	blur = cv2.blur(img,(JANELA,JANELA))
	blur_sem_margem = blur[MARGEM:-MARGEM, MARGEM:-MARGEM, :]
	blur = (blur*255).astype(np.uint8)
	blur_sem_margem = (blur_sem_margem*255).astype(np.uint8)
	cv2.imwrite ('04 - blur.png', blur)
	cv2.imwrite ('14 - blur_sem_margem.png', blur_sem_margem)

	img_ingenuo, img_ingenuo_sem_margem = algoritmo_RGB(ingenuo, img)
	img_separavel, img_separavel_sem_margem = algoritmo_RGB(separavel, img)
	img_integral, img_integral_sem_margem = algoritmo_RGB(integral, img)
    
	cv2.imwrite ('01 - ingenuo.png', img_ingenuo)
	cv2.imwrite ('02 - separavel.png', img_separavel)
	cv2.imwrite ('03 - integral.png', img_integral)

	cv2.imwrite ('11 - img_ingenuo_sem_margem.png', img_ingenuo_sem_margem)
	cv2.imwrite ('12 - img_separavel_sem_margem.png', img_separavel_sem_margem)
	cv2.imwrite ('13 - img_integral_sem_margem.png', img_integral_sem_margem)
      
	if verifica_igual(blur_sem_margem, img_ingenuo_sem_margem):
		print("Algoritmo ingênuo corretamente implementado")
	else:
		print("Algoritmo ingênuo NÃO corretamente implementado")
	if verifica_igual(blur_sem_margem, img_separavel_sem_margem):
		print("Algoritmo separavel corretamente implementado")
	else:
		print("Algoritmo separavel NÃO corretamente implementado")
	if verifica_igual(blur_sem_margem, img_integral_sem_margem):
		print("Algoritmo integral corretamente implementado")
	else: 
		print("Algoritmo integral NÃO corretamente implementado")

	exit()


if __name__ == '__main__':
    main ()

#===============================================================================
