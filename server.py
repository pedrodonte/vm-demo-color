# Flask Server for the application
from flask import Flask, request, send_from_directory, url_for
from flask_cors import CORS, cross_origin
from keras.models import load_model
import tensorflow as tf
from keras.models import load_model
from tensorflow import keras
import cv2
import colorsys
import numpy as np
import datetime
import os

app = Flask(__name__)
CORS(app)

CALCOPIRITA = 'Calcopirita'
NEGATIVO = 'Otro'
UMBRAL_OK = 0.5
ARCHIVO_MODELO_ENTRANADO = 'C:\\solaria\\modelo_28noviembre.h5'
DIRECTORIO_IMAGENES = 'C:\\solaria\\imagenes'
ANCHO_ALTO = 180
DIMENSION_PARA_MODELO_H5 = (ANCHO_ALTO, ANCHO_ALTO)
modelo_red_neuronal = load_model(ARCHIVO_MODELO_ENTRANADO)

amarillo_bajo_1 = np.array([7, 70, 0])
amarillo_alto_1 = np.array([180, 255, 255])
amarillo_bajo_2 = np.array([20, 26, 0])
amarillo_alto_2 = np.array([37, 255, 255])
amarillo_bajo_4 = np.array([0, 25, 0])
amarillo_alto_4 = np.array([180, 255, 255])
rangos_amarillos = [[amarillo_bajo_1, amarillo_alto_1], [
    amarillo_bajo_2, amarillo_alto_2], [amarillo_bajo_4, amarillo_alto_4]]

AMARILLO = (0, 255, 255)
VERDE = (0, 255, 0)
ROJO = (0, 0, 255)


def create_id_from_timestamp():
    return str(datetime.datetime.now().timestamp()).replace('.', '')


def grabar_imagen(prefijo, imagen):
    nombre_archivo = '{}_{}.jpg'.format(prefijo, create_id_from_timestamp())
    path_nuevo_archivo = os.path.join(DIRECTORIO_IMAGENES, nombre_archivo)
    cv2.imwrite(path_nuevo_archivo, imagen)
    return nombre_archivo


def extraer_imagen_por_contorno(imagen_entrada, contorno):
    area_total_imagen = imagen_entrada.shape[1] * imagen_entrada.shape[0]
    x, y, w, h = cv2.boundingRect(contorno)
    sub_imagen = imagen_entrada[y:y+h, x:x+w]
    if area_total_imagen > 1000:
        # entonces guardar la imagen
        grabar_imagen('sub_imagen', sub_imagen)
    return sub_imagen


def buscar_contornos(imagen_de_interes):
    contours, hierarchy = cv2.findContours(
        imagen_de_interes, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contours


def dibujar_contornos_segun_color(imagen_url, color_hsv):
    img = cv2.imread(imagen_url)
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv_img, color_hsv[0], color_hsv[1])

    imagen_restada = cv2.bitwise_and(
        img, img, mask=mask)
    imagen_restada = cv2.cvtColor(imagen_restada, cv2.COLOR_BGR2RGB)
    # Aplicar contornos
    contornos = buscar_contornos(mask)
    for contorno in contornos:
        area = cv2.contourArea(contorno)
        if area > 50:
            cv2.drawContours(img, contornos, -1, (100, 0, 100), 3)

    filename = grabar_imagen('resultado', img)

    return filename


def buscar_contornos_amarillos(img, rango_x):
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(
        hsv_img, rangos_amarillos[rango_x][0], rangos_amarillos[rango_x][1])

    imagen_restada = cv2.bitwise_and(
        img, img, mask=mask)
    imagen_restada = cv2.cvtColor(imagen_restada, cv2.COLOR_BGR2RGB)
    # Aplicar contornos

    contornos, jerarquia = cv2.findContours(
        mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return contornos, jerarquia, imagen_restada


def procesar_imagen_amarilla(img, rango_x, aplicar_rn, imprimir_resultados=False):
    area_total_imagen = img.shape[1] * img.shape[0]
    areas_cuarzo_interno = 0
    area_calcopirita = 0
    copia = img.copy()
    contornos, jerarquia, imagen_restada = buscar_contornos_amarillos(
        img, rango_x)
    contornos_padres = []

    for i in range(len(contornos)):
        data = jerarquia[0][i]
        CID = i
        # next = data[0]
        parent = data[3]
        area = cv2.contourArea(contornos[i])
        if parent == -1:
            contornos_padres.append([CID, data, area])

    for i in range(len(contornos)):
        data = jerarquia[0][i]
        CID = i
        next = jerarquia[0][i][0]
        parent = jerarquia[0][i][3]
        area = cv2.contourArea(contornos[i])
        if area > 50:
            if parent == -1:
                if aplicar_rn:
                    sub_img_original = extraer_imagen_por_contorno(
                        imagen_restada, contornos[i])
                    clase, porcentaje = evaluar_img_object(
                        sub_img_original)
                    cv2.drawContours(
                        copia, contornos, CID, AMARILLO, 2)
                    if clase == 'Calcopirita':
                        area_calcopirita += area
                        cv2.drawContours(
                            copia, contornos, CID, VERDE, -1)
                else:
                    area_calcopirita += area
                    cv2.drawContours(copia, contornos, CID, AMARILLO, -1)
            else:
                cv2.drawContours(copia, contornos,
                                 CID, (255, 255, 255), -1)
                areas_cuarzo_interno += area

    area_calcopirita = area_calcopirita - areas_cuarzo_interno
    area_calcopirita = area_calcopirita if area_calcopirita > 0 else 0

    calculo_area = round(area_calcopirita / area_total_imagen * 100, 2)
    ley_cobre = round((area_calcopirita/area_total_imagen)*100*0.34, 2)

    if imprimir_resultados:
        texto = 'Area: {}%'.format(calculo_area)
        texto_ley_cobre = 'Ley de cobre: {}%'.format(ley_cobre)
        cv2.putText(copia, texto, (10, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, ROJO, 4, cv2.LINE_AA)
        cv2.putText(copia, texto_ley_cobre, (10, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, ROJO, 4, cv2.LINE_AA)

    filename = grabar_imagen('resultado', copia)

    return filename, calculo_area, ley_cobre


def metodo_3(imagen_url, aplicar_rn=False):
    img = cv2.imread(imagen_url)
    imagenes_procesadas = []
    for rango_x in range(len(rangos_amarillos)):
        filename, calculo_area, ley_cobre = procesar_imagen_amarilla(
            img, rango_x, aplicar_rn)
        imagenes_procesadas.append(
            [filename, calculo_area, ley_cobre, rango_x])
    return imagenes_procesadas


def evaluar_img_object(img):
    try:
        # resize image
        img = cv2.resize(img, DIMENSION_PARA_MODELO_H5,
                         interpolation=cv2.INTER_AREA)
        img_array = keras.preprocessing.image.img_to_array(img)
        img_array = tf.expand_dims(img_array, 0)  # Create batch axis
        predictions = modelo_red_neuronal.predict(img_array)
        index = np.argmax(predictions)
        porcentaje = 1-round(predictions.item(index), 2)
        clase = CALCOPIRITA if porcentaje > UMBRAL_OK else NEGATIVO

        return clase, '{:.1f}%'.format(porcentaje * 100)
    except Exception as e:
        return str(e), '0%'


@ app.route('/upload-tres', methods=['POST'])
def index_dos():
    links_imagenes = []
    # the data is a multipart/form-data request
    jpg_original = 'original_'+create_id_from_timestamp() + '.jpg'
    path_imagen_original = os.path.join(DIRECTORIO_IMAGENES, jpg_original)

    my_imagen = request.files['myImage']
    my_imagen.save(path_imagen_original)

    imagenes = metodo_3(path_imagen_original, aplicar_rn=False)

    for imagen in imagenes:
        links_imagenes.append(
            {
                'link': url_for('uploaded_file', filename=imagen[0]),
                'area': imagen[1],
                'ley_cobre': imagen[2],
                'opcion_analisis': imagen[3]
            }
        )
    return {
        'message': 'Image uploaded successfully',

        'image_url': '',
        'links_imagenes': links_imagenes,
        'imagen_original': url_for('uploaded_file', filename=jpg_original),
        'jpg_original': jpg_original
    }


@ app.route('/analizar-imagen-rn', methods=['POST'])
def analizar_imagen_con_la_rn():
    try:
        json_data = request.get_json()
        archivo_imagen = json_data['archivo_imagen']
        path_archivo_original = os.path.join(
            DIRECTORIO_IMAGENES, archivo_imagen)
        rango_x = json_data['rango_x']
        img = cv2.imread(path_archivo_original)

        filename, calculo_area, ley_cobre = procesar_imagen_amarilla(
            img, rango_x, True)
        analisis = {
            'link': url_for('uploaded_file', filename=filename),
            'area': calculo_area,
            'ley_cobre': ley_cobre,
            'opcion_analisis': rango_x,
            'imagen_original': url_for('uploaded_file', filename=archivo_imagen),
            'jpg_original': archivo_imagen
        }
        return {
            'mensaje': 'Image uploaded successfully',
            'codigo': 200,
            'analisis': analisis
        }
    except Exception as e:
        return {
            'mensaje': str(e),
            'codigo': 500,
            'analisis': None
        }


@ app.route('/imagen/<filename>')
def uploaded_file(filename):
    return send_from_directory(DIRECTORIO_IMAGENES, filename)


app.run(debug=True, host='0.0.0.0', port=5000)
