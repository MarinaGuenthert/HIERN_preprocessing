from importlib import import_module
import pandas as pd
import numpy as np
import scipy as sp
import math
import matplotlib.pyplot as plt
import lmfit.models
import sys

import tkinter as tk
import PIL
from PIL import Image, ImageFont
import os

from tkinter import ttk
from tkinter import filedialog
#from tkinter import *
from tkinter import Label, Button, Canvas, Tk, PhotoImage

from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

import scipy.ndimage as ndimage
import scipy.ndimage.filters as filters
import matplotlib.pyplot as plt

from myutils import MyUtils
from joining import path
from theme import HIERNtheme

from Raman_fit import Raman_data_evaluation

class plot_selection(tk.Toplevel):

    def __init__(self, master: Tk):
        tk.Toplevel.__init__(self)

        self.__save_v = tk.StringVar()
        self.__variable = tk.StringVar()
        #self.__variable = MyUtils.plate[0]
        
        self.withdraw()
        self.lift(master) 
        
        icon_path = MyUtils.get_absolute_path('resources\HIERN_icon.ico')
        self.iconbitmap(icon_path)    

    def Raman_single_plotting(self, folder_selected, Raman_data, LorentzFits_Raman, maxima_list):

        self.__save_v = tk.StringVar()
        self.__variable = tk.StringVar()

        #self.__variable = tk.StringVar(self)
        #self = tk.Tk()
        #self.__save_v.set('off')
        self.configure(background=HIERNtheme.mywhite)
        # self.geometry('200x500')

        # OptionList = MyUtils.plate

        #variable = tk.StringVar(self)
        #print(self.__save_v.get())
        self.__variable.set(MyUtils.chosen[0])

        opt = tk.OptionMenu(self, self.__variable, *MyUtils.chosen)
        #opt.config(width=20, font=('Helvetica', 12))
        opt.grid(row = 0, column = 0)

        Button (self, text = 'plot fits', bg = HIERNtheme.myblue, fg = HIERNtheme.mywhite, command = lambda: self.__subplot(folder_selected)).grid(row = 0, column = 1)

        Button (self, text = 'save figure', bg = HIERNtheme.myblue, fg = HIERNtheme.mywhite, command = lambda: self.__save(folder_selected)).grid(row = 0, column = 2)

        self.__save_v.set('off')

        self.update_idletasks()
        self.deiconify()

        # MyUtils.plate = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8']




    def __save(self, folder_selected):
        #global save_v
        self.__save_v.set('on')
        self.__subplot(folder_selected)

    def __subplot(self, folder_selected):

        #print(self.__variable.get())
        #global variable
        #global save_v
        #variable.get()
        #print(str(variable.get()))

        # x_Raman = [None]*96

        #for k in range(0,96,2):
            
            #x_Raman[k] = Raman_data.iloc[:290,k]

        for i in range(0,48):
            if self.__variable.get() == MyUtils.plate[i]:
                fig, axes = plt.subplots(1, 2, figsize=(12.8, 4.8), sharex=True)
                axes[0].plot(Raman_data_evaluation.x_Raman[i*2], Raman_data_evaluation.Raman_data.iloc[0:290,2*i+1], label='original data')
                #plt.xlim([100, 450])
                #axes[0].plot(x, init, '--', label='initial fit')
                axes[0].plot(Raman_data_evaluation.x_Raman[i*2], Raman_data_evaluation.LorentzFits_Raman[2*i].best_fit, '--', label='best fit')
                axes[0].legend()


                comps = Raman_data_evaluation.LorentzFits_Raman[2*i].eval_components(x=Raman_data_evaluation.x_Raman[i*2])
                #axes[1].plot(x_Raman[i*2], Raman_data.iloc[0:290,1])
                #axes[1].plot(x_Raman[i*2], comps['linear'], '--', label='background')
                if len(Raman_data_evaluation.maxima_list[i*2]) == 2:
                    axes[1].plot(Raman_data_evaluation.x_Raman[i*2], comps['l1_'], '--', label='Lorentzian component 1')
                if len(Raman_data_evaluation.maxima_list[i*2]) == 3:
                    axes[1].plot(Raman_data_evaluation.x_Raman[i*2], comps['l1_'], '--', label='Lorentzian component 1')
                    axes[1].plot(Raman_data_evaluation.x_Raman[i*2], comps['l2_'], '--', label='Lorentzian component 2')
                if len(Raman_data_evaluation.maxima_list[i*2]) == 4:
                    axes[1].plot(Raman_data_evaluation.x_Raman[i*2], comps['l1_'], '--', label='Lorentzian component 1')
                    axes[1].plot(Raman_data_evaluation.x_Raman[i*2], comps['l2_'], '--', label='Lorentzian component 2')
                    axes[1].plot(Raman_data_evaluation.x_Raman[i*2], comps['l3_'], '--', label='Lorentzian component 3')
                if len(Raman_data_evaluation.maxima_list[i*2]) == 5:
                    axes[1].plot(Raman_data_evaluation.x_Raman[i*2], comps['l1_'], '--', label='Lorentzian component 1')
                    axes[1].plot(Raman_data_evaluation.x_Raman[i*2], comps['l2_'], '--', label='Lorentzian component 2')
                    axes[1].plot(Raman_data_evaluation.x_Raman[i*2], comps['l3_'], '--', label='Lorentzian component 3')
                    axes[1].plot(Raman_data_evaluation.x_Raman[i*2], comps['l4_'], '--', label='Lorentzian component 4')
                if len(Raman_data_evaluation.maxima_list[i*2]) == 6:
                    axes[1].plot(Raman_data_evaluation.x_Raman[i*2], comps['l1_'], '--', label='Lorentzian component 1')
                    axes[1].plot(Raman_data_evaluation.x_Raman[i*2], comps['l2_'], '--', label='Lorentzian component 2')
                    axes[1].plot(Raman_data_evaluation.x_Raman[i*2], comps['l3_'], '--', label='Lorentzian component 3')
                    axes[1].plot(Raman_data_evaluation.x_Raman[i*2], comps['l4_'], '--', label='Lorentzian component 4')
                    axes[1].plot(Raman_data_evaluation.x_Raman[i*2], comps['l5_'], '--', label='Lorentzian component 5')
                if len(Raman_data_evaluation.maxima_list[i*2]) == 7:
                    axes[1].plot(Raman_data_evaluation.x_Raman[i*2], comps['l1_'], '--', label='Lorentzian component 1')
                    axes[1].plot(Raman_data_evaluation.x_Raman[i*2], comps['l2_'], '--', label='Lorentzian component 2')
                    axes[1].plot(Raman_data_evaluation.x_Raman[i*2], comps['l3_'], '--', label='Lorentzian component 3')
                    axes[1].plot(Raman_data_evaluation.x_Raman[i*2], comps['l4_'], '--', label='Lorentzian component 4')
                    axes[1].plot(Raman_data_evaluation.x_Raman[i*2], comps['l5_'], '--', label='Lorentzian component 5')
                    axes[1].plot(Raman_data_evaluation.x_Raman[i*2], comps['l6_'], '--', label='Lorentzian component 6')
                if len(Raman_data_evaluation.maxima_list[i*2]) == 8:
                    axes[1].plot(Raman_data_evaluation.x_Raman[i*2], comps['l1_'], '--', label='Lorentzian component 1')
                    axes[1].plot(Raman_data_evaluation.x_Raman[i*2], comps['l2_'], '--', label='Lorentzian component 2')
                    axes[1].plot(Raman_data_evaluation.x_Raman[i*2], comps['l3_'], '--', label='Lorentzian component 3')
                    axes[1].plot(Raman_data_evaluation.x_Raman[i*2], comps['l4_'], '--', label='Lorentzian component 4')
                    axes[1].plot(Raman_data_evaluation.x_Raman[i*2], comps['l5_'], '--', label='Lorentzian component 5')
                    axes[1].plot(Raman_data_evaluation.x_Raman[i*2], comps['l6_'], '--', label='Lorentzian component 6')
                    axes[1].plot(Raman_data_evaluation.x_Raman[i*2], comps['l7_'], '--', label='Lorentzian component 7')
                axes[1].legend()
                    
                fig.patch.set_facecolor(HIERNtheme.mywhite)
                    
                if self.__save_v.get() == 'on':
                    single_fit = 'single_fit_of_' + str(MyUtils.plate[i]) + '.png'
                    completeName8 = os.path.join(path.completeName7, single_fit)
                    # print(folder_selected)
                    print(completeName8)
                    plt.savefig(completeName8, transparent = False)

                    #plt.xlim([100, 450])
                plt.show()
                    
                    #canvas = FigureCanvasTkAgg(fig, self)
                    #canvas.config(width=500, height = 200)
                    #canvas.draw()

                    # placing the canvas on the Tkinter window
                    #canvas.get_tk_widget().grid(row = 3, column = 0, columnspan = 12, sticky=tk.W)
                    
                self.__save_v.set('off')
                    
                    


