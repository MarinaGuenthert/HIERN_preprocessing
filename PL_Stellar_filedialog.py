import tkinter as tk
import os
from tkinter import ttk

from tkinter import filedialog
from tkinter import Label, Button, Tk
import threading
from threading import Thread, Event
import time

from myutils import MyUtils
from theme import HIERNtheme
from joining import path
from PL_Stellar_fit import PLS_fit
from output_txt import save_files

from progress import progress_bar_circular



class PL_SN_filedialog(tk.Toplevel):
   
    def __init__(self, master: Tk):
        tk.Toplevel.__init__(self)

        self.BaSO4 = tk.StringVar()
        self.folder_selected = tk.StringVar()
        self.all_filenames = []
        # self.download_thread = None
        
        self.withdraw()
        self.lift(master) 
        
        icon_path = MyUtils.get_absolute_path('resources\HIERN_icon.ico')
        self.iconbitmap(icon_path)
        
        
    def show(self, chosen):
        
        self.__well_number = len(MyUtils.chosen)
        # self.MyUtils.chosen = MyUtils.chosen
        # create user interface with logo

        self.title("PL StellarNet filedialog")
        self.configure(background=HIERNtheme.mywhite)


        #text and buttons for user interface

        label_reference = Label (self, text = '\nwhich is the reference file?', bg = HIERNtheme.mywhite, fg = HIERNtheme.myblue, font = HIERNtheme.header_font)
        label_reference.grid(row=1, columnspan = 3, sticky=tk.W)

        self.__button_reference =  Button (self, text = "browse", bg = HIERNtheme.mylime, fg = HIERNtheme.mywhite, font = HIERNtheme.standard_font, width = 6, command=self.__click_ref)
        self.__button_reference.grid(row=2, column=0, sticky=tk.W)

        label_files = Label (self, text = '\nwhich PL files would you like to evaluate?', bg = HIERNtheme.mywhite, fg = HIERNtheme.myblue, font = HIERNtheme.header_font)
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
        self.Error = Label(self)
        self.Error2 = Label(self)
        
        #return self.BaSO4, self.all_filenames, self.folder_selected
        self.update_idletasks()
        self.deiconify()

        # click functions for user interface

    def __click(self):
        print('done')

    def __click_ref(self):
        #global BaSO4
        self.BaSO4.set(str(filedialog.askopenfilename(parent=self, title='Choose reference')))
        if os.path.exists(self.BaSO4.get()) == True:
            self.__button_reference.config(text = "done", bg = HIERNtheme.mygrey, fg = HIERNtheme.mywhite, font = HIERNtheme.standard_font, width = 6, command=self.__click)
            self.Error.destroy()
        else:
            self.Error = Label(self, fg=HIERNtheme.myorange, bg=HIERNtheme.mywhite, font=HIERNtheme.standard_font, text='the selected reference file does not exist, please choose again')
            self.Error.grid(row=3, columnspan=10, sticky=tk.W)

    def __click_file(self):
        #global all_filenames
        self.all_filenames.extend(filedialog.askopenfilenames(parent=self, title='Choose files'))
        label_selected_files = Label(self, text = 'number of files: ' + str(len(self.all_filenames)), bg = HIERNtheme.mywhite, fg = HIERNtheme.mygrey, font = HIERNtheme.standard_font)
        label_selected_files.grid(row=12, column=1)
        #self.Error_warning = Label (self)
        # Error_warning.grid(row=13, columnspan=10, sticky=tk.W)
        if len(self.all_filenames) == self.__well_number:
            #self.Error_warning.config(fg=HIERNtheme.mylime)
            self.__button_files.config(text = "done", bg = HIERNtheme.mygrey, fg = HIERNtheme.mywhite, font = HIERNtheme.standard_font, width = 6, command=self.__click)
            self.Error_warning.destroy()

        else:
            self.Error_warning.grid(row=13, columnspan=10, sticky=tk.W)
            self.Error_warning.config(fg=HIERNtheme.myorange, bg=HIERNtheme.mywhite, font=HIERNtheme.standard_font, text='the number of chosen files does not match the number of chosen wells, please choose again')
            # Error_warning.grid(row=13, columnspan=10, sticky=tk.W)
            label_selected_files.config(fg=HIERNtheme.myorange)
            self.all_filenames.clear()



    def __click_folder(self):
        #global folder_selected
        self.folder_selected.set(str(filedialog.askdirectory(parent=self, title='Choose folder')))
        if os.path.isdir(self.folder_selected.get()) == True:
            self.__button_folder.config(text = "done", bg = HIERNtheme.mygrey, fg = HIERNtheme.mywhite, font = HIERNtheme.standard_font, width = 6, command=self.__click)
            self.Error2.destroy()
        else:
            self.Error2 = Label(self, fg=HIERNtheme.myorange, bg=HIERNtheme.mywhite, font=HIERNtheme.standard_font, text='the selected folder does not exist, please choose again')
            self.Error2.grid(row=17, columnspan=10, sticky=tk.W)


    def __close_self(self):
        
        # PLS = PL_SN_filedialog(root)

        # threading.Thread(target=progress_bar_circular(self).progress_start()).start()

        # self.bar = threading.Thread(progress_bar_circular(self).progress_show())
        # self.bar.start()

        # progress_bar_circular(self).progress_show()

        path.PL_join_path(self.folder_selected.get())
        self.download_thread = threading.Thread(PLS_fit.PLS_fitting(self.BaSO4.get(), MyUtils.chosen, self.all_filenames, self.folder_selected.get()))#.start()

        # print(type(self.download_thread))
        self.download_thread.start()

        # self.bar.join()
        # self.download_thread.join()

        GaussFits_PL = PLS_fit.GaussFits_PL
        PL_corrected = PLS_fit.PL_corrected
        GaussFits_PL_norm = PLS_fit.GaussFits_PL_norm
        PL_data_norm = PLS_fit.PL_data_norm

        save_files.save_Gauss_PL(path.completeName3, path.completeName4, path.completeName11, path.completeName21, path.completeName22, path.completeName23, path.completeName24, path.completeName25, GaussFits_PL, MyUtils.chosen, path.completeName10)
        
    
    #     print('start monitor')
    #     self.monitor(self.download_thread)
    #     print('end monitor')
        self.destroy()

        

    # def monitor(self, download_thread):
    #     """ Monitor the download thread """
    #     if download_thread.is_alive():
    #         self.after(100, lambda: self.monitor(download_thread))
    #         print('läuft')
    #     else:
    #         progress_bar_circular(self).progress_stop()
    #         # self.bar.join()
    #         # self.pb.stop()
    #         print('stop')


        
    


    #define output filenames

    #self.__folderPath = self.__folder_selected
    #self.__fitted_Graphs = "PL_overview_fit.png"
    #self.__norm_fitted_Graphs = "PL_overview_fit_norm.png"
    #self.__all_parameters = "PL_all_fit_results.txt"
    #self.__fitted_parameters = "PL_overview_fit_parameters.txt"
    #self.__threeD_print = "PL_extracted_fit_parameters"

    #self.completeName1 = os.path.join(self.folderPath, self.__fitted_Graphs)
    #self.completeName2 = os.path.join(self.folderPath, self.__norm_fitted_Graphs)
    #self.completeName3 = os.path.join(self.folderPath, self.__all_parameters)
    #self.completeName4 = os.path.join(self.folderPath, self.__fitted_parameters)
    #self.completeName5 = os.path.join(self.folderPath, self.__threeD_print)
