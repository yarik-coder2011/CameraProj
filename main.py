import cv2
from tkinter import *
from PIL import Image, ImageTk
import numpy as np
import os
from PIL import Image, ImageChops
import pyttsx3

engine = pyttsx3.init()
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml') #подключаем фильтры
face_cascade_nofront = cv2.CascadeClassifier("haarcascade_profileface.xml")
eye_cascade = cv2.CascadeClassifier("haarcascade_eye.xml")





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
        res = "photo/1/" + res + ".png" #сохраняем в паку с всеми фотками
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
            faces_no_front = face_cascade_nofront.detectMultiScale(gray, 1.3, 5)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5) #ищем схожести
            eye = eye_cascade.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2) #Создается прямоугольник
            for (x, y, w, h) in faces_no_front:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2) #Создается прямоугольник
            #for (x, y, w, h) in eye:
            #    cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2) #Создается прямоугольник


            self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
            self.canvas.create_image(0, 0, image=self.photo, anchor=NW) #помещаем в канвас изображение с камеры
            self.master.after(self.delay, self.update)
        else:
            self.cap.release()



def procent(Cam):
    global im_crop, b, result
    schet = 0
    d = []
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    ret, img = Cam.cap.read()
    if ret:
        frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        print(faces)

        for (x, y, w, h) in faces:  # находим лица
            cv2.rectangle(frame, (x, y), (x + w, y + h), (250, 0, 0), 2) #рамка
            im = Image.fromarray(frame)
            im_crop = im.crop((x, y, x + w, y + h))  # обрезаем
        photo = os.listdir("photo/1") #получаем все имена из папки с фотками
        print(photo)
        pon = 10
        for i in photo:
            image_1 = im_crop
            image_2 = Image.open("photo/1/" + i)
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
            d.append(x)
            print(x)
            if len(d) == len(photo):
                for i in range(0, len(d)):
                    #print(d[schet])
                    schet = schet + 1
                    if d[schet] == max(d):
                        #print(schet)
                        print(max(d))
                        global photo_scet
                        photo_scet = photo[schet]
                        #print(photo_scet[-4: -1])
                        lbl.configure(text=photo_scet.replace(".png", ""))
                        lbl.pack()
                        engine.say(photo_scet.replace(".png", ""))
                        engine.runAndWait()
                        break
            if max(d) < 55:
                lbl.configure(text="человека нет в базе")
                lbl.pack()

def bock_procent(Cam):
    global im_crop1, result1
    schet = 0
    d1 = []
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    ret, img = Cam.cap.read()
    if ret:
        frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade_nofront.detectMultiScale(gray, 1.3, 5)
        print(faces)

        for (x, y, w, h) in faces:  # находим лица
            cv2.rectangle(frame, (x, y), (x + w, y + h), (250, 0, 0), 2)  # рамка
            im = Image.fromarray(frame)
            im_crop1 = im.crop((x, y, x + w, y + h))  # обрезаем
        photo = os.listdir("photo/2")  # получаем все имена из папки с фотками
        print(photo)
        pon = 10
        for i in photo:
            image_1 = im_crop1
            image_2 = Image.open("photo/2/" + i)
            result1 = ImageChops.difference(image_1, image_2)
            f = 0
            test = np.array(result1)
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
            d1.append(x)
            print(x)
            if len(d1) == len(photo):
                for i in range(0, len(d1)):
                    schet = schet + 1
                    if d1[schet] == max(d1):
                        print(max(d1))
                        global photo_scet1
                        photo_scet1 = photo[schet]
                        # print(photo_scet[-4: -1])
                        lbl.configure(text=photo_scet1.replace(".png", ""))
                        lbl.pack()
                        engine.say(photo_scet1.replace(".png", ""))
                        engine.runAndWait()
                        break
            if max(d1) < 50:
                lbl.configure(text="человека нет в базе")
                lbl.pack()

def search_func():
    search_proces = format(search.get())
    photo = os.listdir("photo/1")
    photo2 = os.listdir("photo/2")
    print(photo)
    search_proces = search_proces + ".png"
    for i in photo:
        if search_proces == i:
            open = Image.open("photo/1/" + i)
            open.show()
            break
    for i in photo2:
        if search_proces == i:
            open = Image.open("photo/2/" + i)
            open.show()
            break

def all_people():
    photo = os.listdir("photo/1/")
    #print(photo)
    a = ""
    for i in photo:
        a = a + " " + i.replace(".png", ",")
    #print(a)
    lbl_people.configure(text=a)
    lbl_people.pack()

def clear():
    lbl_people.configure(text="")
    lbl_people.pack()

def regist_2():
    ret, img = camera.cap.read()
    res = format(txt.get())  # получаем название с текстового поля
    res = "photo/2/" + res + ".png"  # сохраняем в паку с всеми фотками
    if ret:
        frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # создаём RGB
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # создаём серый
        faces_no_front = face_cascade_nofront.detectMultiScale(gray, 1.3, 5)  # ищем схожести с фильтром
        for (x, y, w, h) in faces_no_front:  # находим лица
            cv2.rectangle(frame, (x, y), (x + w, y + h), (250, 0, 0), 2)
            im = Image.fromarray(frame)
            im_crop = im.crop((x, y, x + w, y + h))  # обрезаем
            im_crop.save(res, quality=95)  # сохраняем




sc = 0

if __name__ == "__main__":
    root = Tk()
    root.title('распознаватель лиц')
    lbl = Label(root, text="")
    lbl.pack()
    camera = Cam(master=root)
    but2 = Button(root, text="регистрация бокового лица", command=regist_2)
    but2.pack()
    txt = Entry(root, width=50)
    txt.place(relx=0.5, rely=0.3)
    txt.pack()
    but = Button(root, text="проверка", command=lambda: procent(camera))
    but.pack()
    but3 = Button(root, text="проверка бокового лица", command=lambda: bock_procent(camera))
    but3.pack()
    search_t = Label(root, text="введите имя человека а я проверю есть ли он в базе")
    search_t.pack()
    search = Entry(root, width=50)
    search.pack()
    but_s = Button(root, text="поиск", command=search_func)
    but_s.pack()
    lbl_people = Label(root, text="")
    lbl_people.pack()
    but_all_people = Button(root, text="вывести всех людей которые есть в базе", command=all_people)
    but_all_people.pack()
    but_clear = Button(root, text="убрать текст", command=clear)
    but_clear.pack()
    wt = Label(text="внимание если лица нету в кадре то программа выведет данные послледнего пользователя")
    wt.pack()
    root.mainloop()
