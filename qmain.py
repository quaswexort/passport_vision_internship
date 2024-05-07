import time
import json

from masking import *
from func import *
from read import *
from cropping import *
arrayDir = ['pages','contourMask','passport','templates','info']
deleteDir(arrayDir)
createDir(arrayDir)

for i in range(1, 6):
    #i = int(input("Введите номер паспорта: "))
    print(i)
    st = time.time()
    # создание JPG из PDF
    name = 'ex'+str(i)
    path2pdf = "get_data\\"+name+".pdf"
    filename = "pages\\"+name+".jpg"
    contour_mask_name = "contourMask\\"+name+"contour_mask_name.png"
    passport_name = "passport\\"+name+"passport.png"
    template_name = "templates\\_"+name+"template.png"

    convertPdf2Jpg(path2pdf, filename)
    createDetectionMask(filename, contour_mask_name)
    try:
        croppByCountour(filename, contour_mask_name, passport_name, name)
        print("croppByCountour")

        createTemplateSegm(passport_name, template_name)
        print("createTemplateSegm")

        print("\033[0m {}" .format("-----------------------------------------------------------------", template_name, "-----------------------------------------------------------------"))

        # with open("true_data.json") as json_file:
        #     true_data = json.load(json_file)
        # Открываем файл JSON с указанием кодировки utf-8
        with open("true_data.json", "r", encoding="utf-8") as json_file:
            true_data = json.load(json_file)

        getData(template_name, name, passport_name, 0)  
        print("getData")

        with open("info\\"+name+"_info.json", "r", encoding="utf-8") as json_file:
            json_data = json.load(json_file)

        for key in json_data.keys():
            if json_data[key] == true_data[key]:
                out_green(json_data[key])
            else:
                out_red(json_data[key])
        print("\033[0m {}" .format("---"+name+"---"))

        fsh = time.time()
        print("\033[0m {}" .format(fsh-st))

    except:
        print("Ошибка входных данных.")
        print("Отсканируйте документ снова, не выходя за границы сканера.")
