import cv2
import easyocr
import numpy as np
from matplotlib import pyplot as pl
from func import *
from datetime import date
import re

def get_unique_meaning(my_list):

    unique = []
    for elem in my_list:
        if elem in unique:
            continue
        else:
            unique.append(elem)

    return unique
            

def rotateToRead(passport_name, angle):

    img = Image.open(passport_name)
    img_rotate = img.rotate(angle, expand=True)
    img_rotate.save(passport_name, quality = 95)


def createTemplateSegm(passport_name, template_name):

    createBackSegm()
    backname = "back.png"
    back = Image.open(backname)
    back.load()

    passport = Image.open(passport_name)
    passport.load()

    back.paste(
        passport,
        (0, 0),
    )
    back.save(template_name)

    return back


def getData(template_name, name, passport_name, rotated_num):
    img = cv2.imread(template_name)
    w = img.shape[1]
    h = img.shape[0]
    colorM = (255, 255, 255)
      # 2-я страница
    cv2.rectangle(img, (0,0), (w, h//2+170), colorM, thickness=cv2.FILLED)
    cv2.GaussianBlur(img, (7,11), 0)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    text = easyocr.Reader(["ru", "be"])
    text = text.readtext(img, 
                            decoder = 'wordbeamsearch',
                            blocklist=["!@#$;:%^&?*()-+="], 
                            width_ths = 1.4,
                            detail=1,
                            contrast_ths=0.01)

    data = dict()
    data["SURNAME_BY"] = None
    data["SURNAME_RU"] = None
    data["NAME_BY"] = None
    data["NAME_RU"] = None
    data["FN_BY"] = None
    data["FN_RU"] = None
    data["PLACE_BY"] = None
    data["PLACE_RU"] = None
    data["DATE OF BIRTH"] = None
    data["IDENTIFICATION No"] = None
    data["ORGANIZATION_BY"] = None
    data["ORGANIZATION_RU"] = None

    try:
        new_list = list()
        for num in range(len(text)):
            el_text = text[num]
            meaning = el_text[1]
            pos = el_text[2]

            #print(meaning, "|", pos)
            check = re.fullmatch(r'^\d$', meaning)
            #print(meaning, "|", pos)
            if float(pos) > 0.40 and not check:
                print(meaning, "|", pos)
                new_list.append(meaning.upper())
            # for word in good_words:
            #     if float(pos) < 0.50 and re.findall(word, meaning):
            #         new_list.append(meaning.upper())   
        print(new_list)
        start = 0
        while not re.findall(r'ФАМИЛИЯ', new_list[start]):
            start += 1
        surname = new_list[start+1]
        surname = surname.split('/')
        data["SURNAME_BY"] = surname[0]
        data["SURNAME_RU"] = surname[1]

        while not re.findall(r'ИМЯ', new_list[start]):
            start += 1
        namep = new_list[start+1]
        namep = namep.split('/')
        data["NAME_BY"] = namep[0]
        data["NAME_RU"] = namep[1]

        while not re.findall(r'ОТЧЕСТВО', new_list[start]):
            start += 1
        fn = new_list[start+1]
        fn = fn.split('/')
        data["FN_BY"] = fn[0]
        data["FN_RU"] = fn[1]
        
        while not re.findall(r'ДАТА РОЖДЕНИЯ', new_list[start]):
            start += 1  
        birth = new_list[start+1]
        data["DATE OF BIRTH"] = birth.replace(' ', '.') 

        while not re.findall(r'ИДЕНТИФИКАЦИОННЫЙ', new_list[start]):
            start += 1
        inum = new_list[start+2]
        data["IDENTIFICATION No"] = inum.strip()
    
        while not re.findall(r'МЕСТО РОЖДЕНИЯ', new_list[start]):
            start += 1
        place = new_list[start+1]
        place = place.split('/')
        data["PLACE_BY"] = place[0]
        data["PLACE_RU"] = place[1]

        while not re.findall(r'ОРГАН', new_list[start]):
            start += 1
        orgab = new_list[start+1]
        orgar = new_list[start+2]
        data["ORGANIZATION_BY"] = orgab
        data["ORGANIZATION_RU"] = orgar
        
        for key in data:
            if isinstance(data[key], str):
                data[key] = data[key].replace('/', '').strip()  # Удаляем пробелы в начале и конце строки

        print(data)

        keys = list(data.keys())
        file = open("info\\"+name+"_info.json", 'w', encoding="utf-8")
        file.write('{\n')
        file.write('"'+str(keys[0])+'" : "'+str(data[keys[0]]) + '"')
        for k in keys[1:]:
            file.write(',\n')
            file.write('"'+str(k)+'" : "'+str(data[k]) + '"')
        file.write('\n}\n')
        file.close()

    except:
        if rotated_num >= 4:
            return False
        rotated_num += 1
        #print("+90 except")
        #print(rotated_num)
        rotateToRead(passport_name, 90)
        createTemplateSegm(passport_name, template_name)
        getData(template_name, name, passport_name, rotated_num)

 