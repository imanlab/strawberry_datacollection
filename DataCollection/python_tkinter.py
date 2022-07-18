import pathlib
from tkinter import *
import tkinter as tk
from PIL import ImageTk, Image
from tkinter import simpledialog
import numpy as np
import sys

image_path = '/Volumes/mydrive/localdrive/datasets/Strawberry_dataset_single/strawberry_dataset_20_01/rgb_image/strawberry_20cm__asda__egypt__fortuna__20_01_2021_12_34_20_17.8_1.png'
number = 10
berry_data = []
berry_data_save = {}


def key(event):
    print("pressed", repr(event.char))


def myClick():
    myLabel = Label(root, text='OK')
    myLabel.pack()


def callback(event):

    # canvas.create_window(event.x, event.y, window=entry1)
    #
    # berry_number = entry1.get()
    # print('entry: ', berry_number )

    USER_INP = simpledialog.askstring(title="Berry ID",
                                      prompt="Berry ID")

    # myButton = Button(root, text='Click Me', command=myClick())
    # myButton.pack()

    if USER_INP:

        global number, berry_data, berry_data_save
        text_id_berry = canvas.create_text(event.x, event.y, text=USER_INP.split(" ")[0], fill='yellow')
        text_id = canvas.create_text(760, number, text=USER_INP, anchor=NW, fill='red', )
        print('user input: ', USER_INP)
        print("clicked at", event.x, event.y)
        USER_INP = list(map(float, USER_INP.split()))
        USER_INP.append(event.x - 100)
        USER_INP.append(event.y - 20)
        berry_data_save[text_id] = USER_INP
        berry_data.append((text_id, text_id_berry, event.x, event.y))
        number += 20


def get_point(event):

    global start_x, start_y

    start_x = canvas.canvasx(event.x)
    start_y = canvas.canvasy(event.y)


def callback_rect(event):

    global berry_data_save
    curX = canvas.canvasx(event.x)
    curY = canvas.canvasy(event.y)

    rectangle_id = canvas.create_rectangle(start_x, start_y, curX, curY, outline='red')

    for berry in berry_data:

        if start_x < berry[2] < curX:
            if start_y < berry[3] < curY:
                canvas.delete(berry[0])
                canvas.delete(berry[1])
                berry_data_save.pop(berry[0])

    canvas.delete(rectangle_id)


def rs_call(image_path):
    root = Tk()
    canvas = Canvas(root, width=960, height=480)
    # entry1 = tk.Entry(root, width=5)
    # entry1.pack()

    img = ImageTk.PhotoImage(Image.open(image_path))
    canvas.create_image(100, 20, anchor=NW, image=img)

    canvas.bind("<Key>", key)
    canvas.bind("<Button-1>", callback)
    canvas.bind("<Button-2>", get_point)
    canvas.bind("<ButtonRelease-2>", callback_rect)
    canvas.pack()

    mainloop()


if __name__ == '__main__':

    folder = sys.argv[1]
    # print(folder)

    # folder = '/Volumes/mydrive/localdrive/datasets/dyson_weight_estimation/003/'

    for file_name in pathlib.Path(folder).rglob('*_rgb.png'):

        print(file_name)

        root = Tk()
        canvas = Canvas(root, width=960, height=480)
        # entry1 = tk.Entry(root, width=5)
        # entry1.pack()

        imag_obj = Image.open(file_name)

        img = ImageTk.PhotoImage(imag_obj)
        canvas.create_image(100, 20, anchor=NW, image=img)

        canvas.bind("<Key>", key)
        canvas.bind("<Button-1>", callback)
        canvas.bind("<Button-2>", get_point)
        canvas.bind("<ButtonRelease-2>", callback_rect)
        canvas.pack()

        imag_obj.save('my_image.png')

        mainloop()

        berry_data_save_list = []
        for k in berry_data_save.keys():
            berry_data_save_list.append(berry_data_save[k])

        berry_data_save_list = np.asarray(berry_data_save_list, dtype=np.float32)
        print('berry_data_save_list: ', berry_data_save_list)
        np.save(str(file_name).replace('_rgb.png', '_label'), berry_data_save_list)
        berry_data_save = {}

    sys.exit(0)
