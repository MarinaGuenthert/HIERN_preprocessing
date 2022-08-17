import tkinter as tk
import os
import threading


from tkinter import filedialog
from tkinter import Label, Button, Tk

from myutils import MyUtils
from theme import HIERNtheme
from joining import path
from trPL_fit import trPL_evaluation
from output_txt import save_files
from progress import progress_bar_circular



class tr_PL_GUI(tk.Toplevel):
    
    def __init__(self, master: Tk):
        tk.Toplevel.__init__(self)

        self.folder_selected = tk.StringVar()
        self.all_filenames = []
        self.variable = tk.StringVar()
        
        self.withdraw()
        self.lift(master)
        
        icon_path = MyUtils.get_absolute_path('resources\HIERN_icon.ico')
        self.iconbitmap(icon_path)

    def show(self, chosen):

        self.__well_number = len(MyUtils.chosen)
        # self.MyUtils.chosen = MyUtils.chosen

        self.title("tr PL filedialog")
        self.configure(background=HIERNtheme.mywhite)

        #text and buttons for user interface

        label_methode = Label (self, text = 'which fit methode should be used?', bg= HIERNtheme.mywhite, fg=HIERNtheme.myblue, font = HIERNtheme.header_font)
        label_methode.grid(row=0, column=0, sticky=tk.W)

        self.variable.set('Select methode')

        methodes = ['averaged three exponential', 'stretched exponential']

        opt = tk.OptionMenu(self, self.variable, *methodes)
        opt.grid(row = 1, column = 0, sticky=tk.W)
        opt.config(bg=HIERNtheme.mylime)



        label_files = Label (self, text = '\nwhich tr PL files would you like to evaluate?', bg = HIERNtheme.mywhite, fg = HIERNtheme.myblue, font = HIERNtheme.header_font)
        label_files.grid(row=4, columnspan = 3, sticky=tk.W)

        label_wells = Label (self, text = 'number of chosen wells: ' + str(self.__well_number), bg = HIERNtheme.mywhite, fg = HIERNtheme.myblue, font = HIERNtheme.standard_font)
        label_wells.grid(row=5, columnspan = 2, sticky=tk.W)

        label_chosen1 = Label (self, text = 'chosen: ', bg = HIERNtheme.mywhite, fg = HIERNtheme.myblue, font = HIERNtheme.standard_font)
        label_chosen1.grid(row=6, column=0, sticky=tk.W)

        label_chosenA = Label (self, text = MyUtils.chosenA, bg = HIERNtheme.mywhite, fg = HIERNtheme.mygrey, font = HIERNtheme.standard_font)
        label_chosenA.grid(row=6, column=1, sticky=tk.W)

        label_chosenB = Label (self, text = MyUtils.chosenB, bg = HIERNtheme.mywhite, fg = HIERNtheme.mygrey, font = HIERNtheme.standard_font)
        label_chosenB.grid(row=7, column=1, sticky=tk.W)

        label_chosenC = Label (self, text = MyUtils.chosenC, bg = HIERNtheme.mywhite, fg = HIERNtheme.mygrey, font = HIERNtheme.standard_font)
        label_chosenC.grid(row=8, column=1, sticky=tk.W)

        label_chosenD = Label (self, text = MyUtils.chosenD, bg = HIERNtheme.mywhite, fg = HIERNtheme.mygrey, font = HIERNtheme.standard_font)
        label_chosenD.grid(row=9, column=1, sticky=tk.W)

        label_chosenE = Label (self, text = MyUtils.chosenE, bg = HIERNtheme.mywhite, fg = HIERNtheme.mygrey, font = HIERNtheme.standard_font)
        label_chosenE.grid(row=10, column=1, sticky=tk.W)

        label_chosenF = Label (self, text = MyUtils.chosenF, bg = HIERNtheme.mywhite, fg = HIERNtheme.mygrey, font = HIERNtheme.standard_font)
        label_chosenF.grid(row=11, column=1, sticky=tk.W)

        self.__button_files = Button (self, text = "browse", bg = HIERNtheme.mylime, fg = HIERNtheme.mywhite, font = HIERNtheme.standard_font, width = 6, command=self.__click_file)
        self.__button_files.grid(row=12, column=0, sticky=tk.W)

        label_folder = Label (self, text = '\nwhere would you like to save the new files?', bg = HIERNtheme.mywhite, fg = HIERNtheme.myblue, font = HIERNtheme.header_font)
        label_folder.grid(row=14, columnspan = 3, sticky=tk.W)

        label_resultfolder = Label (self, text = 'folder for fit results', bg = HIERNtheme.mywhite, fg = HIERNtheme.myblue, font = HIERNtheme.standard_font)
        label_resultfolder.grid(row=15, columnspan = 2, sticky=tk.W)

        self.__button_folder = Button (self, text = "browse", bg = HIERNtheme.mylime, fg = HIERNtheme.mywhite, font = HIERNtheme.standard_font, width = 6, command=self.__click_folder)
        self.__button_folder.grid(row=16, column=0, sticky=tk.W)

        label_distance = Label(self, width=1, height=1, bg=HIERNtheme.mywhite).grid(row=17, column=0)

        button_start = Button (self, text = "submit and start process", bg = HIERNtheme.myorange, fg = HIERNtheme.mywhite, font = HIERNtheme.standard_font, width = 20, command=self.__close_self)
        button_start.grid(row=18, columnspan = 2, sticky=tk.W)

        self.Error_warning = Label (self)
        self.Error2 = Label (self)

        self.update_idletasks()
        self.deiconify()

    def __click(self):
        print('done')


    def __click_file(self):

        self.all_filenames.extend(filedialog.askopenfilenames(parent=self, title='Choose files'))
        label_selected_files = Label(self, text = 'number of files: ' + str(len(self.all_filenames)), bg = HIERNtheme.mywhite, fg = HIERNtheme.mygrey, font = HIERNtheme.standard_font)
        label_selected_files.grid(row=12, column=1)
        if len(self.all_filenames) == self.__well_number:
            self.__button_files.config(text = "done", bg = HIERNtheme.mygrey, fg = HIERNtheme.mywhite, font = HIERNtheme.standard_font, width = 6, command=self.__click)
            self.Error_warning.destroy()

        else:
            self.Error_warning.grid(row=13, columnspan=10, sticky=tk.W)
            self.Error_warning.config(fg=HIERNtheme.myorange, bg=HIERNtheme.mywhite, font=HIERNtheme.standard_font, text='the number of chosen files does not match the number of chosen wells, please choose again')
            # Error_warning.grid(row=13, columnspan=10, sticky=tk.W)
            label_selected_files.config(fg=HIERNtheme.myorange)
            self.all_filenames.clear()



    def __click_folder(self):

        self.folder_selected.set(str(filedialog.askdirectory(parent=self, title='Choose folder')))
        if os.path.isdir(self.folder_selected.get()) == True:
            self.__button_folder.config(text = "done", bg = HIERNtheme.mygrey, fg = HIERNtheme.mywhite, font = HIERNtheme.standard_font, width = 6, command=self.__click)
            self.Error2.destroy()
        else:
            self.Error2 = Label(self, fg=HIERNtheme.myorange, bg=HIERNtheme.mywhite, font=HIERNtheme.standard_font, text='the selected folder does not exist, please choose again')
            self.Error2.grid(row=17, columnspan=10, sticky=tk.W)


    def __close_self(self):
        
        # progress_bar_circular(self).progress_show()

        path.trPL_join_path(self.folder_selected.get())

        if self.variable.get() == 'averaged three exponential':
            # progress_bar_circular(self).progress_show()
            self.download_thread = threading.Thread(trPL_evaluation.averaged_exponential(MyUtils.chosen, self.all_filenames, self.folder_selected.get()))

            self.download_thread.start()

            x_trPL = trPL_evaluation.x_trPL
            curves = trPL_evaluation.curves
            Fits = trPL_evaluation.Fits1    
            Reports = trPL_evaluation.Reports1
            methode = 1

            save_files.save_trPL(path.completeName12, path.completeName13, path.completeName15, path.completeName17, path.completeName27, path.completeName28, Fits, MyUtils.chosen, methode)
            # self.monitor(self.download_thread)


        if self.variable.get() == 'stretched exponential':
            
            # progress_bar_circular(self).progress_show()
            self.download_thread = threading.Thread(trPL_evaluation.stretched_exponential(MyUtils.chosen, self.all_filenames, self.folder_selected.get()))
            # trPL_evaluation.stretched_exponential(MyUtils.chosen, self.all_filenames, self.folder_selected.get())

            self.download_thread.start()

            x_trPL = trPL_evaluation.x_trPL
            curves = trPL_evaluation.curves
            Fits = trPL_evaluation.Fits2    
            Reports = trPL_evaluation.Reports2
            methode = 2

            save_files.save_trPL(path.completeName22, path.completeName23, path.completeName25, path.completeName17, path.completeName27, path.completeName28, Fits, MyUtils.chosen, methode)
            # self.monitor(self.download_thread)


        self.destroy()

    # def monitor(self, download_thread):
    #     """ Monitor the download thread """
    #     if download_thread.is_alive():
    #         self.after(1, lambda: self.monitor(download_thread))
    #         print('läuft')
    #     else:
    #         progress_bar_circular(self).progress_stop()
    #         print('stop')