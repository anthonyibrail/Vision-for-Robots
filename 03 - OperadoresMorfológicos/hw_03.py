# -*- coding: utf-8 -*-
"""HW-03.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1uCSY51NVnllv_ysDXW5IlnPDCsX04pWD

# **OPERADORES MORFOLÓGICOS**
"""

import numpy as np                 # Trabaja con arreglos
import matplotlib.pyplot as plt    # Trabaja con visualización de información
import matplotlib.image as mpimg   # Trabaja con apertura/almacenamiento de imágenes
from skimage import color          # Con ayuda de este se convierte la imagen de color a escala de grises
from skimage.morphology import disk, square, diamond, rectangle # Se importan las formas estructurantes

# CONSTANTES
img = mpimg.imread(r'pattern06.bmp')        # Se carga la imagen
opm = ['erode', 'dilate', 'open', 'close']  # Operaciones morfológicas
se = ['line', 'square', 'diamond', 'disk']  # Formas estructurantes
size = 15                                   # Tamaño de la forma estructurante

"""## Funciones de ayuda y chequeo de imagen"""

def show_props(image):  # Muestra propiedades de la imagen
  print("\nimg type: ", type(image))
  print("img shape: ", image.shape)
  print("img size: ", image.size)
  print("img min: ", image.min())
  print("img max: ", image.max())
  print("img mean: ", image.mean())

def show_img(image):    # Muestra imagen
  plt.figure()
  plt.imshow(image, cmap=plt.cm.gray, vmin=0, vmax=image.max())
  plt.axis('off')
  plt.colorbar()

def check_img():  # Checa la imagen si es a color y lo cambia a grises, y lo reescala (0,1) a (0,255)
  global img
  if len(img.shape) > 2:
    show_props(img)
    print("\nSe convierte a escala de grises")
    img = 255*color.rgb2gray(img)

print("IMAGEN ORIGINAL")
show_props(img)
show_img(img)

check_img()
I = img
print("\nDespués de checar")
show_props(I)
show_img(I)

"""## Elementos estructurantes"""

def create_struct_elem(element, size):
    if element == 'line':
        return rectangle(size, 1) # Para este caso es un rectángulo de tamaño size-filas x 1 columna
    elif element == 'square':
        return square(size)
    elif element == 'diamond':
        return diamond(size)
    elif element == 'disk':
        return disk(size)
    else:
        raise ValueError(f"Element type '{element}' not recognized.")

"""## Operaciones morfológicas"""

# Función de erosión con kernel
def erode(img, kernel):
    h, w = img.shape
    kh, kw = kernel.shape
    
    # Obtener el tamaño del borde de ceros necesario para evitar errores en la operación
    pad_height, pad_width = kh//2, kw//2
    
    # Agregar el borde de ceros a la imagen
    padded_img = np.pad(img, ((pad_height, pad_height), (pad_width, pad_width)), mode='constant')
    
    # Crear la matriz de salida
    output = np.zeros((h, w), dtype=np.uint8)
    
    # Recorrer la imagen de entrada
    for i in range(h):
        for j in range(w):
            # Obtener la submatriz centrada en el pixel actual
            sub = padded_img[i:i+kh, j:j+kw]
            # Realiza la operación de erosión
            output[i, j] = np.min(sub[kernel == 1])
            
    return output

# Función de dilatación con kernel
def dilate(img, kernel):
    h, w = img.shape
    kh, kw = kernel.shape

    # Obtener el tamaño del borde de ceros necesario para evitar errores en la operación
    pad_height, pad_width = kh//2, kw//2

    # Agregar el borde de ceros a la imagen
    padded_img = np.pad(img, ((pad_height, pad_height), (pad_width, pad_width)), mode='constant')
    
    # Crear la matriz de salida
    output = np.zeros((h, w), dtype=np.uint8)

    # Recorrer la imagen
    for i in range(h):
        for j in range(w):
            # Obtener la submatriz centrada en el pixel actual
            sub = padded_img[i:i+kh, j:j+kw]
            # Realiza la operación de dilatación
            output[i, j] = np.max(sub[kernel == 1])

    return output

# Función para apertura con kernel
def open(image, kernel):
    eroded = erode(image, kernel)
    dilated = dilate(eroded, kernel)
    return dilated

# Función para cierre con kernel
def close(image, kernel):
    dilated = dilate(image, kernel)
    eroded = erode(dilated, kernel)
    return eroded

def morphoper(image, operation, element, size):
    # Crear el kernel
    kernel = create_struct_elem(element, size)

    # Aplicar la operación morfológica
    if operation == 'erode':
        output = erode(image, kernel)
    elif operation == 'dilate':
        output = dilate(image, kernel)
    elif operation == 'open':
        output = open(image, kernel)
    elif operation == 'close':
        output = close(image, kernel)
    else:
        raise ValueError("Operación morfológica no válida.")

    return output

print("\nAplicando Erosión: ")

Morph1 = morphoper(I, opm[0], se[0], size)
print("\nCon forma estructurante de línea: ")
show_props(Morph1)
show_img(Morph1)
plt.imsave('output_erosion_1.jpg', Morph1, cmap=plt.cm.gray, vmin= Morph1.min(), vmax= Morph1.max())

Morph2 = morphoper(I, opm[0], se[1], size)
print("\nCon forma estructurante de cuadrado: ")
show_props(Morph2)
show_img(Morph2)
plt.imsave('output_erosion_2.jpg', Morph2, cmap=plt.cm.gray, vmin= Morph2.min(), vmax= Morph2.max())

Morph3 = morphoper(I, opm[0], se[2], size)
print("\nCon forma estructurante de diamante: ")
show_props(Morph3)
show_img(Morph3)
plt.imsave('output_erosion_3.jpg', Morph3, cmap=plt.cm.gray, vmin= Morph3.min(), vmax= Morph3.max())

Morph4 = morphoper(I, opm[0], se[3], size)
print("\nCon forma estructurante de disco: ")
show_props(Morph4)
show_img(Morph4)
plt.imsave('output_erosion_4.jpg', Morph4, cmap=plt.cm.gray, vmin= Morph4.min(), vmax= Morph4.max())

print("\nAplicando Dilatación: ")

Morph5 = morphoper(I, opm[1], se[0], size)
print("\nCon forma estructurante de línea: ")
show_props(Morph5)
show_img(Morph5)
plt.imsave('output_dilatacion_1.jpg', Morph5, cmap=plt.cm.gray, vmin= Morph5.min(), vmax= Morph5.max())

Morph6 = morphoper(I, opm[1], se[1], size)
print("\nCon forma estructurante de cuadrado: ")
show_props(Morph6)
show_img(Morph6)
plt.imsave('output_dilatacion_2.jpg', Morph6, cmap=plt.cm.gray, vmin= Morph6.min(), vmax= Morph6.max())

Morph7 = morphoper(I, opm[1], se[2], size)
print("\nCon forma estructurante de diamante: ")
show_props(Morph7)
show_img(Morph7)
plt.imsave('output_dilatacion_3.jpg', Morph7, cmap=plt.cm.gray, vmin= Morph7.min(), vmax= Morph7.max())

Morph8 = morphoper(I, opm[1], se[3], size)
print("\nCon forma estructurante de disco: ")
show_props(Morph8)
show_img(Morph8)
plt.imsave('output_dilatacion_4.jpg', Morph8, cmap=plt.cm.gray, vmin= Morph8.min(), vmax= Morph8.max())

print("\nAplicando Apertura: ")

Morph9 = morphoper(I, opm[2], se[0], size)
print("\nCon forma estructurante de línea: ")
show_props(Morph9)
show_img(Morph9)
plt.imsave('output_apertura_1.jpg', Morph9, cmap=plt.cm.gray, vmin= Morph9.min(), vmax= Morph9.max())

Morph10 = morphoper(I, opm[2], se[1], size)
print("\nCon forma estructurante de cuadrado: ")
show_props(Morph10)
show_img(Morph10)
plt.imsave('output_apertura_2.jpg', Morph10, cmap=plt.cm.gray, vmin= Morph10.min(), vmax= Morph10.max())

Morph11 = morphoper(I, opm[2], se[2], size)
print("\nCon forma estructurante de diamante: ")
show_props(Morph11)
show_img(Morph11)
plt.imsave('output_apertura_3.jpg', Morph11, cmap=plt.cm.gray, vmin= Morph11.min(), vmax= Morph11.max())

Morph12 = morphoper(I, opm[2], se[3], size)
print("\nCon forma estructurante de disco: ")
show_props(Morph12)
show_img(Morph12)
plt.imsave('output_apertura_4.jpg', Morph12, cmap=plt.cm.gray, vmin= Morph12.min(), vmax= Morph12.max())

print("\nAplicando Cierre: ")

Morph13 = morphoper(I, opm[3], se[0], size)
print("\nCon forma estructurante de línea: ")
show_props(Morph13)
show_img(Morph13)
plt.imsave('output_cierre_1.jpg', Morph13, cmap=plt.cm.gray, vmin= Morph13.min(), vmax= Morph13.max())

Morph14 = morphoper(I, opm[3], se[1], size)
print("\nCon forma estructurante de cuadrado: ")
show_props(Morph14)
show_img(Morph14)
plt.imsave('output_cierre_2.jpg', Morph14, cmap=plt.cm.gray, vmin= Morph14.min(), vmax= Morph14.max())

Morph15 = morphoper(I, opm[3], se[2], size)
print("\nCon forma estructurante de diamante: ")
show_props(Morph15)
show_img(Morph15)
plt.imsave('output_cierre_3.jpg', Morph15, cmap=plt.cm.gray, vmin= Morph15.min(), vmax= Morph15.max())

Morph16 = morphoper(I, opm[3], se[3], size)
print("\nCon forma estructurante de disco: ")
show_props(Morph16)
show_img(Morph16)
plt.imsave('output_cierre_4.jpg', Morph16, cmap=plt.cm.gray, vmin= Morph16.min(), vmax= Morph16.max())