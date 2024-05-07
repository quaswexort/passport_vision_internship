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
    # поле с фото
    cv2.rectangle(img, (0,0), (int(1.4*w)//5+30, int(9*h)//10), colorM, thickness=cv2.FILLED)
    cv2.rectangle(img, (w-50,0), (w, h), colorM, thickness=cv2.FILLED)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    text = easyocr.Reader(["en"])
    text = text.readtext(img, 
                            decoder = 'wordbeamsearch',
                            blocklist=["!@#$;:'%^&?*()-+=."], 
                            width_ths = 1,
                            detail=1,
                            contrast_ths=0.01)

    data = dict()
    data["TYPE"] = None
    data["CODE OF ISSUING"] = None
    data["PASSPORT No"] = None
    data["SURNAME"] = None
    data["GIVEN NAMES"] = None
    data["NATIONALITY"] = None
    data["DATE OF BIRTH"] = None
    data["IDENTIFICATION No"] = None
    data["SEX"] = None
    data["PLACE OF BIRTH"] = None
    data["DATE OF ISSUE"] = None
    data["DATE OF EXPIRY"] = None
    data["AUTHORITY"] = None
    
    try:
        last = len(text)-1
        #prelast = last-1
        
        prelast_str = list()
        new_list = list()
        stopwords = ['TYPE', 'STATE', 'SATE', 'CODE', 'ISSUING', 'PASSPORT', 'SURNAME', 'GIVEN',
                        'NAMES', 'NATIONALITY', 'DATE', 'BIRTH', 'IDENTIFICATION',
                        'SEX', 'PLACE', 'ISSUE', 'AUTHORITY']
        good_words = ['MINISTRY', 'INTERNAL', 'FOREIGN', 'AFFAIRS']

        for num in range(len(text)):
            el_text = text[num]
            meaning = el_text[1]
            pos = el_text[2]

            #print(meaning, "|", pos)
            
            # нашли check = False
            # если ничего не нашли check = True
            check = not re.findall(r'\/', str(meaning)) 
            flag = 0
            for stopword in stopwords:
                if bool(re.findall(stopword, str(meaning))):
                    flag += 1
            #print(meaning, "|", pos)
            if float(pos) > 0.50 and flag == 0 and check:
                #print(meaning, "|", pos)
                new_list.append(meaning.upper())
            for word in good_words:
                if float(pos) < 0.50 and re.findall(word, meaning):
                    new_list.append(meaning.upper())
            flag = 0
            #if float(pos) < 0.50 and (num == prelast or num == last):
                #print(meaning, "|", pos)         
            if re.findall(r'P<', meaning):
                prelast = meaning           

        # --- start : достаем всю информацию из нижних двух строк ---
        # поле TYPE
        #type_meaning = text[prelast][1][0]
        data["TYPE"] = 'P'

        # поле TYPE
        codeIssuing_meaning = text[last][1][10:13]
        if re.fullmatch(r'\b\D\D\D\b', codeIssuing_meaning):
            data["CODE OF ISSUING"] = codeIssuing_meaning.upper()
        else:
            data["CODE OF ISSUING"] = 'BLR'

        numPassport_meaning = text[last][1][:9]
        if not re.findall(r'\D{2}\d{7}', numPassport_meaning) and count > 4:
            return 1
        
        data["PASSPORT No"] = numPassport_meaning.upper()

        match = re.search(r'BLR\w+(<<|<K|K<|KK)', prelast)
        try:
            lastt = len(match[0])
            surname_meaning = match[0][3:lastt-2]
            data["SURNAME"] = surname_meaning.upper()
        except:
            data["SURNAME"] = new_list[3]

        match = re.search(r'(<<|<K|K<|KK)\w+', prelast)
        #print(text[prelast][1])
        lastt = len(match[0])
        names_meaning = match[0][2:lastt]
        data["GIVEN NAMES"] = names_meaning.upper()

        dateBirth = text[last][1][13:19]
        data["DATE OF BIRTH"] = createdateBirth(dateBirth)

        data["SEX"] = text[last][1][20].upper()

        dateExpiry = text[last][1][21:27]
        data["DATE OF EXPIRY"] = createdateExpiry(dateExpiry)

        data["IDENTIFICATION No"] = text[last][1][28:42].upper()
        #if len(data["IDENTIFICATION No"]) < 14:
        #    return 1
        # --- end : достаем всю информацию из нижних двух строк ---
        
        start = 0
        while ''.join(new_list[start].split()) != data["GIVEN NAMES"]:
            start += 1

        nationality_meaning = 'REPUBLIC OF BELARUS'
        data["NATIONALITY"] = nationality_meaning
        
        try:
            while not re.fullmatch(r'M', new_list[start]) and \
                not re.fullmatch(r'F', new_list[start]):
                start += 1
            data["SEX"] = new_list[start]
        except:
            data["SEX"] = text[last][1][20].upper()

        start += 1
        country = 'REPUBLIC OF BELARUS'
        placeB_meaning = new_list[start]
        data["PLACE OF BIRTH"] = placeB_meaning
        count = 0
        if len(placeB_meaning) > 3:
            for i in range(len(placeB_meaning)):
                if placeB_meaning[i] != country[i]:
                    count += 1
            if count < 4:
                data["PLACE OF BIRTH"] = country

        start = start+1
        dateIssue_meaning = new_list[start]

        while dateIssue_meaning.isalpha():
            start += 1
            dateIssue_meaning = new_list[start]
        data["DATE OF ISSUE"] = '.'.join(new_list[start].split())

        start = start+1

        if new_list[start] != 'MINISTRY OF':    
            data["AUTHORITY"] = 'MINISTRY OF'+' '+new_list[start+1]
        else:
            data["AUTHORITY"] = new_list[start]+' '+new_list[start+1]

        keys = list(data.keys())
        file = open("info\\"+name+"_info.json", 'w')
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


def getData2(template_name, name, passport_name, rotated_num):
    img = cv2.imread(template_name)
    w = img.shape[1]
    h = img.shape[0]
    colorM = (255, 255, 255)

    # 2-я страница
    #cv2.rectangle(img, (0,0), (w, h//2+170), colorM, thickness=cv2.FILLED)
    img  = cv2.GaussianBlur(img,(7,11),0)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    

    text = easyocr.Reader(["be", "ru"])
    text = text.readtext(img, 
                            decoder = 'wordbeamsearch',
                            blocklist=["!@#$;:%^&?*()-+="], 
                            width_ths = 1.4,
                            detail=1,
                            contrast_ths=0.01)
    #print(text)
    data = dict()
    data["SURNAME_BY"] = None
    data["SURNAME_RU"] = None
    data["NAME_BY"] = None
    data["NAME_RU"] = None
    data["FN_BY"] = None
    data["FN_RU"] = None
    data["DATE OF BIRTH"] = None
    data["IDENTIFICATION No"] = None
    data["PLACE_BY"] = None
    data["PLACE_RU"] = None
    data["DATE OF EXPIRY"] = None
    data["DATE OF ISSUE"] = None
    data["ORGANIZATION_BY"] = None
    data["ORGANIZATION_RU"] = None

    stopwords = ['РЭСПУБЛІКА БЕЛАРУСЬ / РЕСПУБЛИКА БЕЛАРУСЬ', 'ПРОЗВІШЧА/ФАМИЛИЯ', 'ІМЯ/ИМЯ', 'ІМЯ ПА', 'БАЦЬКУ/ОТЧЕСТВО', 'ІМЯ ПА БАЦЬКУ/ОТЧЕСТВО',
                  'ДАТА РОЖДЕНИЯ ', 'ІДЭНТЫФІКАЦЫЙНЫ','ИДЕНТИФИКАЦИОННЫЙ ', 
                  'МЕСЦА НАРАДЖЭННЯ', 'МЕСТО РОЖДЕНИЯ', 'ДАТА ВЫДАЧЫ/ДАТА ВЫДАЧИ', 'ТЭРМІН ДЗЕЯННЯ/СРОК ДЕЙСТВИЯ',
                  'ЯКІ ВЫДАЎ ПАШПАРТ/ОРГАН, ВЫДАВШИЙ ПАСПОРТ', 'ОРГАН,', '\b9\b' ]

    new_list = list()
    try:
        for num in range(len(text)):
            el_text = text[num]
            meaning = el_text[1]
            pos = el_text[2]

            #print(meaning, "|", pos)

            flag = 0
            for stopword in stopwords:
                #print(bool(re.findall(stopword, str(meaning.upper()))), "|",str(meaning.upper()), "|", pos)
                if bool(re.findall(stopword, str(meaning.upper()))):
                    flag += 1
            

            check = re.fullmatch(r'\b\d\b', meaning)
            if float(pos) > 0.50 and flag==0 and not check:
            #     #print(meaning, "|", pos)
                new_list.append(meaning.upper())
        print(new_list)
        
        start = 0
        surname = new_list[start]
        surname = surname.split('/')
        data["SURNAME_BY"] = surname[0]
        data["SURNAME_RU"] = surname[1]

        start += 1
        names = new_list[start]
        names = names.split('/')
        data["NAME_BY"] = names[0]
        data["NAME_RU"] = names[1]

        start += 1
        fn = new_list[start]
        fn = fn.split('/')
        data["FN_BY"] = fn[0]
        data["FN_RU"] = fn[1]
        
        start += 1
        birth = new_list[start]
        data["DATE OF BIRTH"] = birth

        start += 1
        inum = new_list[start]
        data["IDENTIFICATION No"] = inum

        start += 1
        place = new_list[start]
        place = place.split('/')
        data["PLACE_BY"] = place[0]
        data["PLACE_RU"] = place[1]

        start += 1
        data["DATE OF EXPIRY"] = new_list[start]

        start += 1
        data["DATE OF ISSUE"] = new_list[start]

        start += 1
        orgab = new_list[start].split('/')[0]
        orgar = new_list[start+1]
        data["ORGANIZATION_BY"] = orgab
        data["ORGANIZATION_RU"] = orgar
        
        for key in data.keys():
            print(key, '-', data[key])

        keys = list(data.keys())
        file = open("info\\"+name+"_info.json", 'w', encoding='utf-8')
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
        print("+90 except")
        #print(rotated_num)
        rotateToRead(passport_name, 90)
        createTemplateSegm(passport_name, template_name)
        getData2(template_name, name, passport_name, rotated_num)



