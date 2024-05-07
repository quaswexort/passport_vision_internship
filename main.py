
from pdf2image import convert_from_path
import cv2
import numpy as np
import easyocr

def convertPdf2Jpg(path2pdf, jpgName, path2poppler='C:\\Program Files\\poppler-23.11.0\\Library\\bin'):
    image = convert_from_path(path2pdf, 500, poppler_path=path2poppler)
    image[0].save(jpgName, 'JPEG')

path2pdf = "get_data//ex1"+".pdf"
filename = "pages//ex1"+".jpg"
convertPdf2Jpg(path2pdf, filename)

img = cv2.imread('pages//ex1.jpg')

# img = cv2.resize(img, (img.shape[1]//7, img.shape[0]//7))
# img = img[200:720, 100:500]

# Преобразуем изображение в оттенки серого  
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Резкость
kernel1 = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
sharpened = cv2.filter2D(gray, -1, kernel1)

# Бинаризация
_, binary = cv2.threshold(sharpened, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)

# Удаление шумов медианным фильтром
#median_blur = cv2.medianBlur(binary, 7)
resized_img = cv2.resize(gray, (img.shape[1]//7, img.shape[0]//7))  
cv2.imshow('Image', resized_img)
cv2.imshow('sharpened', sharpened)
cv2.waitKey(0)
cv2.destroyAllWindows()

text_reader = easyocr.Reader(["ru", "be"])
text = text_reader.readtext(gray, 
                            decoder='wordbeamsearch', 
                            blocklist=["!@#$;:%^&?*()-+="],
                            width_ths=2,
                            detail=1, 
                            contrast_ths=0.01,
                            paragraph=False)

for res in text:
    if res[2] > 0.5:
        print(res[1], "|", res[2])
