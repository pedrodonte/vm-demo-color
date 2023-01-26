# Flask Server for the application
from flask import Flask, request, send_from_directory, url_for
from flask_cors import CORS, cross_origin
import cv2
import colorsys
import numpy as np
import datetime

app = Flask(__name__)
CORS(app)


def create_id_from_timestamp():
    return str(datetime.datetime.now().timestamp()).replace('.', '')


def convert_rgb_to_hsv(rgb_string_with_comas):

    # rgb normal: range (0-255, 0-255, 0.255)
    red = int(rgb_string_with_comas.split(',')[0])
    green = int(rgb_string_with_comas.split(',')[1])
    blue = int(rgb_string_with_comas.split(',')[2])

    # get rgb percentage: range (0-1, 0-1, 0-1 )
    red_percentage = red / float(255)
    green_percentage = green / float(255)
    blue_percentage = blue / float(255)

    # get hsv percentage: range (0-1, 0-1, 0-1)
    color_hsv_percentage = colorsys.rgb_to_hsv(
        red_percentage, green_percentage, blue_percentage)

    # get normal hsv: range (0-360, 0-255, 0-255)
    color_h = round(360*color_hsv_percentage[0])
    # color_s = round(255*color_hsv_percentage[1])
    # color_v = round(255*color_hsv_percentage[2])
    # color_hsv = (color_h, color_s, color_h)

    # Definir el rango de color amarillo en HSV
    lower_yellow = (color_h-10, 25, 0)
    upper_yellow = (color_h+100, 255, 255)

    amarillo_bajo_4 = np.array([0, 25, 0])
    amarillo_alto_4 = np.array([180, 255, 255])

    return [lower_yellow, upper_yellow]


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

    filename = 'resultado_'+create_id_from_timestamp() + '.jpg'

    cv2.imwrite(filename, img)

    return filename


amarillo_bajo_1 = np.array([7, 70, 0])
amarillo_alto_1 = np.array([180, 255, 255])
amarillo_bajo_2 = np.array([20, 26, 0])
amarillo_alto_2 = np.array([37, 255, 255])
amarillo_bajo_4 = np.array([0, 25, 0])
amarillo_alto_4 = np.array([180, 255, 255])
rangos_amarillos = [[amarillo_bajo_1, amarillo_alto_1], [
    amarillo_bajo_2, amarillo_alto_2], [amarillo_bajo_4, amarillo_alto_4]]

AMARILLO = (0, 255, 255)


def metodo_3(imagen_url):
    img = cv2.imread(imagen_url)
    area_total_imagen = img.shape[1] * img.shape[0]
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    imagenes_procesadas = []

    for rango_amarillo in rangos_amarillos:
        copia = img.copy()
        area_total = 0
        mask = cv2.inRange(hsv_img, rango_amarillo[0], rango_amarillo[1])

        imagen_restada = cv2.bitwise_and(
            img, img, mask=mask)
        imagen_restada = cv2.cvtColor(imagen_restada, cv2.COLOR_BGR2RGB)
        # Aplicar contornos
        contornos = buscar_contornos(mask)

        for i in range(len(contornos)):
            CID = i

            area = cv2.contourArea(contornos[i])
            if area > 50:
                cv2.drawContours(copia, contornos, CID, AMARILLO, -1)

                ROJO = (0, 0, 255)
                area_total += area

        calculo_area = round(area_total / area_total_imagen * 100, 2)
        ley_cobre = round((area_total/area_total_imagen)*100*0.34, 2)
        texto = 'Area: {}%'.format(calculo_area)
        texto_ley_cobre = 'Ley de cobre: {}%'.format(ley_cobre)
        cv2.putText(copia, texto, (10, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, ROJO, 4, cv2.LINE_AA)
        cv2.putText(copia, texto_ley_cobre, (10, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, ROJO, 4, cv2.LINE_AA)
        filename = 'resultado_'+create_id_from_timestamp() + '.jpg'

        cv2.imwrite(filename, copia)
        imagenes_procesadas.append(filename)

    return imagenes_procesadas


def calibrate_yellow(imagen_url, color_hsv):

    img = cv2.imread(imagen_url)
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv_img, color_hsv[0], color_hsv[1])

    # calcopirita_color = cv2.inRange(imghsv, amarillo_bajo_2, amarillo_alto_2)
    imagen_restada = cv2.bitwise_and(
        img, img, mask=mask)
    imagen_restada = cv2.cvtColor(imagen_restada, cv2.COLOR_BGR2RGB)

    filename = 'resultado_'+create_id_from_timestamp() + '.jpg'

    cv2.imwrite(filename, imagen_restada)

    return filename


@ app.route('/upload', methods=['POST'])
def index():
    # the data is a multipart/form-data request
    my_imagen = request.files['myImage']
    my_imagen.save('image.jpg')
    rgb_color = request.form['rgbColor']

    hcv = convert_rgb_to_hsv(rgb_color)
    filename = dibujar_contornos_segun_color('image.jpg', hcv)
    return {
        'message': 'Image uploaded successfully',
        'rango_hsv': str(hcv),
        'image_url': url_for('uploaded_file', filename=filename)
    }


@ app.route('/upload-tres', methods=['POST'])
def index_dos():
    links_imagenes = []
    # the data is a multipart/form-data request
    my_imagen = request.files['myImage']
    my_imagen.save('image.jpg')

    imagenes = metodo_3('image.jpg')

    for imagen in imagenes:
        links_imagenes.append(url_for('uploaded_file', filename=imagen))
    return {
        'message': 'Image uploaded successfully',

        'image_url': '',
        'links_imagenes': links_imagenes,
        'imagen_original': url_for('uploaded_file', filename='image.jpg')
    }


@ app.route('/imagen/<filename>')
def uploaded_file(filename):
    return send_from_directory('.', filename)


app.run(debug=True, host='0.0.0.0', port=5000)
