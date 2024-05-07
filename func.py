from pdf2image import convert_from_path
import cv2
import numpy as np
from PIL import Image
import os
import shutil
from datetime import date


def out_red(text):
    print("\033[31m {}" .format(text))


def out_green(text):
    print("\033[32m {}" .format(text))


def convertPdf2Jpg(path2pdf, jpgName, path2poppler='C:\\Program Files\\poppler-23.11.0\\Library\\bin'):
    
    image = convert_from_path(path2pdf, 500, poppler_path=path2poppler)
    image[0].save(jpgName, 'JPEG')


def getTime(Tstart, Tfinish):
    t = Tfinish-Tstart
    return int(t//60), int(t%60)


def deleteDir(arrayDir):
    try:
        for nameDir in arrayDir:
            shutil.rmtree(nameDir)
    except:
        print()


def createDir(arrayDir):
    try:
        for nameDir in arrayDir:
            os.mkdir(nameDir)
    except:
        print()


def createBackSegm():

    H_PASSPORT = 3445
    W_PASSPORT = 2425
    back= np.zeros((3445,2425), dtype='uint8')
    cv2.imwrite("back.png", back)


def createdateBirth(dateBirth):

    if not dateBirth.isdigit():
        dateBirth = list(dateBirth)
        for i in range(len(dateBirth)):
            ch = dateBirth[i]
            if ch == 'o' or ch == 'O':
                dateBirth[i] = '0'
        dateBirth = ''.join(dateBirth)

    yearB = int(dateBirth[:2])
    monthB = dateBirth[2:4]
    dayB = dateBirth[4:]

    today = date.today()
    d1 = today.strftime("%d/%m/%Y")
    yearNow = d1[-4:]
    if yearB < int(yearNow[-2:]):
        yearB = yearNow[-4:-2] + str(yearB)
        if len(yearB) != 4:
            yearB = list(yearB)
            yearB.insert(2, '0')
            yearB = ''.join(yearB)
    else:
        yearB = str(int(yearNow[-4:-2])-1) + str(yearB)
        # добавить допорлнение числа
    datte = dayB+'.'+monthB+'.'+yearB
    return datte


def createdateExpiry(dateExpiry):
    
    # проверка, везде ли число
    if not dateExpiry.isdigit():
        dateExpiry = list(dateExpiry)
        for i in range(len(dateExpiry)):
            ch = dateExpiry[i]
            if ch == 'o' or ch == 'O':
                dateExpiry[i] = '0'
        dateExpiry = ''.join(dateExpiry)

    yearE = int(dateExpiry[:2])
    monthE = dateExpiry[2:4]
    dayE = dateExpiry[4:]

    today = date.today()
    d1 = today.strftime("%d/%m/%Y")
    yearNow = d1[-4:]
    if yearE >= int(yearNow[-2:]):
        yearE = yearNow[-4:-2] + str(yearE)
        if len(yearE) != 4:
            yearE = list(yearE)
            yearE.insert(2, '0')
            yearE = ''.join(yearE)
    else:
        yearE = str(int(yearNow[-4:-2])+1) + str(yearE)
        #print("Пасспорт мб просрочен!!!")
    datte = dayE+'.'+monthE+'.'+yearE
    return datte