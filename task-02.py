import tkinter
from tkinter import *
import tkinter as tk
import tkinter.messagebox as mbox
from tkinter import ttk
from tkinter import filedialog
from PIL import ImageTk, Image
import cv2
import os
import numpy as np
from cv2 import *
import random

window = Tk()
window.geometry("1000x700")
window.title("Image Encryption Decryption")
window.configure(background="#ffffff")


global count, emig
frp = []
tname = []
con = 1
bright = 0
panelB = None
panelA = None
x = None
filename = None
image_encrypted = None
key = None

def getpath(path):
    a = path.split(r'/')
    fname = a[-1]
    l = len(fname)
    location = path[:-l]
    return location

def getfoldername(path):
    a = path.split(r'/')
    name = a[-1]
    return name

def getfilename(path):
    a = path.split(r'/')
    fname = a[-1]
    a = fname.split('.')
    a = a[0]
    return a

def openfilename():
    filename = filedialog.askopenfilename(title='"pen"', filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
    return filename

def open_img():
    global x, panelA, panelB
    global count, eimg, location, filename
    count = 0
    x = openfilename()
    if x:
        img = Image.open(x)
        eimg = img
        img = ImageTk.PhotoImage(img)
        temp = x
        location = getpath(temp)
        filename = getfilename(temp)
        if panelA is None or panelB is None:
            panelA = Label(image=img)
            panelA.image = img
            panelA.pack(side="left", padx=40, pady=10)
            panelB = Label(image=img)
            panelB.image = img
            panelB.pack(side="right", padx=10, pady=10)
        else:
            panelA.configure(image=img)
            panelB.configure(image=img)
            panelA.image = img
            panelB.image = img
    else:
        mbox.showwarning("Warning", "No image selected.")

def en_fun(x):
    global image_encrypted, key
    image_input = cv2.imread(x, 0)
    if image_input is not None:
        (x1, y) = image_input.shape
        image_input = image_input.astype(float) / 255.0
        mu, sigma = 0, 0.1
        key = np.random.normal(mu, sigma, (x1, y)) + np.finfo(float).eps
        image_encrypted = image_input / key
        cv2.imwrite('image_encrypted.jpg', image_encrypted * 255)
        imge = Image.open('image_encrypted.jpg')
        imge = ImageTk.PhotoImage(imge)
        panelB.configure(image=imge)
        panelB.image = imge
        mbox.showinfo("Encrypt Status", "Image Encrypted successfully.")
        filename = filedialog.asksaveasfile(mode='w', defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg")])
        if filename:
            with open(filename.name, 'wb') as f:
                f.write(open('image_encrypted.jpg', 'rb').read())
            mbox.showinfo("Success", "Encrypted image saved successfully!")
    else:
        mbox.showwarning("Warning", "Failed to read image.")

def de_fun():
    global image_encrypted, key
    if image_encrypted is not None and key is not None:
        image_output = image_encrypted * key
        image_output *= 255.0
        cv2.imwrite('image_output.jpg', image_output)
        imgd = Image.open('image_output.jpg')
        imgd = ImageTk.PhotoImage(imgd)
        panelB.configure(image=imgd)
        panelB.image = imgd
        mbox.showinfo("Decrypt Status", "Image decrypted successfully.")
        filename = filedialog.asksaveasfile(mode='w', defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg")])
        if filename:
            with open(filename.name, 'wb') as f:
                f.write(open('image_output.jpg', 'rb').read())
            mbox.showinfo("Success", "Decrypted image saved successfully!")
    else:
        mbox.showwarning("Warning", "Image not encrypted yet.")

def reset():
    global count, eimg
    if x is not None:
        count = 6
        global o6
        o6 = cv2.imread(x)[:, :, ::-1]
        image = Image.fromarray(o6)
        eimg = image
        image = ImageTk.PhotoImage(image)
        panelB.configure(image=image)
        panelB.image = image
        mbox.showinfo("Success", "Image reset to original format!")
    else:
        mbox.showwarning("Warning", "No image selected.")

def save_img():
    global location, filename, eimg
    if filename is not None:
        filename = filedialog.asksaveasfile(mode='w', defaultextension=".jpg")
        if filename:
            eimg.save(filename)
            mbox.showinfo("Success", "Encrypted Image Saved Successfully!")
    else:
        mbox.showwarning("Warning", "No image to save.")

    
start1 = tk.Label(text="ORIGINAL\n\nIMAGE", borderwidth=3, font=("TimesRoman", 20), bg="#bcbcbc", fg="black", relief="raised")
start1.place(x=150, y=270)

start1 = tk.Label(text="Click here to select image:", font=("TimesRoman", 20), fg="#000000", bg="#ffffff")
start1.place(x=50, y=50)

start1 = tk.Label(text="ENCRYPTED\nDECRYPTED\nIMAGE", borderwidth=3, font=("TimesRoman", 20), bg="#bcbcbc", fg="black", relief="raised")
start1.place(x=750, y=270)

chooseb = Button(window, text="SELECT", command=open_img, font=("Times Roman", 30, "bold"), bg="#bcbcbc", fg="black", borderwidth=3, relief="raised")
chooseb.place(x=450, y=40)

saveb = Button(window, text="SAVE", command=save_img, font=("Times Roman", 20), bg="#bcbcbc", fg="black", borderwidth=3, relief="raised")
saveb.place(x=200, y=580)

enb = Button(window, text="ENCRYPT", command=lambda: en_fun(x), font=("Times Roman", 20), bg="#bcbcbc", fg="black", borderwidth=3, relief="raised")
enb.place(x=450, y=250)

deb = Button(window, text="DECRYPT", command=de_fun, font=("Times Roman", 20), bg="#bcbcbc", fg="black", borderwidth=3, relief="raised")
deb.place(x=450, y=350)

resetb = Button(window, text="RESET", command=reset, font=("Times Roman", 20), bg="#bcbcbc", fg="black", borderwidth=3, relief="raised")
resetb.place(x=700, y=580)

def download_encrypted():
    global image_encrypted
    if image_encrypted is not None:
        filename = filedialog.asksaveasfile(mode='w', defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg")])
        if filename:
            cv2.imwrite(filename.name, image_encrypted * 255)
            mbox.showinfo("Success", "Encrypted Image Downloaded Successfully!")
    else:
        mbox.showwarning("Warning", "No encrypted image to download.")

def download_decrypted():
    global image_encrypted, key
    if image_encrypted is not None and key is not None:
        image_output = image_encrypted * key
        image_output *= 255.0
        filename = filedialog.asksaveasfile(mode='w', defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg")])
        if filename:
            cv2.imwrite(filename.name, image_output)
            mbox.showinfo("Success", "Decrypted Image Downloaded Successfully!")
    else:
        mbox.showwarning("Warning", "No decrypted image to download.")

window.mainloop()