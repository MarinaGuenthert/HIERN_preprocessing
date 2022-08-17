import imp
import tkinter as tk
from tkinter import ttk
from tkinter import Tk, PhotoImage, Label, Button
#import awesometkinter as atk
from theme import HIERNtheme
from myutils import MyUtils
import PIL
from threading import Thread


class progress_bar_circular(tk.Toplevel, Thread):
    
    def __init__(self, master: Tk):
        tk.Toplevel.__init__(self)
    
        # self.MyUtils.chosen = []
        # self.__buttons = [[None]*8 for _ in range(6)]
        # self.__sample = [[None]*8 for _ in range(6)]
        #self.methode = StringVar()

        self.withdraw()
        self.lift(master)

        # self.columnconfigure(0, 1)
        # self.rowconfigure(0, 1)
        
        icon_path = MyUtils.get_absolute_path('resources\HIERN_icon.ico')
        self.iconbitmap(icon_path)

        self.pb = ttk.Progressbar(self, orient=tk.HORIZONTAL, mode='indeterminate', length=200)
        # self.pb.grid(row=5, columnspan=5)

    def progress_show(self):

        self.title('progress')

        Label(self, text='in progress', font=HIERNtheme.header_font, fg=HIERNtheme.myblue, bg=HIERNtheme.mywhite).grid(row=0, column=0)

        Label(self, text='do not worry, this migth take up to 30 min', font=HIERNtheme.standard_font, fg=HIERNtheme.myblue, bg=HIERNtheme.mywhite).grid(row=3, column=0)

        # self.pb = ttk.Progressbar(self, orient=tk.HORIZONTAL, mode='indeterminate', length=200)
        self.pb.grid(row=5, columnspan=5)

        Button(self, text='stop', command=self.pb.stop).grid(row=7, column=0)

        # self.geometry('600x600')
        self.configure(background=HIERNtheme.mywhite)

        self.progress_start

        self.update_idletasks()
        self.deiconify()
        
    # def show(self, methode):

    def progress_start(self):

        self.pb.start(20)
        print('START')

        # 3d progressbar
        # f1 = atk.Frame3d(self)
        # f1.grid(row=3, column=3)
        # bar = atk.RadialProgressbar3d(f1, bg = HIERNtheme.mywhite, fg=HIERNtheme.mylime, size=150, text_fg = '#333')
        # # bar = atk.RadialProgressbar(f1, fg='green', bg='white')
        # bar.grid(row=20, column=20)
        # bar.start()

    def progress_stop(self):

        print('STOP')
        self.pb.stop
        self.destroy()
        