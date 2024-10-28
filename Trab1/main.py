#===============================================================================
# Exemplo: segmentação de uma imagem em escala de cinza.
#-------------------------------------------------------------------------------
# Autor: Bogdan T. Nassu
# Aluno: Heitor Derder Trevisol
# Universidade Tecnológica Federal do Paraná
#===============================================================================

import sys
import timeit
import numpy as np
import cv2

#===============================================================================

INPUT_IMAGE =  'arroz.bmp'

# TODO: ajuste estes parâmetros!
NEGATIVO = False
THRESHOLD = 0.8
ALTURA_MIN = 10
LARGURA_MIN = 10
N_PIXELS_MIN = 100

#===============================================================================

def binariza (img, threshold):
    ''' Binarização simples por limiarização.

Parâmetros: img: imagem de entrada. Se tiver mais que 1 canal, binariza cada
              canal independentemente.
            threshold: limiar.
            
Valor de retorno: versão binarizada da img_in.'''

    # TODO: escreva o código desta função.
    # Dica/desafio: usando a função np.where, dá para fazer a binarização muito
    # rapidamente, e com apenas uma linha de código!
    
    return np.where(img > threshold, 1.0, 0.0)

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

def rotula (img, largura_min, altura_min, n_pixels_min):
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

    # Mantém uma cópia colorida para desenhar a saída.
    img_out = cv2.cvtColor (img, cv2.COLOR_GRAY2BGR)

    # Segmenta a imagem.
    if NEGATIVO:
        img = 1 - img
    img = binariza (img, THRESHOLD)
    cv2.imshow ('01 - binarizada', img)
    cv2.imwrite ('01 - binarizada.png', img*255)

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
