import tkinter as tk
import os
import threading

from tkinter import filedialog, Tk
from tkinter import Label, Button
from myutils import MyUtils
from theme import HIERNtheme
from joining import path
from output_txt import save_files
from PLE_fit import PLE_Tecan_fit
from progress import progress_bar_circular


class PLE_Tecan_filedialog(tk.Toplevel):
   
    def __init__(self, master: Tk): 
        tk.Toplevel.__init__(self)

        self.folder_selected = tk.StringVar()
        self.filename = tk.StringVar()
        
        self.withdraw()
        self.lift(master) 
        
        icon_path = MyUtils.get_absolute_path('resources\HIERN_icon.ico')
        self.iconbitmap(icon_path)
        
        
    def show(self, chosen):

        # self.MyUtils.chosen = MyUtils.chosen
        
        self.title("PLE Tecan filedialog")
        self.configure(background=HIERNtheme.mywhite)

        file_label = Label (self, text = '\nwhich PLE file would you like to fit?', bg = HIERNtheme.mywhite, fg = HIERNtheme.myblue, font = HIERNtheme.header_font)
        file_label.grid(row=1, column=0, sticky=tk.W)
            
        self.__file_select = Button (self, text = "browse", bg = HIERNtheme.mylime, fg = HIERNtheme.mywhite, font = HIERNtheme.standard_font, width = 6, command=self.__click_file)
        self.__file_select.grid(row=2, column=0, sticky=tk.W)

        save_label = Label (self, text = '\nwhere would you like to save the new files?', bg = HIERNtheme.mywhite, fg = HIERNtheme.myblue, font = HIERNtheme.header_font)
        save_label.grid(row=5, column=0, sticky=tk.W)

        folder_label = Label (self, text = 'folder for fit results', bg = HIERNtheme.mywhite, fg = HIERNtheme.myblue, font = HIERNtheme.standard_font)
        folder_label.grid(row=6, column=0, sticky=tk.W)

        self.__folder_select = Button (self, text = "browse", bg = HIERNtheme.mylime, fg = HIERNtheme.mywhite, font = HIERNtheme.standard_font, width = 6, command=self.__click_folder)
        self.__folder_select.grid(row=7, column=0, sticky=tk.W)

        self.__submit = Button (self, text = "submit and start process", bg = HIERNtheme.myorange, fg = HIERNtheme.mywhite, font = HIERNtheme.standard_font, width = 20, command=self.__close_self)
        self.__submit.grid(row=9, column=0, sticky=tk.W)

        self.Error2 = Label (self)
        self.Error_warning = Label (self)

        self.update_idletasks()
        self.deiconify()

   
    def __click(self):
        print('done')

    def __click_file(self):
        self.filename.set(str(filedialog.askopenfilename(parent = self, title='Chosse file')))
        if os.path.exists(self.filename.get()) == True:
            self.__file_select.config(bg = HIERNtheme.mygrey, text='done', command=self.__click)
            self.Error_warning.destroy()
        else:
            self.Error_warning.grid(row=3, columnspan=10, sticky=tk.W)
            self.Error_warning.config(fg=HIERNtheme.myorange, bg=HIERNtheme.mywhite, font=HIERNtheme.standard_font, text='the file you chose does not exist, please choose again')
            # Error_warning.grid(row=13, columnspan=10, sticky=tk.W)
            # label_selected_files.config(fg=HIERNtheme.myorange)
            self.filename.clear()

        
    def __click_folder(self):
        self.folder_selected.set(str(filedialog.askdirectory(parent = self, title='Choose folder')))
        if os.path.isdir(self.folder_selected.get()) == True:
            self.__folder_select.config(bg = HIERNtheme.mygrey, text='done', command=self.__click)
            self.Error2.destroy()
        else:
            self.Error2 = Label(self, fg=HIERNtheme.myorange, bg=HIERNtheme.mywhite, font=HIERNtheme.standard_font, text='the selected folder does not exist, please choose again')
            self.Error2.grid(row=8, columnspan=10, sticky=tk.W)


    def __close_self(self):

        # progress_bar_circular(self).progress_show()

        path.PLE_join_path(self.folder_selected.get())
        self.download_thread = threading.Thread(PLE_Tecan_fit.PLE_fitting(MyUtils.chosen, self.filename.get(), self.folder_selected.get()))
        
        self.download_thread.start()

        GaussFits_PLE = PLE_Tecan_fit.GaussFits_PLE
        GaussFits_PLE_norm = PLE_Tecan_fit.GaussFits_PLE_norm
        PLE_data_norm = PLE_Tecan_fit.PLE_data_norm
        PLE_data = PLE_Tecan_fit.PLE_data
        GaussCurvesT = PLE_Tecan_fit.GaussCurvesT
        LinearFits_Eg = PLE_Tecan_fit.LinearFits_Eg
        max_index = PLE_Tecan_fit.max_index
        Eg = PLE_Tecan_fit.Eg

        save_files.save_PLE(MyUtils.chosen, path.completeName3, path.completeName4, path.completeName6, path.completeName7, path.completeName8, path.completeName11, path.completeName20, path.completeName21, path.completeName22, path.completeName23, path.completeName24, path.completeName25, GaussFits_PLE, LinearFits_Eg, Eg, max_index)


    #     print('start monitor')
    #     self.monitor(self.download_thread)
    #     print('end monitor')
        self.destroy()

    # def monitor(self, download_thread):
    #     """ Monitor the download thread """
    #     if download_thread.is_alive():
    #         self.after(1, lambda: self.monitor(download_thread))
    #         print('läuft')
    #     else:
    #         progress_bar_circular(self).progress_stop()
    #         print('stop')