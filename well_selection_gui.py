import tkinter as tk
from tkinter import Label, Button, Tk
from PLE_filedialog import PLE_Tecan_filedialog
from PL_Tecan_filedialog import PL_Tecan_Filedialog
from Raman_filedialog import Raman_dialog
from myutils import MyUtils
from theme import HIERNtheme
from PL_Stellar_filedialog import PL_SN_filedialog
from reflectance_filedialog import reflectance_gui
from trPL_filedialog import tr_PL_GUI
import threading

class well_gui(tk.Toplevel):
    
    def __init__(self, master: Tk):
        tk.Toplevel.__init__(self)
    
        # self.MyUtils.chosen = []
        self.__buttons = [[None]*8 for _ in range(6)]
        self.__sample = [[None]*8 for _ in range(6)]
        #self.methode = StringVar()

        self.withdraw()
        self.lift(master)
        
        icon_path = MyUtils.get_absolute_path('resources\HIERN_icon.ico')
        self.iconbitmap(icon_path)
        
    def show(self, methode):
        
        self.title('choose wells')
        
        MyUtils.chosen.clear()
        MyUtils.amplitude_list.clear()
        MyUtils.height_list.clear()
        MyUtils.center_list.clear()
        MyUtils.fwhm_list.clear()
        MyUtils.chosenA = ['__'] * 8
        MyUtils.chosenB = ['__'] * 8
        MyUtils.chosenC = ['__'] * 8
        MyUtils.chosenD = ['__'] * 8
        MyUtils.chosenE = ['__'] * 8
        MyUtils.chosenF = ['__'] * 8

        label_title = Label(self, bg = HIERNtheme.mywhite, fg = HIERNtheme.myblue, font = HIERNtheme.standard_font, text = '\n' + 'Which well positions should be evaluated?' + '\n')
        label_title.grid(row=0, column = 0, columnspan = 8, sticky=tk.W)

        for i in range (6):
            for col in range (8):
                self.__sample[i][col] = tk.StringVar()
                self.__sample[i][col].set(str(MyUtils.plate[col+i*8]))
                self.__buttons[i][col] = Button (self, bg = HIERNtheme.mygrey, fg = HIERNtheme.mywhite, font = HIERNtheme.standard_font, command = lambda i=i, j=col : self.__choose(i, j))
                self.__buttons[i][col].config(textvariable = self.__sample[i][col], width = 6, height = 3)
                self.__buttons[i][col].grid(row = i+2, column = col)

        button_select_all = Button (self, bg = HIERNtheme.myblue, fg = HIERNtheme.mywhite, font = HIERNtheme.standard_font, text = 'Select all', command = self.__choose_all)
        button_select_all.grid(row=50, column=0, columnspan=2, sticky=tk.W)

        button_undo = Button (self, bg = HIERNtheme.myblue, fg = HIERNtheme.mywhite, font = HIERNtheme.standard_font, text = 'Undo selection', command = self.__undo_all)
        button_undo.grid(row=50, column=2, columnspan=2, sticky=tk.W)

        button_submit = Button (self, bg = HIERNtheme.myorange, fg = HIERNtheme.mywhite, font = HIERNtheme.standard_font, text = 'submit and close', command = lambda: self.__close_root(methode))
        button_submit.grid(row=50, column=5, columnspan=3, sticky=tk.E)

        self.configure(background=HIERNtheme.mywhite)
        
        self.update_idletasks()
        self.deiconify()
        

    def __choose(self, i, j):
        self.__buttons[i][j].config(bg = HIERNtheme.mylime, command = lambda i=i, j=j : self.__undo(i,j))
        MyUtils.chosen.append(str(self.__sample[i][j].get()))


    def __choose_all(self):
        MyUtils.chosen.clear()
        for i in range(6):
            for col in range (8):
                self.__buttons[i][col].config(bg = HIERNtheme.mylime, command = lambda i=i, j=col : self.__undo(i,j))
                MyUtils.chosen.append(str(MyUtils.plate[col+i*8]))

    def __undo_all(self):
        MyUtils.chosen.clear()
        for i in range(6):
            for col in range (8):
                self.__buttons[i][col].config(bg = HIERNtheme.mygrey, command = lambda i=i, j=col : self.__choose(i,j))

    def __undo(self, i,j):
        MyUtils.chosen.remove(str(self.__sample[i][j].get()))
        self.__buttons[i][j].config(bg = HIERNtheme.mygrey, command = lambda i=i, j=j : self.__choose(i,j))

    def __close_root(self, methode):

        #self.methode.set(methode.get())
        print('blub')
        print(methode)
        # print(MyUtils.chosenA)

        for i in range(0,8):
            j = 0
            if MyUtils.plate[i] in MyUtils.chosen:
                MyUtils.chosenA[i-j*8] = MyUtils.plate[i]
        
        for i in range(8,16):
            j = 1
            if MyUtils.plate[i] in MyUtils.chosen:
                MyUtils.chosenB[i-j*8] = MyUtils.plate[i]

        for i in range(16,24):
            j = 2
            if MyUtils.plate[i] in MyUtils.chosen:
                MyUtils.chosenC[i-j*8] = MyUtils.plate[i]

        for i in range(24,32):
            j = 3
            if MyUtils.plate[i] in MyUtils.chosen:
                MyUtils.chosenD[i-j*8] = MyUtils.plate[i]

        for i in range(32,40):
            j = 4
            if MyUtils.plate[i] in MyUtils.chosen:
                MyUtils.chosenE[i-j*8] = MyUtils.plate[i]

        for i in range(40,48):
            j = 5
            if MyUtils.plate[i] in MyUtils.chosen:
                MyUtils.chosenF[i-j*8] = MyUtils.plate[i]

        # print(MyUtils.chosenA)

        if methode == 'one':
        
            PLS = PL_SN_filedialog(self)
            #PLS = self.methode.get()
            target=PLS.show(MyUtils.chosen)

        if methode == 'two':

            PLET = PLE_Tecan_filedialog(self)
            PLET.show(MyUtils.chosen)
        
        if methode == 'three':

            refGUI = reflectance_gui(self)
            refGUI.show(MyUtils.chosen)


        if methode == 'four':

            RamanGUI = Raman_dialog(self)
            RamanGUI.show(MyUtils.chosen)


        if methode == 'five':

            trPLGUI = tr_PL_GUI(self)
            trPLGUI.show(MyUtils.chosen)

        if methode == 'six':

            PLT = PL_Tecan_Filedialog(self)
            PLT.show(MyUtils.chosen)


        self.destroy()

    