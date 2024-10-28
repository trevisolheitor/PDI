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

#===============================================================================

def ingenuo (img_original):
	img = img_original.copy()
	for l_index, linha in enumerate(img_original):
		if l_index < math.floor(JANELA/2) or l_index > (len(img) - math.floor(JANELA/2) - 1):
			continue
		for c_index, coluna in enumerate(linha):
			if c_index < math.floor(JANELA/2) or c_index > (len(linha) - math.floor(JANELA/2) - 1):
				img[l_index][c_index] = 0 
				continue
			soma = 0
			for l in range(l_index - math.floor(JANELA/2), l_index + math.floor(JANELA/2)):
				for c in range(c_index - math.floor(JANELA/2), c_index + math.floor(JANELA/2)): 
					soma = soma + img_original[l][c]
			media = soma / (JANELA*JANELA)	
			img[l_index][c_index] = media
	return img
	
	
def separavel(img_original):
	img = img_original.copy()
	for l_index, linha in enumerate(img_original):
		for c_index, coluna in enumerate(linha):
			if c_index < math.floor(JANELA/2) or c_index > (len(linha) - math.floor(JANELA/2) - 1):
				img[l_index][c_index] = 0 
				continue
			soma = 0
			for c in range(c_index - math.floor(JANELA/2), c_index + math.floor(JANELA/2)): 
				soma = soma + img_original[l_index][c]
			media = soma / JANELA
			img[l_index][c_index] = media
			
	for l_index, linha in enumerate(img):
		if l_index < math.floor(JANELA/2) or l_index > (len(img) - math.floor(JANELA/2) - 1):
			continue
		for c_index, coluna in enumerate(linha):
			if c_index < math.floor(JANELA/2) or c_index > (len(linha) - math.floor(JANELA/2) - 1):
				img[l_index][c_index] = 0 
				continue
			soma = 0
			for l in range(l_index - math.floor(JANELA/2), l_index + math.floor(JANELA/2)): 
				soma = soma + img[l][c_index]
			media = soma / JANELA
			img[l_index][c_index] = media			
	return img
	
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
				if (((l_index + math.floor(JANELA/2)) > (len(img) - math.floor(JANELA/2) - 1)) and ((c_index + math.floor(JANELA/2)) > (len(linha) - math.floor(JANELA/2) - 1))):
					soma = img_integral[len(img) - 1][len(linha) - 1]
				elif ((l_index + math.floor(JANELA/2)) > (len(img) - math.floor(JANELA/2) - 1)):
					soma = img_integral[len(img) - 1][c_index + math.floor(JANELA/2)]
				elif ((c_index + math.floor(JANELA/2)) > (len(linha) - math.floor(JANELA/2) - 1)):
					soma = img_integral[l_index + math.floor(JANELA/2)][len(linha) - 1]
				else:
					soma = img_integral[l_index + math.floor(JANELA/2)][c_index + math.floor(JANELA/2)]
				flag = 0
				if c_index - math.floor(JANELA/2) > 0:
					if ((l_index + math.floor(JANELA/2)) > (len(img) - math.floor(JANELA/2) - 1)):
						soma = soma - img_integral[len(img) - 1][c_index - math.floor(JANELA/2) - 1]
					else:
						soma = soma - img_integral[l_index + math.floor(JANELA/2)][c_index - math.floor(JANELA/2) - 1]
					flag = flag + 1
				if l_index - math.floor(JANELA/2) > 0:
					if ((c_index + math.floor(JANELA/2)) > (len(linha) - math.floor(JANELA/2) - 1)):
						soma = soma - img_integral[l_index - math.floor(JANELA/2) - 1][len(linha) - 1]
					else:
						soma = soma - img_integral[l_index - math.floor(JANELA/2) - 1][c_index + math.floor(JANELA/2)]
					flag = flag + 1			
				if flag == 2:
					soma = soma + img_integral[l_index - math.floor(JANELA/2) - 1][c_index - math.floor(JANELA/2) - 1]
				media = soma / (JANELA*JANELA)
				img[l_index][c_index] = media
				
	return img
				
#===============================================================================

def main ():

    # Abre a imagem em escala de cinza.
    img = cv2.imread (INPUT_IMAGE, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print ('Erro abrindo a imagem.\n')
        sys.exit ()

    # É uma boa prática manter o shape com 3 valores, independente da imagem ser
    # colorida ou não. Também já convertemos para float32.
    img = img.reshape ((img.shape [0], img.shape [1], 1))
    img = img.astype (np.float32) / 255
    
    #img_ingenuo = ingenuo(img)
    #img_separavel = separavel(img)
    img_integral = integral(img)

    # Segmenta a imagem.
    #cv2.imshow ('01 - ingenuo', img_ingenuo)
    
    #cv2.imwrite ('01 - ingenuo.png', img_ingenuo*255)
    #cv2.imwrite ('02 - separavel.png', img_separavel*255)
    cv2.imwrite ('03 - integral.png', img_integral*255)
        
    exit()

    start_time = timeit.default_timer ()
    componentes = rotula (img, LARGURA_MIN, ALTURA_MIN, N_PIXELS_MIN)
    n_componentes = len (componentes)
    print ('Tempo: %f' % (timeit.default_timer () - start_time))
    print ('%d componentes detectados.' % n_componentes)

    # Mostra os objetos encontrados.
    for c in componentes:
        cv2.rectangle (img_out, (c ['L'], c ['T']), (c ['R'], c ['B']), (0,0,1))

    cv2.imshow ('02 - out', img_out)
    cv2.imwrite ('02 - out.png', img_out*255)
    cv2.waitKey ()
    cv2.destroyAllWindows ()


if __name__ == '__main__':
    main ()

#===============================================================================
