# Импортируем библиотеки
from PIL import ImageDraw, ImageFont, Image
import numpy as np
from imutils.video import VideoStream
import imutils
import cv2
from time import sleep

# Загружаем шрифт
FONT = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSansBold.ttf", 16)

# минимальный размер пятна
BLOBSIZE = 1000

# константы насыщенности и яркости
S_MIN = 29
S_MAX = 255
V_MIN = 148
V_MAX = 255

# примерные значения тона для фильтров
HUES = { 
        "оранжевый": 10, 
        "жёлтый": 40, 
        "зелёный": 55,
        "синий": 100, 
        "фиолетовый" : 130, 
        "красный": 165, 
        }

# цвет подсвечивания контуров (красный, зелёный, синий)
CONTCOLOR = (0, 255, 0)

# толщина линии контура
CTHICK = 2

# определяем размеры кадра
FRAMESIZE = (640, 480)

# создаём объект видео потока
vs = VideoStream(src=0, usePiCamera=True, resolution=FRAMESIZE, framerate=32).start()

# ждём окончания инициализации видеопотока
sleep(2)

# определяем функцию проверки углов контура
def shapeDetect(c):

    # инициируем переменную названия фигуры и приблизительный контур
    shape = ""
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.04 * peri, True)

    # если 3 вершины - фигура треугольник
    if len(approx) == 3:
        shape = "треугольник"

    # если 4 - прямоугольник
    elif len(approx) == 4:

        # вычисляем прямоугольник в который вписывается фигура
        # и его отношение сторон
        (x, y, w, h) = cv2.boundingRect(approx)
        ar = w / float(h)

        # если отношение сторон не 1 - значит прямоугольник
        shape = "квадрат" if ar >= 0.95 and ar <= 1.05 else "прямоугольник"

    # иначе - круг
    else:
        shape = "круг"

    # возвращаем название фигуры
    return shape

# входим в бесконечный цикл
while True:

    # считываем кадр из потока
    image = vs.read()

    # создаём его копию для вывода
    img_copy = image.copy()

    # уменьшаем изображение для ускорения вычислений
    resized = imutils.resize(image, width=300)

    # вычисляем отношение оригинального изображения к уменьшенному
    ratio = image.shape[0] / float(resized.shape[0])

    # проходим по всем тонам
    for hue in HUES:

        # вычисляем порог тона
        h_min = HUES[hue] - 10
        h_max = HUES[hue] + 10

        # определяем границы цвета в HSV
        lower_range = np.array([h_min, S_MIN, V_MIN])
        upper_range = np.array([h_max, S_MAX, V_MAX])

        # конвертируем изображение в HSV
        hsv = cv2.cvtColor(resized, cv2.COLOR_BGR2HSV)

        # создаём маску из границ цвета
        thres = cv2.inRange(hsv, lower_range, upper_range)
        thres = cv2.GaussianBlur(thres, (5, 5), 0)

        # вывод масок всех цветов
        #cv2.imshow(hue, thres) # раскомментируйте для вывода

        # находим контуры
        cnts = cv2.findContours( 
                                 thres.copy(), 
                                 cv2.RETR_EXTERNAL, 
                                 cv2.CHAIN_APPROX_SIMPLE 
                                )                       
        cnts = imutils.grab_contours(cnts)

        # Следующие два цикла можно объединить в один если
        # нет необходимости выводить текст кириллицей. Для
        # вывода латиницы используйте cv2.putText()

        # проходим по всем контурам
        for c in cnts:

            # если площадь текущего контура мала...
            if cv2.contourArea(c) < BLOBSIZE:
                # переходим к следующему
                continue

            # приводим размеры контуров к исходным
            c = c.astype("float")
            c *= ratio
            c = c.astype("int")

            # выводим контуры на копию изображения
            cv2.drawContours(img_copy, [c], -1, CONTCOLOR, CTHICK)

        # Следующие манипуляции нужны для вывода текста кириллицей.
        # Конвертируем изображение из BGR в RGB
        img = cv2.cvtColor(img_copy, cv2.COLOR_BGR2RGB)
        # создаём объект изображения PIL из массива пикселей
        im_pil = Image.fromarray(img)
        # создаём объект рисования
        draw = ImageDraw.Draw(im_pil)

        # проходим по всем контурам
        for c in cnts:

            # если площадь текущего контура мала...
            if cv2.contourArea(c) < BLOBSIZE:
                # переходим к следующему
                continue

            # получаем моменты изображения контура
            M = cv2.moments(c)
            cX = 0
            cY = 0

            # вычисляем из моментов координаты
            if M["m00"] != 0:
                cX = int((M["m10"] / M["m00"]) * ratio)
                cY = int((M["m01"] / M["m00"]) * ratio)

            # вычисляем название фигуры
            shapename = shapeDetect(c)
            shapename = hue + " " + shapename

            # выводим название фигуры
            draw.text((cX, cY), shapename, font=FONT)

        # конвертируем объект изображения PIL обратно в массив пикселей
        img_copy = np.asarray(im_pil)
        # конвертируем изображение из RGB в BGR
        img_copy = cv2.cvtColor(img_copy, cv2.COLOR_BGR2RGB)

    # выводим изображение
    cv2.imshow("Image", img_copy)

    # Если была нажата клавиша ESC
    k = cv2.waitKey(1)
    if k == 27:

        # прерываем выполнение цикла
        break

# закрываем все окна
cv2.destroyAllWindows()

# останавливаем видео поток
vs.stop()