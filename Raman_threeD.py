from importlib import import_module
import pandas as pd
import numpy as np
import scipy as sp
import math
import matplotlib.pyplot as plt
from matplotlib import animation
import lmfit.models
import sys

import tkinter as tk
import PIL
from PIL import Image, ImageFont
import os

from tkinter import Variable, ttk
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
from output_txt import save_files
plt.rcParams['animation.ffmpeg_path'] = r'C:\FFmpeg\bin\ffmpeg.exe'

class plot_Raman_D(tk.Toplevel):

    def __init__(self, master: Tk):
        tk.Toplevel.__init__(self)

        self.__startvalue = tk.StringVar()
        self.__endvalue = tk.StringVar()
        self.__name = tk.StringVar()

        self.variable = tk.StringVar()
        self.__geometry = tk.StringVar()
        
        self.withdraw()
        self.lift(master) 
        
        icon_path = MyUtils.get_absolute_path('resources\HIERN_icon.ico')
        self.iconbitmap(icon_path)  

    def Raman_threeD_plotting(self, folder_selected):

        self.__startvalue = tk.StringVar()
        self.__endvalue = tk.StringVar()
        self.__name = tk.StringVar()

        self.configure(background=HIERNtheme.mywhite)

        self.title('Raman 3D evaluation')
        self.__geometry.set('horizontal')

        title_Label = Label(self, text='which peak would you like to evaluate?', bg=HIERNtheme.mywhite, fg=HIERNtheme.myblue, font=HIERNtheme.header_font)
        title_Label.grid(row=0, columnspan=3)

        start_Label = Label(self,text='start value for peak position', bg=HIERNtheme.mywhite, fg=HIERNtheme.myblue, font=HIERNtheme.standard_font)
        start_Label.grid(row=1, column=0)

        end_Label = Label(self,text='end value for peak position', bg=HIERNtheme.mywhite, fg=HIERNtheme.myblue, font=HIERNtheme.standard_font)
        end_Label.grid(row=2, column=0)

        e1 = tk.Entry(self, textvariable=self.__startvalue)
        e2 = tk.Entry(self, textvariable=self.__endvalue)

        e1.grid(row=1, column=2)
        e2.grid(row=2, column=2)

        name_Label = Label(self, text='title for 3D plot', bg=HIERNtheme.mywhite, fg=HIERNtheme.myblue, font=HIERNtheme.header_font)
        name_Label.grid(row=5, columnspan=2)

        e3 = tk.Entry(self, textvariable=self.__name)
        e3.grid(row=5, column=2)

        label_angle = Label (self, text = 'which well should be in front for the 3D snapshot?', bg= HIERNtheme.mywhite, fg=HIERNtheme.myblue, font = HIERNtheme.header_font)
        label_angle.grid(row=7, column=0, sticky=tk.W)

        self.variable.set('Select well')

        angles = ['A1', 'A8', 'F1', 'F8']

        opt = tk.OptionMenu(self, self.variable, *angles)
        opt.grid(row = 8, column = 0, sticky=tk.W)
        opt.config(bg=HIERNtheme.mylime)

        geometry_Label = Label(self, text='In which way should the 3D plots be alligned?', bg=HIERNtheme.mywhite, fg=HIERNtheme.myblue, font=HIERNtheme.header_font)
        geometry_Label.grid(row=10, columnspan=2)

        self.__toggle_button = Button(self, text="horizontal", bg=HIERNtheme.mygreen, fg=HIERNtheme.mywhite, font=HIERNtheme.standard_font, command= self.__Simpletoggle)
        self.__toggle_button.grid(row=11, column=0, sticky=tk.W)

        submit_Button = Button(self, text='submit', bg=HIERNtheme.myorange, fg=HIERNtheme.mywhite, font=HIERNtheme.standard_font, command=lambda:self.__submit(folder_selected, self.variable))
        submit_Button.grid(row=13, column=2)

        self.update_idletasks()
        self.deiconify()

    def __Simpletoggle(self):
        
        if self.__toggle_button.config('text')[-1] == 'vertical':
            self.__toggle_button.config(text='horizontal', bg=HIERNtheme.mygreen)
            self.__geometry.set('horizontal')
        else:
            self.__toggle_button.config(text='vertical', bg=HIERNtheme.myturquoise)
            self.__geometry.set('vertical')


    def __fill_list(self, key, k):

        # for k in range (0,48):
        #     # print(k)
        #     if MyUtils.plate[k] in MyUtils.chosen:
        #         for key in Raman_data_evaluation.LorentzFits_Raman[k*2].params:
                    # print(MyUtils.plate[k])
                    # print(Raman_data_evaluation.LorentzFits_Raman[k*2].params[key])
        if key == 'l1_center':
            # print('center')
            if Raman_data_evaluation.LorentzFits_Raman[k*2].params[key].value >= float(self.__startvalue.get()) and Raman_data_evaluation.LorentzFits_Raman[k*2].params[key].value <= float(self.__endvalue.get()):
                MyUtils.center_list.append(Raman_data_evaluation.LorentzFits_Raman[k*2].params[key].value)
                MyUtils.height_list.append(Raman_data_evaluation.LorentzFits_Raman[k*2].params['l1_height'].value)
                MyUtils.fwhm_list.append(Raman_data_evaluation.LorentzFits_Raman[k*2].params['l1_fwhm'].value)
                MyUtils.amplitude_list.append(Raman_data_evaluation.LorentzFits_Raman[k*2].params['l1_amplitude'].value)
                # print('yes')
                return
            else:
                MyUtils.center_list.append(0)
                MyUtils.height_list.append(0)
                MyUtils.fwhm_list.append(0)
                MyUtils.amplitude_list.append(0)


        elif key == 'l2_center':

            if Raman_data_evaluation.LorentzFits_Raman[k*2].params[key].value >= float(self.__startvalue.get()) and Raman_data_evaluation.LorentzFits_Raman[k*2].params[key].value <= float(self.__endvalue.get()):
                MyUtils.center_list.pop(k)
                MyUtils.height_list.pop(k)
                MyUtils.fwhm_list.pop(k)
                MyUtils.amplitude_list.pop(k)
                MyUtils.center_list.insert(k, Raman_data_evaluation.LorentzFits_Raman[k*2].params[key].value)
                MyUtils.height_list.insert(k, Raman_data_evaluation.LorentzFits_Raman[k*2].params['l2_height'].value)
                MyUtils.fwhm_list.insert(k, Raman_data_evaluation.LorentzFits_Raman[k*2].params['l2_fwhm'].value)
                MyUtils.amplitude_list.insert(k, Raman_data_evaluation.LorentzFits_Raman[k*2].params['l2_amplitude'].value)
                
                # MyUtils.center_list.append(Raman_data_evaluation.LorentzFits_Raman[k*2].params[key].value)
                # MyUtils.height_list.append(Raman_data_evaluation.LorentzFits_Raman[k*2].params['l2_height'].value)
                # MyUtils.fwhm_list.append(Raman_data_evaluation.LorentzFits_Raman[k*2].params['l2_fwhm'].value)
                # MyUtils.amplitude_list.append(Raman_data_evaluation.LorentzFits_Raman[k*2].params['l2_amplitude'].value)
                # print('yes')
                return

        elif key == 'l3_center':

            if Raman_data_evaluation.LorentzFits_Raman[k*2].params[key].value >= float(self.__startvalue.get()) and Raman_data_evaluation.LorentzFits_Raman[k*2].params[key].value <= float(self.__endvalue.get()):
                MyUtils.center_list.pop(k)
                MyUtils.height_list.pop(k)
                MyUtils.fwhm_list.pop(k)
                MyUtils.amplitude_list.pop(k)
                MyUtils.center_list.insert(k, Raman_data_evaluation.LorentzFits_Raman[k*2].params[key].value)
                MyUtils.height_list.insert(k, Raman_data_evaluation.LorentzFits_Raman[k*2].params['l3_height'].value)
                MyUtils.fwhm_list.insert(k, Raman_data_evaluation.LorentzFits_Raman[k*2].params['l3_fwhm'].value)
                MyUtils.amplitude_list.insert(k, Raman_data_evaluation.LorentzFits_Raman[k*2].params['l3_amplitude'].value)
                
                # MyUtils.center_list.append(Raman_data_evaluation.LorentzFits_Raman[k*2].params[key].value)
                # MyUtils.height_list.append(Raman_data_evaluation.LorentzFits_Raman[k*2].params['l3_height'].value)
                # MyUtils.fwhm_list.append(Raman_data_evaluation.LorentzFits_Raman[k*2].params['l3_fwhm'].value)
                # MyUtils.amplitude_list.append(Raman_data_evaluation.LorentzFits_Raman[k*2].params['l3_amplitude'].value)
                # print('yes')
                return

        elif key == 'l4_center':

            if Raman_data_evaluation.LorentzFits_Raman[k*2].params[key].value >= float(self.__startvalue.get()) and Raman_data_evaluation.LorentzFits_Raman[k*2].params[key].value <= float(self.__endvalue.get()):
                MyUtils.center_list.pop(k)
                MyUtils.height_list.pop(k)
                MyUtils.fwhm_list.pop(k)
                MyUtils.amplitude_list.pop(k)
                MyUtils.center_list.insert(k, Raman_data_evaluation.LorentzFits_Raman[k*2].params[key].value)
                MyUtils.height_list.insert(k, Raman_data_evaluation.LorentzFits_Raman[k*2].params['l4_height'].value)
                MyUtils.fwhm_list.insert(k, Raman_data_evaluation.LorentzFits_Raman[k*2].params['l4_fwhm'].value)
                MyUtils.amplitude_list.insert(k, Raman_data_evaluation.LorentzFits_Raman[k*2].params['l4_amplitude'].value)
                
                # MyUtils.center_list.append(Raman_data_evaluation.LorentzFits_Raman[k*2].params[key].value)
                # MyUtils.height_list.append(Raman_data_evaluation.LorentzFits_Raman[k*2].params['l4_height'].value)
                # MyUtils.fwhm_list.append(Raman_data_evaluation.LorentzFits_Raman[k*2].params['l4_fwhm'].value)
                # MyUtils.amplitude_list.append(Raman_data_evaluation.LorentzFits_Raman[k*2].params['l4_amplitude'].value)
                # print('yes')
                return

        elif key == 'l5_center':

            if Raman_data_evaluation.LorentzFits_Raman[k*2].params[key].value >= float(self.__startvalue.get()) and Raman_data_evaluation.LorentzFits_Raman[k*2].params[key].value <= float(self.__endvalue.get()):
                MyUtils.center_list.pop(k)
                MyUtils.height_list.pop(k)
                MyUtils.fwhm_list.pop(k)
                MyUtils.amplitude_list.pop(k)
                MyUtils.center_list.insert(k, Raman_data_evaluation.LorentzFits_Raman[k*2].params[key].value)
                MyUtils.height_list.insert(k, Raman_data_evaluation.LorentzFits_Raman[k*2].params['l5_height'].value)
                MyUtils.fwhm_list.insert(k, Raman_data_evaluation.LorentzFits_Raman[k*2].params['l5_fwhm'].value)
                MyUtils.amplitude_list.insert(k, Raman_data_evaluation.LorentzFits_Raman[k*2].params['l5_amplitude'].value)
                
                # MyUtils.center_list.append(Raman_data_evaluation.LorentzFits_Raman[k*2].params[key].value)
                # MyUtils.height_list.append(Raman_data_evaluation.LorentzFits_Raman[k*2].params['l5_height'].value)
                # MyUtils.fwhm_list.append(Raman_data_evaluation.LorentzFits_Raman[k*2].params['l5_fwhm'].value)
                # MyUtils.amplitude_list.append(Raman_data_evaluation.LorentzFits_Raman[k*2].params['l5_amplitude'].value)
                # print('yes')
                return

        elif key == 'l6_center':

            if Raman_data_evaluation.LorentzFits_Raman[k*2].params[key].value >= float(self.__startvalue.get()) and Raman_data_evaluation.LorentzFits_Raman[k*2].params[key].value <= float(self.__endvalue.get()):
                MyUtils.center_list.pop(k)
                MyUtils.height_list.pop(k)
                MyUtils.fwhm_list.pop(k)
                MyUtils.amplitude_list.pop(k)
                MyUtils.center_list.insert(k, Raman_data_evaluation.LorentzFits_Raman[k*2].params[key].value)
                MyUtils.height_list.insert(k, Raman_data_evaluation.LorentzFits_Raman[k*2].params['l6_height'].value)
                MyUtils.fwhm_list.insert(k, Raman_data_evaluation.LorentzFits_Raman[k*2].params['l6_fwhm'].value)
                MyUtils.amplitude_list.insert(k, Raman_data_evaluation.LorentzFits_Raman[k*2].params['l6_amplitude'].value)
                
                # MyUtils.center_list.append(Raman_data_evaluation.LorentzFits_Raman[k*2].params[key].value)
                # MyUtils.height_list.append(Raman_data_evaluation.LorentzFits_Raman[k*2].params['l6_height'].value)
                # MyUtils.fwhm_list.append(Raman_data_evaluation.LorentzFits_Raman[k*2].params['l6_fwhm'].value)
                # MyUtils.amplitude_list.append(Raman_data_evaluation.LorentzFits_Raman[k*2].params['l6_amplitude'].value)
                # print('yes')
                return

        elif key == 'l7_center':

            if Raman_data_evaluation.LorentzFits_Raman[k*2].params[key].value >= float(self.__startvalue.get()) and Raman_data_evaluation.LorentzFits_Raman[k*2].params[key].value <= float(self.__endvalue.get()):
                MyUtils.center_list.pop(k)
                MyUtils.height_list.pop(k)
                MyUtils.fwhm_list.pop(k)
                MyUtils.amplitude_list.pop(k)
                MyUtils.center_list.insert(k, Raman_data_evaluation.LorentzFits_Raman[k*2].params[key].value)
                MyUtils.height_list.insert(k, Raman_data_evaluation.LorentzFits_Raman[k*2].params['l7_height'].value)
                MyUtils.fwhm_list.insert(k, Raman_data_evaluation.LorentzFits_Raman[k*2].params['l7_fwhm'].value)
                MyUtils.amplitude_list.insert(k, Raman_data_evaluation.LorentzFits_Raman[k*2].params['l7_amplitude'].value)
                
                # MyUtils.center_list.append(Raman_data_evaluation.LorentzFits_Raman[k*2].params[key].value)
                # MyUtils.height_list.append(Raman_data_evaluation.LorentzFits_Raman[k*2].params['l7_height'].value)
                # MyUtils.fwhm_list.append(Raman_data_evaluation.LorentzFits_Raman[k*2].params['l7_fwhm'].value)
                # MyUtils.amplitude_list.append(Raman_data_evaluation.LorentzFits_Raman[k*2].params['l7_amplitude'].value)
                # print('yes')
                return

        elif key == 'l8_center':

            if Raman_data_evaluation.LorentzFits_Raman[k*2].params[key].value >= float(self.__startvalue.get()) and Raman_data_evaluation.LorentzFits_Raman[k*2].params[key].value <= float(self.__endvalue.get()):
                MyUtils.center_list.pop(k)
                MyUtils.height_list.pop(k)
                MyUtils.fwhm_list.pop(k)
                MyUtils.amplitude_list.pop(k)
                MyUtils.center_list.insert(k, Raman_data_evaluation.LorentzFits_Raman[k*2].params[key].value)
                MyUtils.height_list.insert(k, Raman_data_evaluation.LorentzFits_Raman[k*2].params['l8_height'].value)
                MyUtils.fwhm_list.insert(k, Raman_data_evaluation.LorentzFits_Raman[k*2].params['l8_fwhm'].value)
                MyUtils.amplitude_list.insert(k, Raman_data_evaluation.LorentzFits_Raman[k*2].params['l8_amplitude'].value)
                
                # MyUtils.center_list.append(Raman_data_evaluation.LorentzFits_Raman[k*2].params[key].value)
                # MyUtils.height_list.append(Raman_data_evaluation.LorentzFits_Raman[k*2].params['l8_height'].value)
                # MyUtils.fwhm_list.append(Raman_data_evaluation.LorentzFits_Raman[k*2].params['l8_fwhm'].value)
                # MyUtils.amplitude_list.append(Raman_data_evaluation.LorentzFits_Raman[k*2].params['l8_amplitude'].value)
                # print('yes')
                return


# else:
#     MyUtils.center_list.append(0)
#     # print('no no')

        # print(MyUtils.center_list)

    def __submit(self, folder_selected, variable):

        for k in range (0,48):
            # print(k)
            if MyUtils.plate[k] in MyUtils.chosen:
                for key in Raman_data_evaluation.LorentzFits_Raman[k*2].params:
                    self.__fill_list(key, k)
                    # print(k)
            else:
                MyUtils.center_list.append(0)
                MyUtils.height_list.append(0)
                MyUtils.amplitude_list.append(0)
                MyUtils.fwhm_list.append(0)
     #          print('no no')

        LorentzFits_Raman = Raman_data_evaluation.LorentzFits_Raman  
        Reports_Raman = Raman_data_evaluation.Reports_Raman
        x_Raman = Raman_data_evaluation.x_Raman
        Raman_data = Raman_data_evaluation.Raman_data
        local_max = Raman_data_evaluation.local_max
        maxima_list = Raman_data_evaluation.maxima_list

        maxima_list = Raman_data_evaluation.maxima_list
        problem = Raman_data_evaluation.problem

        save_files.save_Raman2(MyUtils.chosen, maxima_list, Reports_Raman, LorentzFits_Raman, problem, path.completeName11, path.completeName21, path.completeName22, path.completeName23, path.completeName24)
        print('done')

        # print('center ') 
        # print(len(MyUtils.center_list))
        # print(MyUtils.center_list)
        # print('height ')
        # print(len(MyUtils.height_list))
        # print(MyUtils.height_list)
        # print('fwhm ')
        # print(len(MyUtils.fwhm_list))
        # print(MyUtils.fwhm_list)
        # print('amplitude ')
        # print(len(MyUtils.amplitude_list))
        # print(MyUtils.amplitude_list)

        # print(Raman_data_evaluation.LorentzFits_Raman)

        dz1 = []
        dz2 = []
        dz3 = []
        dz4 = []

        plt.rcParams['font.size'] = '6'
        plt.rcParams['figure.constrained_layout.use'] = True

        red = [1.00, 0.84, 0.70, 0.56, 0.42, 0.28, 0.14, 0.00]
        green = [0.00, 0.20, 0.40, 0.60, 0.80, 1.00]
        blue = [0.00]
        alpha = [1.00]

        blub = [None]*48

        for i in range (0,48):
            for i in range (0,8):
                j = 0
                blub[i] = [red[i-8*j],green[j],blue[0],alpha[0]]
            for i in range (8,16):
                j = 1
                blub[i] = [red[i-8*j],green[j],blue[0],alpha[0]]
            for i in range (16,24):
                j = 2
                blub[i] = [red[i-8*j],green[j],blue[0],alpha[0]]
            for i in range (24,32):
                j = 3
                blub[i] = [red[i-8*j],green[j],blue[0],alpha[0]]
            for i in range (32,40):
                j = 4
                blub[i] = [red[i-8*j],green[j],blue[0],alpha[0]]
            for i in range (40,48):
                j = 5
                blub[i] = [red[i-8*j],green[j],blue[0],alpha[0]]

        result1 = np.array(MyUtils.height_list)
        result2 = np.array(MyUtils.center_list)
        result3 = np.array(MyUtils.amplitude_list)
        result4 = np.array(MyUtils.fwhm_list)

        print(self.__geometry.get())

        if self.__geometry.get() == 'horizontal':

            fig=plt.figure(figsize=(10, 2.5), dpi=100)

            ax1=fig.add_subplot(141, projection='3d')
            ax2=fig.add_subplot(142, projection='3d')
            ax3=fig.add_subplot(143, projection='3d')
            ax4=fig.add_subplot(144, projection='3d')

        elif self.__geometry.get() == 'vertical':

            fig=plt.figure(figsize=(2.5, 10), dpi=100)

            ax1=fig.add_subplot(411, projection='3d')
            ax2=fig.add_subplot(412, projection='3d')
            ax3=fig.add_subplot(413, projection='3d')
            ax4=fig.add_subplot(414, projection='3d')

        if self.variable.get() == 'A1':
            
            ax1.view_init(azim=0)
            ax2.view_init(azim=0)
            ax3.view_init(azim=0)
            ax4.view_init(azim=0)
        
        elif self.variable.get() == 'A8':

            ax1.view_init(azim=270)
            ax2.view_init(azim=270)
            ax3.view_init(azim=270)
            ax4.view_init(azim=270)

        elif self.variable.get() == 'F1':

            ax1.view_init(azim=90)
            ax2.view_init(azim=90)
            ax3.view_init(azim=90)
            ax4.view_init(azim=90)

        elif self.variable.get() == 'F8':

            ax1.view_init(azim=180)
            ax2.view_init(azim=180)
            ax3.view_init(azim=180)
            ax4.view_init(azim=180)


        ax1.set_title(self.__name.get() + ' height')
        ax2.set_title(self.__name.get() + ' center')
        ax3.set_title(self.__name.get() + ' amplitude')
        ax4.set_title(self.__name.get() + ' fwhm')


        ylabels = np.array(['A', 'B', 'C', 'D', 'E', 'F'])
        xlabels = np.array(['1','2','3','4','5','6','7', '8'])
        xpos = np.arange(xlabels.shape[0])
        ypos = np.arange(ylabels.shape[0])

        xposM, yposM = np.meshgrid(xpos, ypos, copy=False)

        # subplot 1

        zpos1=result1
        zpos1 = zpos1.ravel()

        dx=0.8
        dy=0.8
        dz1=zpos1

        ax1.w_xaxis.set_ticks(xpos + dx/2.)
        ax1.w_xaxis.set_ticklabels(xlabels,  fontsize = 6)

        ax1.w_yaxis.set_ticks(ypos + dy/2.)
        ax1.w_yaxis.set_ticklabels(ylabels,  fontsize = 6)
        ax1.invert_xaxis()

        ax1.FontSize = 8
        #ax1.view_init(azim=self.__angle1)

        ax1.bar3d(xposM.ravel(), yposM.ravel(), dz1*0, dx, dy, dz1, color=blub)

        fig.patch.set_facecolor(HIERNtheme.mywhite)

        # subplot 2

        zpos2=result2
        zpos2 = zpos2.ravel()

        dx=0.8
        dy=0.8
        dz2=zpos2

        ax2.w_xaxis.set_ticks(xpos + dx/2.)
        ax2.w_xaxis.set_ticklabels(xlabels,  fontsize = 6)

        ax2.w_yaxis.set_ticks(ypos + dy/2.)
        ax2.w_yaxis.set_ticklabels(ylabels,  fontsize = 6)
        ax2.invert_xaxis()

        ax2.FontSize = 8
        #ax2.view_init(azim=self.__angle2)

        ax2.bar3d(xposM.ravel(), yposM.ravel(), dz2*0, dx, dy, dz2, color=blub)

        # subplot 3

        zpos3=result3
        zpos3 = zpos3.ravel()

        dx=0.8
        dy=0.8
        dz3=zpos3

        ax3.w_xaxis.set_ticks(xpos + dx/2.)
        ax3.w_xaxis.set_ticklabels(xlabels,  fontsize = 6)

        ax3.w_yaxis.set_ticks(ypos + dy/2.)
        ax3.w_yaxis.set_ticklabels(ylabels,  fontsize = 6)
        ax3.invert_xaxis()

        ax3.FontSize = 8
        #ax3.view_init(azim=self.__angle3)

        ax3.bar3d(xposM.ravel(), yposM.ravel(), dz3*0, dx, dy, dz3, color=blub)

        # subplot 4

        zpos4=result4
        zpos4 = zpos4.ravel()

        dx=0.8
        dy=0.8
        dz4=zpos4

        ax4.w_xaxis.set_ticks(xpos + dx/2.)
        ax4.w_xaxis.set_ticklabels(xlabels, fontsize = 6)

        ax4.w_yaxis.set_ticks(ypos + dy/2.)
        ax4.w_yaxis.set_ticklabels(ylabels, fontsize = 6)
        ax4.invert_xaxis()

        ax4.FontSize = 8
        #ax4.view_init(azim=self.__angle4)

        ax4.bar3d(xposM.ravel(), yposM.ravel(), dz4*0, dx, dy, dz4, color=blub)

        fig.patch.set_facecolor(HIERNtheme.mywhite)

        #if self.__save_v == 'on':
        folderPath = folder_selected
        video = self.__geometry + "3D_animation_" + self.__name.get() +".png"
        completename10 = os.path.join(path.completeName7, video)

        plt.savefig(completename10, transparent = False)

        # ----------------------------------------------#

        #fig = plt.figure()
        #ax = fig.add_subplot(111, projection='3d')

        # load some test data for demonstration and plot a wireframe
        #X, Y, Z = axes3d.get_test_data(0.1)
        #ax.grid(False)
        #ax1.set_axis_off()
        #ax2.set_axis_off()
        #ax3.set_axis_off()
        #ax4.set_axis_off()

        def init():
            ax1.bar3d(xposM.ravel(), yposM.ravel(), dz1*0, dx, dy, dz1, color=blub)
            ax2.bar3d(xposM.ravel(), yposM.ravel(), dz2*0, dx, dy, dz2, color=blub)
            ax3.bar3d(xposM.ravel(), yposM.ravel(), dz3*0, dx, dy, dz3, color=blub)
            ax4.bar3d(xposM.ravel(), yposM.ravel(), dz4*0, dx, dy, dz4, color=blub)
            return fig,

        def animate(i):
            ax1.view_init(elev=30., azim=1.0*i)
            ax2.view_init(elev=30., azim=1.0*i)
            ax3.view_init(elev=30., azim=1.0*i)
            ax4.view_init(elev=30., azim=1.0*i)
            return fig,

        # Animate
        ani = animation.FuncAnimation(fig, animate, init_func=init,
                                    frames=360, interval=200, blit=False)  


        folderPath = folder_selected
        snapshot = self.__geometry + "3D_animation_" + self.__name.get() +".mp4"
        completename11 = os.path.join(path.completeName7, snapshot)

        f = completename11 
        writervideo = animation.FFMpegWriter(fps=60) 
        ani.save(f, writer=writervideo)  

        #g = r"c://Users/xx/Desktop/animation.gif" 
        #writergif = animation.PillowWriter(fps=30) 
        #ani.save(g, writer=writergif)

        #HTML(ani.to_html5_video())

        #with open("myvideo2.html", "w") as f:
        #    print(ani.to_html5_video(), file=f)

        # -------------------------------------------------- #

        #canvas = FigureCanvasTkAgg(fig, self)
        #canvas.draw()

        # placing the canvas on the Tkinter self
        #canvas.get_tk_widget().grid(row = 15, column = 0, columnspan = 12, sticky=tk.W)

        
        #self.__save_v = 'off'

        plt.show()
        self.destroy()
