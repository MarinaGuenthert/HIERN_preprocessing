import matplotlib.pyplot as plt
import tkinter as tk
import numpy
import os

from myutils import MyUtils
from PLE_fit import PLE_Tecan_fit
from joining import path
from theme import HIERNtheme

from tkinter import Tk, Label, Button



class PLE_Tecan_plot(tk.Toplevel):
    
    def __init__(self, master: Tk):
        tk.Toplevel.__init__(self)
        
        self.row = tk.StringVar()
        self.column = tk.StringVar()
        #self.__variable = MyUtils.plate[0]
        
        self.withdraw()
        self.lift(master) 
        
        icon_path = MyUtils.get_absolute_path('resources\HIERN_icon.ico')
        self.iconbitmap(icon_path)    

    def overlaying_plot(self):

        self.configure(background=HIERNtheme.mywhite)

        label_row = Label (self, text = 'which row would you like to evaluate?', bg= HIERNtheme.mywhite, fg=HIERNtheme.myblue, font = HIERNtheme.header_font)
        label_row.grid(row=1, column=0, sticky=tk.W)

        self.row.set('Select row')

        rows = ['A', 'B', 'C', 'D', 'E', 'F']

        opt = tk.OptionMenu(self, self.row, *rows)
        opt.grid(row = 2, column = 0, sticky=tk.W)
        opt.config(bg=HIERNtheme.mylime)

        label_column = Label (self, text = 'which column would you like to evaluate?', bg= HIERNtheme.mywhite, fg=HIERNtheme.myblue, font = HIERNtheme.header_font)
        label_column.grid(row=4, column=0, sticky=tk.W)

        self.column.set('Select column')

        columns = ['1', '2', '3', '4', '5', '6', '7', '8']

        opt = tk.OptionMenu(self, self.column, *columns)
        opt.grid(row = 5, column = 0, sticky=tk.W)
        opt.config(bg=HIERNtheme.mylime)

        submit_Button = Button(self, text='submit', bg=HIERNtheme.myorange, fg=HIERNtheme.mywhite, font=HIERNtheme.standard_font, command=lambda:self.__PLE_double_plotting(self.row.get(), self.column.get()))
        submit_Button.grid(row=10, column=5)

        self.update_idletasks()
        self.deiconify()

    def __PLE_double_plotting(self, row, column):

    
        red = [1.00, 0.84, 0.70, 0.56, 0.42, 0.28, 0.14, 0.00]
        green = [0.00, 0.20, 0.40, 0.60, 0.80, 1.00]
        blue = [0.00]
        alpha = [1.00]

        fig, axs = plt.subplots(1, 2, sharex=True, sharey=True, figsize = (10,5))

        fig.text(0.5, 0.0, 'energy [eV]', ha='center')
        fig.text(0.0, 0.5, 'intensity', va='center', rotation='vertical')

        axs[0].set_title('row ' + str(self.row.get()))
        axs[1].set_title('column ' + str(self.column.get()))

        # for i in range(0,48):
            
        if self.row.get() == 'A':
            for i in range(0,8):
                j = 0
                if MyUtils.plate[i] in MyUtils.chosen:
                    axs[0].plot(PLE_Tecan_fit.PLE_data.iloc[:,49], PLE_Tecan_fit.PLE_data.iloc[:,i+1], color=[red[i-8*j],green[j],blue[0],alpha[0]], linewidth=1.5, label=MyUtils.plate[i])
                    axs[0].plot(PLE_Tecan_fit.PLE_data.iloc[:,49], PLE_Tecan_fit.GaussFits_PLE[i].best_fit, '--', color=[0.38,0.38,0.38,1], linewidth=1.5, label=str(MyUtils.plate[i]+' fit'))

        if self.row.get() == 'B':
            for i in range(8,16):
                j = 1
                if MyUtils.plate[i] in MyUtils.chosen:
                    axs[0].plot(PLE_Tecan_fit.PLE_data.iloc[:,49], PLE_Tecan_fit.PLE_data.iloc[:,i+1], color=[red[i-8*j],green[j],blue[0],alpha[0]], linewidth=1.5, label=MyUtils.plate[i])
                    axs[0].plot(PLE_Tecan_fit.PLE_data.iloc[:,49], PLE_Tecan_fit.GaussFits_PLE[i].best_fit, '--', color=[0.38,0.38,0.38,1], linewidth=1.5, label=str(MyUtils.plate[i]+' fit'))

        if self.row.get() == 'C':
            for i in range(16,24):
                j = 2
                if MyUtils.plate[i] in MyUtils.chosen:
                    axs[0].plot(PLE_Tecan_fit.PLE_data.iloc[:,49], PLE_Tecan_fit.PLE_data.iloc[:,i+1], color=[red[i-8*j],green[j],blue[0],alpha[0]], linewidth=1.5, label=MyUtils.plate[i])
                    axs[0].plot(PLE_Tecan_fit.PLE_data.iloc[:,49], PLE_Tecan_fit.GaussFits_PLE[i].best_fit, '--', color=[0.38,0.38,0.38,1], linewidth=1.5, label=str(MyUtils.plate[i]+' fit'))

        if self.row.get() == 'D':
            for i in range(24,32):
                j = 3
                if MyUtils.plate[i] in MyUtils.chosen:
                    axs[0].plot(PLE_Tecan_fit.PLE_data.iloc[:,49], PLE_Tecan_fit.PLE_data.iloc[:,i+1], color=[red[i-8*j],green[j],blue[0],alpha[0]], linewidth=1.5, label=MyUtils.plate[i])
                    axs[0].plot(PLE_Tecan_fit.PLE_data.iloc[:,49], PLE_Tecan_fit.GaussFits_PLE[i].best_fit, '--', color=[0.38,0.38,0.38,1], linewidth=1.5, label=str(MyUtils.plate[i]+' fit'))

        if self.row.get() == 'E':
            for i in range(32,40):
                j = 4
                if MyUtils.plate[i] in MyUtils.chosen:
                    axs[0].plot(PLE_Tecan_fit.PLE_data.iloc[:,49], PLE_Tecan_fit.PLE_data.iloc[:,i+1], color=[red[i-8*j],green[j],blue[0],alpha[0]], linewidth=1.5, label=MyUtils.plate[i])
                    axs[0].plot(PLE_Tecan_fit.PLE_data.iloc[:,49], PLE_Tecan_fit.GaussFits_PLE[i].best_fit, '--', color=[0.38,0.38,0.38,1], linewidth=1.5, label=str(MyUtils.plate[i]+' fit'))

        if self.row.get() == 'F':
            for i in range(40,48):
                j = 5
                if MyUtils.plate[i] in MyUtils.chosen:
                    axs[0].plot(PLE_Tecan_fit.PLE_data.iloc[:,49], PLE_Tecan_fit.PLE_data.iloc[:,i+1], color=[red[i-8*j],green[j],blue[0],alpha[0]], linewidth=1.5, label=MyUtils.plate[i])
                    axs[0].plot(PLE_Tecan_fit.PLE_data.iloc[:,49], PLE_Tecan_fit.GaussFits_PLE[i].best_fit, '--', color=[0.38,0.38,0.38,1], linewidth=1.5, label=str(MyUtils.plate[i]+' fit'))

        if self.column.get() == '1':
            for i in range (0,48,8):
                j = int(i/8)
                if MyUtils.plate[i] in MyUtils.chosen:
                    axs[1].plot(PLE_Tecan_fit.PLE_data.iloc[:,49], PLE_Tecan_fit.PLE_data.iloc[:,i+1], color=[red[i-8*j],green[j],blue[0],alpha[0]], linewidth=1.5, label=MyUtils.plate[i])
                    axs[1].plot(PLE_Tecan_fit.PLE_data.iloc[:,49], PLE_Tecan_fit.GaussFits_PLE[i].best_fit, '--', color=[0.38,0.38,0.38,1], linewidth=1.5, label=str(MyUtils.plate[i]+' fit'))
                

        if self.column.get() == '2':
            for i in range (0,48,8):
                j = int(i/8)
                if MyUtils.plate[i] in MyUtils.chosen:
                    axs[1].plot(PLE_Tecan_fit.PLE_data.iloc[:,49], PLE_Tecan_fit.PLE_data.iloc[:,i+2], color=[red[i+1-8*j],green[j],blue[0],alpha[0]], linewidth=1.5, label=str(MyUtils.plate[i+1]))
                    axs[1].plot(PLE_Tecan_fit.PLE_data.iloc[:,49], PLE_Tecan_fit.GaussFits_PLE[i+1].best_fit, '--', color=[0.38,0.38,0.38,1], linewidth=1.5, label=str(MyUtils.plate[i+1]+' fit'))  
                

        if self.column.get() == '3':
            for i in range (0,48,8):
                j = int(i/8)
                if MyUtils.plate[i] in MyUtils.chosen:
                    axs[1].plot(PLE_Tecan_fit.PLE_data.iloc[:,49], PLE_Tecan_fit.PLE_data.iloc[:,i+3], color=[red[i+2-8*j],green[j],blue[0],alpha[0]], linewidth=1.5, label=MyUtils.plate[i+2])
                    axs[1].plot(PLE_Tecan_fit.PLE_data.iloc[:,49], PLE_Tecan_fit.GaussFits_PLE[i+2].best_fit, '--', color=[0.38,0.38,0.38,1], linewidth=1.5, label=str(MyUtils.plate[i+2]+' fit'))  
                

        if self.column.get() == '4':
            for i in range (0,48,8):
                j = int(i/8)
                if MyUtils.plate[i] in MyUtils.chosen:
                    axs[1].plot(PLE_Tecan_fit.PLE_data.iloc[:,49], PLE_Tecan_fit.PLE_data.iloc[:,i+4], color=[red[i+3-8*j],green[j],blue[0],alpha[0]], linewidth=1.5, label=MyUtils.plate[i+3])
                    axs[1].plot(PLE_Tecan_fit.PLE_data.iloc[:,49], PLE_Tecan_fit.GaussFits_PLE[i+3].best_fit, '--', color=[0.38,0.38,0.38,1], linewidth=1.5, label=str(MyUtils.plate[i+3]+' fit'))            
                

        if self.column.get() == '5':
            for i in range (0,48,8):
                j = int(i/8)
                if MyUtils.plate[i] in MyUtils.chosen:
                    axs[1].plot(PLE_Tecan_fit.PLE_data.iloc[:,49], PLE_Tecan_fit.PLE_data.iloc[:,i+5], color=[red[i+4-8*j],green[j],blue[0],alpha[0]], linewidth=1.5, label=MyUtils.plate[i+4])
                    axs[1].plot(PLE_Tecan_fit.PLE_data.iloc[:,49], PLE_Tecan_fit.GaussFits_PLE[i+4].best_fit, '--', color=[0.38,0.38,0.38,1], linewidth=1.5, label=str(MyUtils.plate[i+4]+' fit')) 
                

        if self.column.get() == '6':
            for i in range (0,48,8):
                j = int(i/8)
                if MyUtils.plate[i] in MyUtils.chosen:
                    axs[1].plot(PLE_Tecan_fit.PLE_data.iloc[:,49], PLE_Tecan_fit.PLE_data.iloc[:,i+6], color=[red[i+5-8*j],green[j],blue[0],alpha[0]], linewidth=1.5, label=MyUtils.plate[i+5])
                    axs[1].plot(PLE_Tecan_fit.PLE_data.iloc[:,49], PLE_Tecan_fit.GaussFits_PLE[i+5].best_fit, '--', color=[0.38,0.38,0.38,1], linewidth=1.5, label=str(MyUtils.plate[i+5]+' fit'))  
                

        if self.column.get() == '7':
            for i in range (0,48,8):
                j = int(i/8)
                if MyUtils.plate[i] in MyUtils.chosen:
                    axs[1].plot(PLE_Tecan_fit.PLE_data.iloc[:,49], PLE_Tecan_fit.PLE_data.iloc[:,i+7], color=[red[i+6-8*j],green[j],blue[0],alpha[0]], linewidth=1.5, label=MyUtils.plate[i+6])
                    axs[1].plot(PLE_Tecan_fit.PLE_data.iloc[:,49], PLE_Tecan_fit.GaussFits_PLE[i+6].best_fit, '--', color=[0.38,0.38,0.38,1], linewidth=1.5, label=str(MyUtils.plate[i+6]+' fit'))  
                

        if self.column.get() == '8':
            for i in range (0,48,8):
                j = int(i/8)
                if MyUtils.plate[i] in MyUtils.chosen:   
                    axs[1].plot(PLE_Tecan_fit.PLE_data.iloc[:,49], PLE_Tecan_fit.PLE_data.iloc[:,i+8], color=[red[i+7-8*j],green[j],blue[0],alpha[0]], linewidth=1.5, label=MyUtils.plate[i+7])
                    axs[1].plot(PLE_Tecan_fit.PLE_data.iloc[:,49], PLE_Tecan_fit.GaussFits_PLE[i+7].best_fit, '--', color=[0.38,0.38,0.38,1], linewidth=1.5, label=str(MyUtils.plate[i+7]+' fit'))   
                    

        for ax in axs.flat:
            ax.label_outer()

        fig.tight_layout()
        fig.patch.set_facecolor(HIERNtheme.mywhite)
        single_fit = 'row_' + str(self.row.get()) + '_column_' + str(self.column.get()) + '.png'
        cName8 = os.path.join(path.completeName0, single_fit)
        axs[0].legend(loc='upper right')
        axs[1].legend(loc='upper right')
        plt.legend
        plt.savefig(cName8, transparent = False)
    

        plt.show() 

    def PLE_plotting(chosen, PLE_data, GaussFits_PLE,  completeName1, self):


        #MyUtils.plate = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8']

        red = [1.00, 0.84, 0.70, 0.56, 0.42, 0.28, 0.14, 0.00]
        green = [0.00, 0.20, 0.40, 0.60, 0.80, 1.00]
        blue = [0.00]
        alpha = [1.00]

        #fig = plt.figure()

        fig, axs = plt.subplots(6, 8, sharex=True, sharey=True, figsize = (20,15))

        fig.text(0.5, 0.0, 'energy [eV]', ha='center')
        fig.text(0.0, 0.5, 'intensity', va='center', rotation='vertical')

        i = 0
        #j = 0

        for i in range(0,49):
            for i in range(0,8):
                j = 0
                axs[j,i-8*j].set_title(MyUtils.plate[i])
                if MyUtils.plate[i] in MyUtils.chosen:
                    axs[j,i-8*j].plot(PLE_Tecan_fit.PLE_data.iloc[:,49], PLE_Tecan_fit.PLE_data.iloc[:,i+1], color=[red[i-8*j],green[j],blue[0],alpha[0]], linewidth=1.5)
                    axs[j,i-8*j].plot(PLE_Tecan_fit.PLE_data.iloc[:,49], PLE_Tecan_fit.GaussFits_PLE[i].best_fit, '--', color=[0.38,0.38,0.38,1], linewidth=1.5)
            for i in range(8,16):
                j = 1
                axs[j,i-8*j].set_title(MyUtils.plate[i])
                if MyUtils.plate[i] in MyUtils.chosen:
                    axs[j,i-8*j].plot(PLE_Tecan_fit.PLE_data.iloc[:,49], PLE_Tecan_fit.PLE_data.iloc[:,i+1], color=[red[i-8*j],green[j],blue[0],alpha[0]], linewidth=1.5)
                    axs[j,i-8*j].plot(PLE_Tecan_fit.PLE_data.iloc[:,49], PLE_Tecan_fit.GaussFits_PLE[i].best_fit, '--', color=[0.38,0.38,0.38,1], linewidth=1.5)
            for i in range(16,24):
                j = 2
                axs[j,i-8*j].set_title(MyUtils.plate[i])
                if MyUtils.plate[i] in MyUtils.chosen:
                    axs[j,i-8*j].plot(PLE_Tecan_fit.PLE_data.iloc[:,49], PLE_Tecan_fit.PLE_data.iloc[:,i+1], color=[red[i-8*j],green[j],blue[0],alpha[0]], linewidth=1.5)
                    axs[j,i-8*j].plot(PLE_Tecan_fit.PLE_data.iloc[:,49], PLE_Tecan_fit.GaussFits_PLE[i].best_fit, '--', color=[0.38,0.38,0.38,1], linewidth=1.5)
            for i in range(24,32):
                j = 3
                axs[j,i-8*j].set_title(MyUtils.plate[i])
                if MyUtils.plate[i] in MyUtils.chosen:
                    axs[j,i-8*j].plot(PLE_Tecan_fit.PLE_data.iloc[:,49], PLE_Tecan_fit.PLE_data.iloc[:,i+1], color=[red[i-8*j],green[j],blue[0],alpha[0]], linewidth=1.5)
                    axs[j,i-8*j].plot(PLE_Tecan_fit.PLE_data.iloc[:,49], PLE_Tecan_fit.GaussFits_PLE[i].best_fit, '--', color=[0.38,0.38,0.38,1], linewidth=1.5)
            for i in range(32,40):
                j = 4
                axs[j,i-8*j].set_title(MyUtils.plate[i])
                if MyUtils.plate[i] in MyUtils.chosen:
                    axs[j,i-8*j].plot(PLE_Tecan_fit.PLE_data.iloc[:,49], PLE_Tecan_fit.PLE_data.iloc[:,i+1], color=[red[i-8*j],green[j],blue[0],alpha[0]], linewidth=1.5)
                    axs[j,i-8*j].plot(PLE_Tecan_fit.PLE_data.iloc[:,49], PLE_Tecan_fit.GaussFits_PLE[i].best_fit, '--', color=[0.38,0.38,0.38,1], linewidth=1.5)
            for i in range(40,48):
                j = 5
                axs[j,i-8*j].set_title(MyUtils.plate[i])
                if MyUtils.plate[i] in MyUtils.chosen:
                    axs[j,i-8*j].plot(PLE_Tecan_fit.PLE_data.iloc[:,49], PLE_Tecan_fit.PLE_data.iloc[:,i+1], color=[red[i-8*j],green[j],blue[0],alpha[0]], linewidth=1.5)
                    axs[j,i-8*j].plot(PLE_Tecan_fit.PLE_data.iloc[:,49], PLE_Tecan_fit.GaussFits_PLE[i].best_fit, '--', color=[0.38,0.38,0.38,1], linewidth=1.5)
                
                
        for ax in axs.flat:
            ax.label_outer()


        fig.tight_layout()
        fig.patch.set_facecolor('white')
        plt.savefig(path.completeName1, transparent = False)
        plt.show()


    def PLE_plotting_norm(chosen, PLE_data, PLE_data_norm, GaussFits_PLE_norm, completeName2, self):

        # normalized plotting

        #MyUtils.plate = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8']

        red = [1.00, 0.84, 0.70, 0.56, 0.42, 0.28, 0.14, 0.00]
        green = [0.00, 0.20, 0.40, 0.60, 0.80, 1.00]
        blue = [0.00]
        alpha = [1.00]

        #fig = plt.figure()

        fig, axs = plt.subplots(6, 8, sharex=True, sharey=True, figsize = (20,15))

        plt.ylim(0, 1.1)

        fig.text(0.5, 0.0, 'energy [eV]', ha='center')
        fig.text(0.0, 0.5, 'normalized intensity', va='center', rotation='vertical')

        i = 0
        #j = 0

        for i in range(0,49):
            for i in range(0,8):
                j = 0
                axs[j,i-8*j].set_title(MyUtils.plate[i])
                if MyUtils.plate[i] in MyUtils.chosen:
                    axs[j,i-8*j].plot(PLE_Tecan_fit.PLE_data.iloc[:,49], PLE_Tecan_fit.PLE_data_norm[i], color=[red[i-8*j],green[j],blue[0],alpha[0]], linewidth=1.5)
                    axs[j,i-8*j].plot(PLE_Tecan_fit.PLE_data.iloc[:,49], PLE_Tecan_fit.GaussFits_PLE_norm[i], '--', color=[0.38,0.38,0.38,1], linewidth=1.5)
            for i in range(8,16):
                j = 1
                axs[j,i-8*j].set_title(MyUtils.plate[i])
                if MyUtils.plate[i] in MyUtils.chosen:
                    axs[j,i-8*j].plot(PLE_Tecan_fit.PLE_data.iloc[:,49], PLE_Tecan_fit.PLE_data_norm[i], color=[red[i-8*j],green[j],blue[0],alpha[0]], linewidth=1.5)
                    axs[j,i-8*j].plot(PLE_Tecan_fit.PLE_data.iloc[:,49], PLE_Tecan_fit.GaussFits_PLE_norm[i], '--', color=[0.38,0.38,0.38,1], linewidth=1.5)
            for i in range(16,24):
                j = 2
                axs[j,i-8*j].set_title(MyUtils.plate[i])
                if MyUtils.plate[i] in MyUtils.chosen:
                    axs[j,i-8*j].plot(PLE_Tecan_fit.PLE_data.iloc[:,49], PLE_Tecan_fit.PLE_data_norm[i], color=[red[i-8*j],green[j],blue[0],alpha[0]], linewidth=1.5)
                    axs[j,i-8*j].plot(PLE_Tecan_fit.PLE_data.iloc[:,49], PLE_Tecan_fit.GaussFits_PLE_norm[i], '--', color=[0.38,0.38,0.38,1], linewidth=1.5)
            for i in range(24,32):
                j = 3
                axs[j,i-8*j].set_title(MyUtils.plate[i])
                if MyUtils.plate[i] in MyUtils.chosen:
                    axs[j,i-8*j].plot(PLE_Tecan_fit.PLE_data.iloc[:,49], PLE_Tecan_fit.PLE_data_norm[i], color=[red[i-8*j],green[j],blue[0],alpha[0]], linewidth=1.5)
                    axs[j,i-8*j].plot(PLE_Tecan_fit.PLE_data.iloc[:,49], PLE_Tecan_fit.GaussFits_PLE_norm[i], '--', color=[0.38,0.38,0.38,1], linewidth=1.5)
            for i in range(32,40):
                j = 4
                axs[j,i-8*j].set_title(MyUtils.plate[i])
                if MyUtils.plate[i] in MyUtils.chosen:
                    axs[j,i-8*j].plot(PLE_Tecan_fit.PLE_data.iloc[:,49], PLE_Tecan_fit.PLE_data_norm[i], color=[red[i-8*j],green[j],blue[0],alpha[0]], linewidth=1.5)
                    axs[j,i-8*j].plot(PLE_Tecan_fit.PLE_data.iloc[:,49], PLE_Tecan_fit.GaussFits_PLE_norm[i], '--', color=[0.38,0.38,0.38,1], linewidth=1.5)
            for i in range(40,48):
                j = 5
                axs[j,i-8*j].set_title(MyUtils.plate[i])
                if MyUtils.plate[i] in MyUtils.chosen:
                    axs[j,i-8*j].plot(PLE_Tecan_fit.PLE_data.iloc[:,49], PLE_Tecan_fit.PLE_data_norm[i], color=[red[i-8*j],green[j],blue[0],alpha[0]], linewidth=1.5)
                    axs[j,i-8*j].plot(PLE_Tecan_fit.PLE_data.iloc[:,49], PLE_Tecan_fit.GaussFits_PLE_norm[i], '--', color=[0.38,0.38,0.38,1], linewidth=1.5)
                
        for ax in axs.flat:
            ax.label_outer()


        fig.tight_layout()
        fig.patch.set_facecolor('white')
        plt.savefig(path.completeName2, transparent = False)
        plt.show()



    def PLE_plotting_Eg(chosen, PLE_data,LinearFits_Eg, GaussCurvesT, max_index, completeName5, self):

        # bandgap extrapolation plotting

        #MyUtils.plate = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8']

        red = [1.00, 0.84, 0.70, 0.56, 0.42, 0.28, 0.14, 0.00]
        green = [0.00, 0.20, 0.40, 0.60, 0.80, 1.00]
        blue = [0.00]
        alpha = [1.00]

        #fig = plt.figure()

        fig, axs = plt.subplots(6, 8, sharex=True, sharey=True, figsize = (20,15))

        #plt.xlim(1.75, 2.0)
        #plt.ylim(0, 1.1)

        fig.text(0.5, 0.0, 'energy [eV]', ha='center')
        fig.text(0.0, 0.5, 'normalized intensity', va='center', rotation='vertical')

        #i = 0
        #j = 0

        for i in range(0,49):
            for i in range(0,8):
                j = 0
                axs[j,i-8*j].set_title(MyUtils.plate[i])
                if isinstance(PLE_Tecan_fit.max_index[i], numpy.integer) == True:
                    if PLE_Tecan_fit.max_index[i] <= 245:
                        xPLE = PLE_Tecan_fit.PLE_data.iloc[int(PLE_Tecan_fit.max_index[i]+15):int(PLE_Tecan_fit.max_index[i]+45),49]
                        if MyUtils.plate[i] in MyUtils.chosen:
                            axs[j,i-8*j].plot(xPLE, PLE_Tecan_fit.LinearFits_Eg[i].best_fit, color=[red[i-8*j],green[j],blue[0],alpha[0]], linewidth=1.5)
                            axs[j,i-8*j].plot(xPLE, PLE_Tecan_fit.GaussCurvesT.iloc[PLE_Tecan_fit.max_index[i]+15:PLE_Tecan_fit.max_index[i]+45,i], '--', color=[0.38,0.38,0.38,1], linewidth=1.5)
            for i in range(8,16):
                j = 1
                axs[j,i-8*j].set_title(MyUtils.plate[i])
                if isinstance(PLE_Tecan_fit.max_index[i], numpy.integer) == True:
                    if PLE_Tecan_fit.max_index[i] <= 245:
                        xPLE = PLE_Tecan_fit.PLE_data.iloc[int(PLE_Tecan_fit.max_index[i]+15):int(PLE_Tecan_fit.max_index[i]+45),49]
                        # axs[j,i-8*j].set_title(MyUtils.plate[i])
                        if MyUtils.plate[i] in MyUtils.chosen:
                            axs[j,i-8*j].plot(xPLE, PLE_Tecan_fit.LinearFits_Eg[i].best_fit, color=[red[i-8*j],green[j],blue[0],alpha[0]], linewidth=1.5)
                            axs[j,i-8*j].plot(xPLE, PLE_Tecan_fit.GaussCurvesT.iloc[PLE_Tecan_fit.max_index[i]+15:PLE_Tecan_fit.max_index[i]+45,i], '--', color=[0.38,0.38,0.38,1], linewidth=1.5)
            for i in range(16,24):
                j = 2
                axs[j,i-8*j].set_title(MyUtils.plate[i])
                if isinstance(PLE_Tecan_fit.max_index[i], numpy.integer) == True:
                    if PLE_Tecan_fit.max_index[i] <= 245:
                        xPLE = PLE_Tecan_fit.PLE_data.iloc[int(PLE_Tecan_fit.max_index[i]+15):int(PLE_Tecan_fit.max_index[i]+45),49]
                        # j = 2
                        # axs[j,i-8*j].set_title(MyUtils.plate[i])
                        if MyUtils.plate[i] in MyUtils.chosen:
                            axs[j,i-8*j].plot(xPLE, PLE_Tecan_fit.LinearFits_Eg[i].best_fit, color=[red[i-8*j],green[j],blue[0],alpha[0]], linewidth=1.5)
                            axs[j,i-8*j].plot(xPLE, PLE_Tecan_fit.GaussCurvesT.iloc[PLE_Tecan_fit.max_index[i]+15:PLE_Tecan_fit.max_index[i]+45,i], '--', color=[0.38,0.38,0.38,1], linewidth=1.5)
            for i in range(24,32):
                j = 3
                axs[j,i-8*j].set_title(MyUtils.plate[i])
                if isinstance(PLE_Tecan_fit.max_index[i], numpy.integer) == True:
                    if PLE_Tecan_fit.max_index[i] <= 245:
                        xPLE = PLE_Tecan_fit.PLE_data.iloc[int(PLE_Tecan_fit.max_index[i]+15):int(PLE_Tecan_fit.max_index[i]+45),49]
                        # j = 3
                        # axs[j,i-8*j].set_title(MyUtils.plate[i])
                        if MyUtils.plate[i] in MyUtils.chosen:
                            axs[j,i-8*j].plot(xPLE, PLE_Tecan_fit.LinearFits_Eg[i].best_fit, color=[red[i-8*j],green[j],blue[0],alpha[0]], linewidth=1.5)
                            axs[j,i-8*j].plot(xPLE, PLE_Tecan_fit.GaussCurvesT.iloc[PLE_Tecan_fit.max_index[i]+15:PLE_Tecan_fit.max_index[i]+45,i], '--', color=[0.38,0.38,0.38,1], linewidth=1.5)
            for i in range(32,40):
                j = 4
                axs[j,i-8*j].set_title(MyUtils.plate[i])
                if isinstance(PLE_Tecan_fit.max_index[i], numpy.integer) == True:
                    if PLE_Tecan_fit.max_index[i] <= 245:
                        xPLE = PLE_Tecan_fit.PLE_data.iloc[int(PLE_Tecan_fit.max_index[i]+15):int(PLE_Tecan_fit.max_index[i]+45),49]
                        # j = 4
                        # axs[j,i-8*j].set_title(MyUtils.plate[i])
                        if MyUtils.plate[i] in MyUtils.chosen:
                            axs[j,i-8*j].plot(xPLE, PLE_Tecan_fit.LinearFits_Eg[i].best_fit, color=[red[i-8*j],green[j],blue[0],alpha[0]], linewidth=1.5)
                            axs[j,i-8*j].plot(xPLE, PLE_Tecan_fit.GaussCurvesT.iloc[PLE_Tecan_fit.max_index[i]+15:PLE_Tecan_fit.max_index[i]+45,i], '--', color=[0.38,0.38,0.38,1], linewidth=1.5)
            for i in range(40,48):
                j = 5
                axs[j,i-8*j].set_title(MyUtils.plate[i])
                if isinstance(PLE_Tecan_fit.max_index[i], numpy.integer) == True:
                    if PLE_Tecan_fit.max_index[i] <= 245:
                        xPLE = PLE_Tecan_fit.PLE_data.iloc[int(PLE_Tecan_fit.max_index[i]+15):int(PLE_Tecan_fit.max_index[i]+45),49]
                        # j = 5
                        # axs[j,i-8*j].set_title(MyUtils.plate[i])
                        if MyUtils.plate[i] in MyUtils.chosen:
                            axs[j,i-8*j].plot(xPLE, PLE_Tecan_fit.LinearFits_Eg[i].best_fit, color=[red[i-8*j],green[j],blue[0],alpha[0]], linewidth=1.5)
                            axs[j,i-8*j].plot(xPLE, PLE_Tecan_fit.GaussCurvesT.iloc[PLE_Tecan_fit.max_index[i]+15:PLE_Tecan_fit.max_index[i]+45,i], '--', color=[0.38,0.38,0.38,1], linewidth=1.5)
                
        for ax in axs.flat:
            ax.label_outer()


        fig.tight_layout()
        fig.patch.set_facecolor('white')
        plt.savefig(path.completeName9, transparent = False)
        plt.show()
