import tkinter as tk
import os
import threading

from tkinter import Entry, filedialog
from tkinter import Label, Button, Tk
from output_txt import save_files

from theme import HIERNtheme
from myutils import MyUtils
from joining import path
from Raman_fit import Raman_data_evaluation
from output_txt import save_files
from progress import progress_bar_circular



class Raman_dialog(tk.Toplevel):

    def __init__(self, master: Tk):
        tk.Toplevel.__init__(self)

        self.SiO2 = tk.StringVar()
        self.folder_selected = tk.StringVar()
        self.all_filenames = []

        self.baseline = tk.StringVar()
        self.minimum = tk.StringVar()
        self.maximum = tk.StringVar()
        
        self.withdraw()
        self.lift(master) 
        
        icon_path = MyUtils.get_absolute_path('resources\HIERN_icon.ico')
        self.iconbitmap(icon_path)
        
        
    def show(self, chosen):

        self.configure(background=HIERNtheme.mywhite)

        # self.MyUtils.chosen = MyUtils.chosen

        reference_label = Label (self, text = '\nwhich is the Si reference file?', bg = HIERNtheme.mywhite, fg = HIERNtheme.myblue, font = HIERNtheme.header_font)
        reference_label.grid(row=1, columnspan = 3, sticky=tk.W)

        self.__SiO2_button =  Button (self, text = "browse", bg = HIERNtheme.mylime, fg = HIERNtheme.mywhite, font = HIERNtheme.standard_font, width = 6, command=self.__click_ref)
        self.__SiO2_button.grid(row=2, column=0, sticky=tk.W)

        label_files = Label (self, text = '\nwhich Raman files would you like to fit?', bg = HIERNtheme.mywhite, fg = HIERNtheme.myblue, font = HIERNtheme.header_font)
        label_files.grid(row=4, columnspan = 3, sticky=tk.W)

        label_chosen1 = Label (self, text = 'chosen: ', bg = HIERNtheme.mywhite, fg = HIERNtheme.myblue, font = HIERNtheme.standard_font)
        label_chosen1.grid(row=5, column=0, sticky=tk.W)

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
            
        self.__files_button = Button (self, text = "browse", bg = HIERNtheme.mylime, fg = HIERNtheme.mywhite, font = HIERNtheme.standard_font, width = 6, command=self.__click_file)
        self.__files_button.grid(row=12, column=0, sticky=tk.W)

        label_folder = Label (self, text = '\nwhere would you like to save the new files?', bg = HIERNtheme.mywhite, fg = HIERNtheme.myblue, font = HIERNtheme.header_font)
        label_folder.grid(row=14, columnspan = 3, sticky=tk.W)

        label_folder2 = Label (self, text = 'folder for fit results', bg = HIERNtheme.mywhite, fg = HIERNtheme.myblue, font = HIERNtheme.standard_font)
        label_folder2.grid(row=15, columnspan = 2, sticky=tk.W)

        self.__folder_button = Button (self, text = "browse", bg = HIERNtheme.mylime, fg = HIERNtheme.mywhite, font = HIERNtheme.standard_font, width = 6, command=self.__click_folder)
        self.__folder_button.grid(row=16, column=0, sticky=tk.W)

        label_distance = Label(self, width=1, height=1, bg=HIERNtheme.mywhite).grid(row=17, column=0)

        label_baseline = Label(self, text = 'use quadratic baseline correction?', bg = HIERNtheme.mywhite, fg = HIERNtheme.myblue, font=HIERNtheme.header_font)
        label_baseline.grid(row=19, columnspan=3, sticky=tk.W)

        self.__baseline_button = Button (self, text = "off", bg = HIERNtheme.mygrey, fg = HIERNtheme.mywhite, width = 6, font = HIERNtheme.standard_font, command=self.__on)
        self.__baseline_button.grid(row=20, column=0, sticky=tk.W)

        peaks_label = Label(self, bg = HIERNtheme.mywhite, fg = HIERNtheme.myblue, font=HIERNtheme.header_font, text='What is the minimum and maximum prominence for the peaks?')
        peaks_label.grid(row=22, columnspan=3, sticky=tk.W)

        minimum_label = Label(self, text = 'Minimum', bg = HIERNtheme.mywhite, fg = HIERNtheme.myblue, font=HIERNtheme.standard_font)
        minimum_label.grid(row=23, column=0,  sticky=tk.W)

        maximum_label = Label(self, text = 'Maximum', bg = HIERNtheme.mywhite, fg = HIERNtheme.myblue, font=HIERNtheme.standard_font)
        maximum_label.grid(row=23, column=1,  sticky=tk.W)

        minimum_entry = Entry(self, textvariable=self.minimum, width=10)
        minimum_entry.grid(row=24, column=0, sticky=tk.W)

        maximum_entry = Entry(self, textvariable=self.maximum, width=10)
        maximum_entry.grid(row=24, column=1, sticky=tk.W)

        # Label(self, width=1, height=1, bg=HIERNtheme.mywhite).grid(row=24, column=0)

        Label(self, width=1, height=1, bg=HIERNtheme.mywhite).grid(row=25, column=0)
        Label(self, width=1, height=1, bg=HIERNtheme.mywhite).grid(row=21, column=0)

        submit_button = Button (self, text = "submit and start process", bg = HIERNtheme.myorange, fg = HIERNtheme.mywhite, font = HIERNtheme.standard_font, width = 20, command=self.__close_self)
        submit_button.grid(row=26, columnspan = 2, sticky=tk.W)

        self.Error_warning = Label (self)
        self.Error = Label(self)
        self.Error2 = Label(self)

        self.update_idletasks()
        self.deiconify()

    
    def __on(self):
        self.baseline.set('on')
        self.__baseline_button.config(text = 'on', bg = HIERNtheme.mylime, fg = HIERNtheme.mywhite, command=self.__off)

    def __off(self):
        self.baseline.set('off')
        self.__baseline_button.config(text = 'off', bg = HIERNtheme.mygrey, fg = HIERNtheme.mywhite, command=self.__on)


    def __click(self):
        print('done')
    
    def __click_ref(self):
        
        #global SiO2
        self.SiO2.set(filedialog.askopenfilename(parent=self, title='Choose reference'))
        if os.path.exists(self.SiO2.get()) == True:
            self.__SiO2_button.config(text = "done", bg = HIERNtheme.mygrey, fg = HIERNtheme.mywhite, font = HIERNtheme.standard_font, width = 6, command=self.__click)
            self.Error.destroy()
        else:
            self.Error = Label(self, fg=HIERNtheme.myorange, bg=HIERNtheme.mywhite, font=HIERNtheme.standard_font, text='the selected reference file does not exist, please choose again')
            self.Error.grid(row=3, columnspan=10, sticky=tk.W)


    def __click_file(self):
        #global all_filenames
        self.all_filenames.extend(filedialog.askopenfilenames(parent=self, title='Choose a File'))
        if len(self.all_filenames) == len(MyUtils.chosen):
            self.__files_button.config(text = "done", bg = HIERNtheme.mygrey, fg = HIERNtheme.mywhite, font = HIERNtheme.standard_font, width = 6, command=self.__click)
            self.Error_warning.destroy()
            #print(filename)
            #Button['text'] = 'done'
        else:
            self.Error_warning.grid(row=13, columnspan=10, sticky=tk.W)
            self.Error_warning.config(fg=HIERNtheme.myorange, bg=HIERNtheme.mywhite, font=HIERNtheme.standard_font, text='the number of chosen files does not match the number of chosen wells, please choose again')
            # Error_warning.grid(row=13, columnspan=10, sticky=tk.W)
            # label_selected_files.config(fg=HIERNtheme.myorange)
            self.all_filenames.clear()

        
    def __click_folder(self):
        #global folder_selected
        self.folder_selected.set(filedialog.askdirectory(parent=self, title = 'Choose folder'))
        if os.path.isdir(self.folder_selected.get()) == True:
            self.__folder_button.config(text = "done", bg = HIERNtheme.mygrey, fg = HIERNtheme.mywhite, font = HIERNtheme.standard_font, width = 6, command=self.__click)
            self.Error2.destroy()
        else:
            self.Error2 = Label(self, fg=HIERNtheme.myorange, bg=HIERNtheme.mywhite, font=HIERNtheme.standard_font, text='the selected folder does not exist, please choose again')
            self.Error2.grid(row=17, columnspan=10, sticky=tk.W)


    def __close_self(self):

        # self.bar = threading.Thread(progress_bar_circular(self).progress_show())
        # self.bar.start()
        
        path.Raman_join_path(self.folder_selected.get())
        Raman_data_evaluation.Raman_findpeaks(MyUtils.chosen, self.SiO2.get(), self.all_filenames, self.folder_selected.get(), self.baseline.get(), self.minimum.get(), self.maximum.get())

        # self.download_thread1.start()

        LorentzFits_Raman = Raman_data_evaluation.LorentzFits_Raman  
        Reports_Raman = Raman_data_evaluation.Reports_Raman
        x_Raman = Raman_data_evaluation.x_Raman
        Raman_data = Raman_data_evaluation.Raman_data
        local_max = Raman_data_evaluation.local_max
        maxima_list = Raman_data_evaluation.maxima_list

        self.download_thread = threading.Thread(Raman_data_evaluation.Raman_fitting(MyUtils.chosen, self.SiO2.get(), self.all_filenames, self.folder_selected.get(), self.baseline.get(), self.minimum.get(), self.maximum.get()))

        self.download_thread.start()

        # print('start monitor')
        # # self.monitor(self.download_thread1)
        # self.monitor(self.download_thread)
        # print('end monitor')

        maxima_list = Raman_data_evaluation.maxima_list
        problem = Raman_data_evaluation.problem
        # LorentzFits_Raman = Raman_data_evaluation.LorentzFits_Raman
        # Reports_Raman = Raman_data_evaluation.Reports_Raman

        save_files.save_Raman1(MyUtils.chosen, maxima_list, Reports_Raman, LorentzFits_Raman, problem, path.completeName5, path.completeName3, path.completeName6)
        


        self.destroy()

    # def monitor(self, download_thread):
    #     """ Monitor the download thread """
    #     if download_thread.is_alive():
    #         self.after(1, lambda: self.monitor(download_thread))
    #         print('läuft')
    #     else:
    #         progress_bar_circular(self).progress_stop()
    #         self.bar.join()
    #         print('stop')