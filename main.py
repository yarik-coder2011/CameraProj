import cv2
from tkinter import *
from PIL import Image, ImageTk
import numpy as np
import os
from PIL import Image, ImageChops

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml') #подключаем фильтры


def cutter(img):
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml') #подключаем фильтры
    img = cv2.imread(res) #читаем картинку из фото
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #переводим в чб
    faces = face_cascade.detectMultiScale(gray, 1.3, 5) #ищем схожести
    for (x, y, w, h) in faces: #находим лицо
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2) #обводим лицо
        im = Image.open(res) #открываем картинку
        im_crop = im.crop((x, y, x + w, y + h)) #обрезаем лицо
        im_crop.save('pon.png', quality=95) #сохраняем
        cv2.imshow('img', img) #показываем результат
class Cam:
    def __init__(self, master=None):
        self.cap = cv2.VideoCapture(0) #подключчаемся к камере
        self.master = master
        self.canvas = Canvas(master, width=800, height=600) #создаём канвас для изображение с камеры
        self.canvas.pack()
        self.btn = Button(root, text="регистрация", command=self.photo) #создаём кнопку
        self.btn.pack()

        self.delay = int(1000/self.cap.get(cv2.CAP_PROP_FPS)) #получаем картинку с камеры и обнавляем её
        self.update()

    def photo(self):
        ret, img = self.cap.read()
        global res
        res = format(txt.get()) #получаем название с текстового поля
        res = "photo/" + res + ".png" #сохраняем в паку с всеми фотками
        if ret:
            frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) #создаём RGB
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #создаём серый
            faces = face_cascade.detectMultiScale(gray, 1.3, 5) #ищем схожести с фильтром
            for (x, y, w, h) in faces: #находим лица
                cv2.rectangle(frame, (x, y), (x + w, y + h), (250, 0, 0), 2)
                im = Image.fromarray(frame)
                im_crop = im.crop((x, y, x + w, y + h)) #обрезаем
                im_crop.save(res, quality=95) #сохраняем
    def update(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) #создаём RGB
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #создаём серый
            faces = face_cascade.detectMultiScale(gray, 1.3, 5) #ищем схожести
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2) #Создается прямоугольник
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
            self.canvas.create_image(0, 0, image=self.photo, anchor=NW) #помещаем в канвас изображение с камеры
            self.master.after(self.delay, self.update)
        else:
            self.cap.release()





def procent(Cam):
    global im_crop, b
    schet = 0
    d = []
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    ret, img = Cam.cap.read()
    if ret:
        frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        #print(faces)

        for (x, y, w, h) in faces:  # находим лица
            cv2.rectangle(frame, (x, y), (x + w, y + h), (250, 0, 0), 2) #рамка
            im = Image.fromarray(frame)
            im_crop = im.crop((x, y, x + w, y + h))  # обрезаем
        photo = os.listdir("photo") #получаем все имена из папки с фотками
        print(photo)
        pon = 10
        for i in photo:
            image_1 = im_crop
            image_2 = Image.open("photo/" + i)
            result = ImageChops.difference(image_1, image_2)
            f = 0
            test = np.array(result)
            test1 = test.shape[0]
            test2 = test.shape[1]
            size = test1 * test2
            for i in test:
                for j in i:
                    if j[0] < 50 and j[1] < 50 and j[2] < 50:
                        f += 1
                    else:
                        continue

            x = 100 * f // size
            len_phot = len(photo)
            #max_x = max(x)
            d.append(x)

            #print(x)
            #if x >= 55:
            #    pon = 1
            #if pon == 1:
            #    lbl.configure(text="человек есть в базе")
            #    lbl.pack()
            #    pon = 1
            #if pon == 0 and x < 55 or pon == 10:
            #    lbl.configure(text="человека нет в базе")
            #    lbl.pack()

            #print(photo)
            if len(d) == len(photo):
                for i in range(0, len(d)):
                    #print(d[schet])
                    schet = schet + 1
                    if d[schet] == max(d):
                        #print(schet)
                        print(max(d))
                        lbl.configure(text=photo[schet])
                        lbl.pack()
                        break
            if max(d) < 55:
                lbl.configure(text="человека нет в базе")
                lbl.pack()



if __name__ == "__main__":
    root = Tk()
    root.title('распознаватель лиц')
    lbl = Label(root, text="")
    lbl.pack()
    camera = Cam(master=root)
    txt = Entry(root, width=10)
    txt.place(relx = 0.5, rely = 0.3)
    txt.pack()
    but = Button(root, text="проверка в процентовке", command= lambda: procent(camera))
    but.pack()
    wt = Label(text="внимание если лица нету в кадре то программа выведет данные послледнего пользователя")
    wt.pack()

    root.mainloop()