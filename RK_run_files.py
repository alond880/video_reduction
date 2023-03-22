#the porpuse of this code is to a general program to get all files names in a folder
#and send them to any script that is in need for such a function.
import os
import sys
import cv2
import tkinter as tk
import tkinter.filedialog
from tkinter import ttk
from tkinter import filedialog as fd
import tkinter.filedialog


#define main window
global main_window
main_window = tk.Tk()

#chosen video file path
global path
path = "No path selected..."

def browse_click():
    # chosen video file object
    global chosen_path
    chosen_path = tk.filedialog.askdirectory(parent=main_window)
    print("folder: " + chosen_path)

    if chosen_path:
        main_window.text.set(chosen_path)
        #file.close()


#def script_click():
    # chosen script
    #global chosen_script
    #chosen_script = fd.askopenfile(parent=main_window, mode='rb')
    #print("script: " + chosen_script.name)


def start_click():
    os.system("python " + "script.py" + " " + chosen_path)
    #print("python " + chosen_script.name + " " + chosen_path)



def main():
    return

if __name__ == '__main__':
    sys.exit(main())