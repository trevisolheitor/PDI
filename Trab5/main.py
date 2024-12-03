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
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
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

      

def gradinete(img):
    imagegray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    lap = cv2.Laplacian(imagegray, cv2.CV_64F)
    lap = np.uint8(np.absolute(lap))
    return lap
    cv2.imshow("Laplacian", lap)
    cv2.waitKey()
    cv2.destroyAllWindows()


def mistura(img, back, grad):
    img_out = img.copy()
    grad = grad/255.0

    for iy, y in enumerate(img):
        for ix, x in enumerate(y):
            for ic, c in enumerate(x):
            
                img_out[iy][ix][ic] = (img[iy][ix][ic]*(1-grad[iy][ix])) + back[iy][ix][ic]*(grad[iy][ix])
    
    return img_out
#    dst = cv2.addWeighted(img, (1.0-grad), back, grad, 0.0)
    cv2.imshow("add", img_out)
    cv2.waitKey()
    cv2.destroyAllWindows()



def greenes(img): #calcula a verdicidade de cada pixel
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

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

def verdisse(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    h = h.astype(float)
    for y, valueY in enumerate(h):
        for x, valueX in enumerate(valueY):
            if valueX in range(50, 70): #range de verde
                h[y][x] = (valueX - 60) / 20.0
            else:
                h[y][x] = 1
    kernel = np.array([[0, 1, 0], 
                       [1, 1, 1], 
                       [0, 1, 0]], dtype=np.uint8)
    h = cv2.dilate(h, kernel, iterations=1) # para tentar tirar ruido
    cv2.imshow("verdisse", h)
    cv2.waitKey()
    cv2.destroyAllWindows()


def main():
    images = open_all_images(INPUT_FOLDER)
    for img, filename in images:
        expected = filename.split('.')[0]
        verdisse(img)
        # simples = greenes(img)
        # cv2.imwrite("simples/simples"+filename, simples)
        # fundo_verde, back = so_fundo(img)
        # grad = gradinete(fundo_verde)
        # cv2.imwrite("gradiente/gradiente"+filename, grad)
        # mist = mistura(simples, back, grad)
        # cv2.imwrite("mistura/mistura"+filename, mist)
    
    


if __name__ == "__main__":
    main()