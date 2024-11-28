#===============================================================================
# Exemplo: Contagem de Arroz
#-------------------------------------------------------------------------------
# Autor: Bogdan T. Nassu
# Aluno: Heitor Derder Trevisol
# Universidade Tecnológica Federal do Paraná
#===============================================================================

import sys, os
import timeit
import numpy as np
import cv2

#===============================================================================

INPUT_FOLDER =  '/home/heitordt/PDI/Trab4'

# TODO: ajuste estes parâmetros!
NEGATIVO = False
THRESHOLD = 0.8
ALTURA_MIN = 10
LARGURA_MIN = 10
N_PIXELS_MIN = 70

#-------------------------------------------------------------------------------

def flood(img, y, x, label, n_pixels, coordinates):

    img[y][x] = label
    if (y < coordinates['T']):
    	coordinates['T'] = y
    if (y > coordinates['B']):
    	coordinates['B'] = y
    if (x < coordinates['L']):
    	coordinates['L'] = x
    if (x > coordinates['R']):
    	coordinates['R'] = x
    n_pixels = n_pixels + 1
    
    if ((x-1) >= 0 and img[y][x-1] == 1):
    	coordinates, n_pixels = flood(img, y, x-1, label, n_pixels, coordinates)
    
    if ((x+1) < img.shape[1] and img[y][x+1] == 1):
    	coordinates, n_pixels = flood(img, y, x+1, label, n_pixels, coordinates)
    
    if ((y-1) >= 0 and img[y-1][x] == 1):
    	coordinates, n_pixels = flood(img, y-1, x, label, n_pixels, coordinates)
    
    if ((y+1) < img.shape[0] and img[y+1][x] == 1):
    	coordinates, n_pixels = flood(img, y+1, x, label, n_pixels, coordinates)
    	
    return(coordinates, n_pixels)
    
#-------------------------------------------------------------------------------

def rotula (img):
    '''Rotulagem usando flood fill. Marca os objetos da imagem com os valores
[0.1,0.2,etc].

Parâmetros: img: imagem de entrada E saída.
            largura_min: descarta componentes com largura menor que esta.
            altura_min: descarta componentes com altura menor que esta.
            n_pixels_min: descarta componentes com menos pixels que isso.

Valor de retorno: uma lista, onde cada item é um vetor associativo (dictionary)
com os seguintes campos:

'label': rótulo do componente.
'n_pixels': número de pixels do componente.
'T', 'L', 'B', 'R': coordenadas do retângulo envolvente de um componente conexo,
respectivamente: topo, esquerda, baixo e direita.'''

    # TODO: escreva esta função.
    # Use a abordagem com flood fill recursivo.
    
    list_components = []
    label = 2
    
    for i in range(img.shape[0]):
    	for j in range(img.shape[1]):
    		if (img[i][j] == 1):
    			coordinates, n_pixels = flood(img, i, j, label, 0, coordinates={'T':i, 'B':i, 'L':j, 'R':j})    			
    			if (n_pixels < N_PIXELS_MIN or (coordinates['B'] - coordinates['T']) < ALTURA_MIN or (coordinates['R'] - coordinates['L']) < LARGURA_MIN):
    				np.where(img == label, 0.0, img)
    			else:
    				arroz = {'label':label, 'T':coordinates['T'], 'B':coordinates['B'], 'L':coordinates['L'], 'R':coordinates['R'], 'n_pixels':n_pixels}
    				list_components.append(arroz)
    				label = label + 1
    
    return(list_components)

def riceEstimator (labels):
    arg = []
    riceCounter = 0
    for x in labels:
    	arg.append(x['n_pixels'])
    arg = sorted(arg)
    median = np.median(arg)
    sigma = np.std(arg)
    if sigma > median/2:
    	median = median - sigma*0.2
    for x in labels:
    	if x['n_pixels'] > median:
    		riceCounter = riceCounter + round(x['n_pixels']/median)
    	else:
    		riceCounter = riceCounter + 1
    
    return riceCounter

def riceCounter (img):

    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.medianBlur(img, 5)
    img = cv2.GaussianBlur(img, (0,0), 1.5)
    img = cv2.normalize(img, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)
    img = cv2.Canny(img, 50, 150)
    
    kernel = np.array([[0, 1, 0],
    			[1, 1, 1],
    			[0, 1, 0]], dtype=np.uint8)
    
    img = cv2.dilate(img, kernel, iterations=1)
    
    filled_img = np.zeros_like(img)
    
    edges, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(filled_img, edges, -1, (255), thickness=cv2.FILLED)
    
    img = img.astype(np.float32)/255.0
    _labels = rotula(img)
    print("____________________________________________")
    return riceEstimator(_labels)

#===============================================================================

def main ():

    _images = []
    for _file in os.listdir(INPUT_FOLDER):
    	if _file.endswith((".png", ".jpeg", ".bmp")):
	    	img = cv2.imread (_file, cv2.IMREAD_COLOR)
    		if img is None:
        		print ('Erro abrindo a imagem.\n')
        		sys.exit ()
    		else:
        		_images.append((img, _file))

    
    for img, _file in _images:
    	target = _file.split('.')[0]
    	img_temp = img.copy()
    	result = riceCounter(img_temp)
    	print("Alvo: %s, Calculado: %s\n" % (target, result))


if __name__ == '__main__':
    main ()

#===============================================================================
