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

    # Abre a imagem em escala de cinza.
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
					
					
	cv2.imshow("a", img_bright_pass)
	cv2.waitKey()
	exit()
	
	
"""
	blur = cv2.blur(img,(JANELA,JANELA))
	blur_sem_margem = blur[MARGEM:-MARGEM, MARGEM:-MARGEM, :]
	blur = (blur*255).astype(np.uint8)
	blur_sem_margem = (blur_sem_margem*255).astype(np.uint8)
	cv2.imwrite ('04 - blur.png', blur)
	cv2.imwrite ('14 - blur_sem_margem.png', blur_sem_margem)
    
	cv2.imwrite ('01 - ingenuo.png', img_ingenuo)
	cv2.imwrite ('02 - separavel.png', img_separavel)
	cv2.imwrite ('03 - integral.png', img_integral)

	cv2.imwrite ('11 - img_ingenuo_sem_margem.png', img_ingenuo_sem_margem)
	cv2.imwrite ('12 - img_separavel_sem_margem.png', img_separavel_sem_margem)
	cv2.imwrite ('13 - img_integral_sem_margem.png', img_integral_sem_margem)	"""	      

#	exit()


if __name__ == '__main__':
    main ()

#===============================================================================
