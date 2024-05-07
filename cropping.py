import numpy as np
import cv2
import imutils

def croppByCountour(filename, contour_mask_name, name_passport, name):

    image = cv2.imread(contour_mask_name)
    h, w, c = image.shape

    original = cv2.imread(filename)
    h, w, c = original.shape

    # Шаг 2
    grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    grayImageBlur = cv2.blur(grayImage,(3,3))
    edgedImage = cv2.Canny(grayImageBlur, 100, 300, 3)
    # выход - серое изображение с определенными границами

    # Шаг 3
    # найти контуры на обрезанном изображении, рационально организовать область 
    # оставить только большие варианты 
    allContours = cv2.findContours(edgedImage.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    allContours = imutils.grab_contours(allContours)
    # сортировка контуров области по уменьшению и сохранение топ-1
    allContours = sorted(allContours, key=cv2.contourArea, reverse=True)[:1]
    # aппроксимация контура
    perimeter = cv2.arcLength(allContours[0], True) 
    ROIdimensions = cv2.approxPolyDP(allContours[0], 0.02*perimeter, True)
    # показать контуры на изображении
    cv2.drawContours(original, [ROIdimensions], -1, (0,0,255), 5)#image

    # Шаг 4
    # изменение массива координат
    ROIdimensions = ROIdimensions.reshape(4,2)
    # список удержания координат ROI
    rect = np.zeros((4,2), dtype='float32')
    # наименьшая сумма будет у верхнего левого угла, 
    # наибольшая — у нижнего правого угла
    s = np.sum(ROIdimensions, axis=1)
    rect[0] = ROIdimensions[np.argmin(s)]
    rect[2] = ROIdimensions[np.argmax(s)]
    # верх-право будет с минимальной разницей
    # низ-лево будет иметь максимальную разницу
    diff = np.diff(ROIdimensions, axis=1)
    rect[1] = ROIdimensions[np.argmin(diff)]
    rect[3] = ROIdimensions[np.argmax(diff)]
    # верх-лево, верх-право, низ-право, низ-лево
    (tl, tr, br, bl) = rect
    # вычислить ширину ROI
    widthA = np.sqrt( (tl[0] - tr[0])**2 + (tl[1] - tr[1])**2 )
    widthB = np.sqrt( (bl[0] - br[0])**2 + (bl[1] - br[1])**2 )
    maxWidth = max(int(widthA), int(widthB))
    # вычислить высоту ROI
    heightA = np.sqrt( (tl[0] - bl[0])**2 + (tl[1] - bl[1])**2 )
    heightB = np.sqrt( (tr[0] - br[0])**2 + (tr[1] - br[1])**2 )
    maxHeight = max(int(heightA), int(heightB))

    # Шаг 5
    # набор итоговых точек для обзора всего документа
    # размер нового изображения
    dst = np.array([
        [0,0],
        [maxWidth-1, 0],
        [maxWidth-1, maxHeight-1],
        [0, maxHeight-1]], dtype="float32")
    # вычислить матрицу перспективного преобразования и применить её
    transformMatrix = cv2.getPerspectiveTransform(rect, dst)
    # преобразовать ROI
    scan = cv2.warpPerspective(original, transformMatrix, (maxWidth, maxHeight))
    cv2.imwrite(name_passport, scan)

    # image = cv2.imread(contour_mask_name)
    # cv2.imwrite(name_passport, image)