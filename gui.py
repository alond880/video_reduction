#!/usr/bin/python
import os
import sys
import cv2
import tkinter as tk
import tkinter.filedialog
from tkinter import ttk
from tkinter import filedialog as fd
import tkinter.filedialog


#fflag : 0 - folder
#        1 - file

#script_pass_arguments:
# [0] = path
# [1] = fflag
# [2] = tank id
# [3] = location
# [4] = battalion
# [5] = sensetivity
# [6] = max length


#define main window
global main_window
main_window = tk.Tk()

#chosen video file path
global path
path = "No file selected..."

global script_pass_arguments
script_pass_arguments = ["", "", "", "", "", "", ""]


def play_gif(file_path):
    return


def browse_file_click():
    # chosen video file object
    global chosen_file
    chosen_file = fd.askopenfile(parent=main_window, mode='rb')

    if chosen_file:
        main_window.text.set(chosen_file.name)
        #file.close()


def browse_folder_click():
    # chosen videos folder object
    global chosen_folder
    chosen_folder = tk.filedialog.askdirectory(parent=main_window)

    if chosen_folder:
        main_window.text.set(chosen_folder)
        # file.close()
    return

#function that runs the movment recognition script
def start_thinking(path, fflag):
    #print(script_pass_arguments[0])
    #print(script_pass_arguments[1])
    #print(script_pass_arguments[2])
    #print(script_pass_arguments[3])

    script_pass_arguments[0] = path
    script_pass_arguments[1] = str(fflag)

    #print(type(fflag))
    #print(script_pass_arguments)

    #                             path                            fflag                             tank id                          location                        battalion
    os.system('python main.py ' + script_pass_arguments[0] + " " + script_pass_arguments[1] + " " + script_pass_arguments[2] + " " + script_pass_arguments[3] + " " +script_pass_arguments[4])


def confirm_window_func(fflag):

    confirm_window = tk.Tk()
    confirm_window.geometry("200x250")
    confirm_window.title("confirmation window")

    if fflag == 1:
        #check if user chose a file
        try:
            chosen_file
        except NameError:
            confirm_messege = "no file selected"
        else:
            confirm_messege = chosen_file.name

    elif fflag == 0:
        try:
            chosen_folder
        except NameError:
            confirm_messege = "no folder selected"
        else:
            confirm_messege = chosen_folder


    verifay_label1 = tk.Label(confirm_window, text="input selected:")
    verifay_label2 = tk.Label(confirm_window, text="continue?")
    confirm_label = tk.Label(confirm_window, text=confirm_messege)
    verifay_label1.pack()
    confirm_label.pack()
    verifay_label2.pack()

    ok_bottum = tk.Button(confirm_window,
                       text="yes",
                       width=10,
                       height=1,
                       bg='green',
                       command=lambda: start_thinking(confirm_messege, fflag))
    ok_bottum.place(x=120, y=200)

    cancel_bottum = tk.Button(confirm_window,
                          text="cancel",
                          width=10,
                          height=1,
                          bg='red',
                          command=confirm_window.withdraw)
    cancel_bottum.place(x=0, y=200)


def start_click(fflag):
    confirm_window_func(fflag)


def get_settings(settings_label, sensitivity, max_length):

    sensitivity_value = sensitivity.get()
    max_length_value = max_length.get()

    script_pass_arguments[4] = sensitivity_value
    script_pass_arguments[5] = max_length_value

    print("First Name: %s\nLast Name: %s" % (sensitivity_value, max_length_value))
    settings_label.config(text="changes saved")
    settings_label.place(x=105, y=200)


def settings_click():
    settings_window = tk.Tk()
    settings_window.geometry("300x350")
    settings_window.title("settings window")

    settings_label = tk.Label(settings_window, text="")
    tk.Label(settings_window, text="sensitivity").grid(row=0)
    tk.Label(settings_window, text="max wait (sec)").grid(row=1)

    sensitivity = tk.Entry(settings_window)
    max_length = tk.Entry(settings_window)

    sensitivity.grid(row=0, column=1)
    max_length.grid(row=1, column=1)

    ok_bottum = tk.Button(settings_window,
                          text="OK",
                          width=10,
                          height=1,
                          bg='white',
                          command=lambda: get_settings(settings_label, sensitivity, max_length))
    ok_bottum.place(x=100, y=300)

    explenation_label = tk.Label(settings_window, text="sensetivity is size of smallest object\n"
                                                       "to detect moving.\n"
                                                       "default and recommended sensetivity is 900\n"
                                                       "max wait is wait time between movments.")
    explenation_label.place(x=30, y=100)


def ok_entry_func(tank_id_entry, location_entry, battalion_entry, ok_label):

    tank_id = tank_id_entry.get()
    location = location_entry.get()
    battalion = battalion_entry.get()

    script_pass_arguments[2] = tank_id
    script_pass_arguments[3] = location
    script_pass_arguments[4] = battalion

    ok_label.config(text="changes saved")
    ok_label.place(x=160, y=210)

    print("tank id: " + str(tank_id))
    print("location: " + str(location))
    print("battalion: " + str(battalion))


def MainWindow():
    main_window.geometry("400x500")
    main_window.title("Video Redaction Application")
    main_window.text = tk.StringVar()
    main_window.text.set("No input")

    first_img = tk.PhotoImage(file="C:/Users/Rapat/Desktop/images/tankmid.gif")
    img_label = tk.Label(main_window, image=first_img, height=150, width=250)
    img_label.place(x=75, y=325)
    img_label.image = first_img


    browse_file = tk.Button(main_window,
                       text="Browse file",
                       width=10,
                       height=1,
                       command=browse_file_click,
                       bg='white')
    browse_file.place(x=300, y=31)

    browse_file_label = tk.Label(main_window, textvariable=main_window.text, height=1, width=40)
    browse_file_label.place(x=0, y=50)

    browse_folder = tk.Button(main_window,
                            text="Browse folder",
                            width=10,
                            height=1,
                            command=browse_folder_click,
                            bg='white')
    browse_folder.place(x=300, y=61)

    #browse_folder_label = tk.Label(main_window, textvariable=main_window.text, height=1, width=40)
    #browse_folder_label.place(x=0, y=66)

    start_file = tk.Button(main_window,
                       text="start file",
                       width=10,
                       height=2,
                       command=lambda: start_click(1),
                       bg = 'green')
    start_file.place(x=125, y=255)

    start_folder = tk.Button(main_window,
                      text="start folder",
                      width=10,
                      height=2,
                      command=lambda: start_click(0),
                      bg='green')
    start_folder.place(x=225, y=255)

    settings = tk.Button(main_window,
                      text="settings",
                      width=15,
                      height=1,
                      command=settings_click,
                      bg='white')

    settings.place(x=5, y=5)

    #video tags
    canvas1 = tk.Canvas(main_window, width=50, height=100)
    canvas1.place(x=190, y=120)

    tank_id_entry = tk.Entry(main_window)
    canvas1.create_window(10, 0, window=tank_id_entry)
    tank_id_label = tk.Label(main_window, text=":צ")
    tank_id_label.place(x=280,y=110)


    location_entry = tk.Entry(main_window)
    canvas1.create_window(10, 20, window=location_entry)
    location_entry_label = tk.Label(main_window, text=":מיקום")
    location_entry_label.place(x=280, y=130)

    battalion_entry = tk.Entry(main_window)
    canvas1.create_window(10, 40, window=battalion_entry)
    battalion_entry_label = tk.Label(main_window, text=":גדוד")
    battalion_entry_label.place(x=280, y=150)

    ok_label = tk.Label(main_window, text=" ")
    ok_entry = tk.Button(main_window,
                      text="ok",
                      width=7,
                      height=1,
                      command= lambda: ok_entry_func(tank_id_entry,location_entry, battalion_entry, ok_label),
                      bg='white')
    ok_entry.place(x=170, y=175)


def main():
    MainWindow()
    main_window.mainloop()
    return

if __name__ == '__main__':
    sys.exit(main())  # next section explains the use of sys.exit