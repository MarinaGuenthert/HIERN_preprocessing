import tkinter as tk
from tkinter import Tk, PhotoImage, Label, Button
import tkpdf
# import awesometkinter as atk
import threading

from PLE_fit import PLE_Tecan_fit

from Raman_fit import Raman_data_evaluation
from Raman_plot import Raman_plotting
from Tauc_3D import Tauc_plot_Eg

from myutils import MyUtils
from theme import HIERNtheme
from threeD_lifetime import threeD_plot_lifetime
from well_selection_gui import well_gui
from PL_Stellar_filedialog import PL_SN_filedialog
from joining import path
from PL_Stellar_fit import PLS_fit
from PL_Stellar_plot import PLS_plot
from threeD_gui import threeD_plot

from PL_Tecan_fit import PL_Tecan_Fit
from PL_Tecan_plot import PL_Tecan_Plot

from PLE_plot import PLE_Tecan_plot
from threeD_Eg import threeD_plot_Eg

from reflectance_plot import ref_plot
from reflectance_correction import ref_correction
from Tauc_3D import Tauc_plot_Eg

from Raman_plot import Raman_plotting
from Raman_single_plot import plot_selection
from Raman_threeD import plot_Raman_D

from trPL_plot import trPL_plotting
from threeD_lifetime import threeD_plot_lifetime

from progress import progress_bar_circular




def click():
    Label(root, text='not yet implemented', bg=HIERNtheme.mywhite, fg= HIERNtheme.myred, font=HIERNtheme.standard_font). grid(row=20, column=1, columnspan=3)

def help():

    newWindow = tk.Toplevel(root)
 
    # sets the title of the
    # Toplevel widget
    newWindow.title("Manual")

    icon_path = MyUtils.get_absolute_path('resources\HIERN_icon.ico')
    newWindow.iconbitmap(icon_path)

    newWindow.configure(background=HIERNtheme.mywhite)

    screen_width = newWindow.winfo_screenwidth()
    screen_height = newWindow.winfo_screenheight()

    newWindow.geometry("%dx%d" % (screen_width/2, screen_height/2))


    pdf_path = MyUtils.get_absolute_path('resources\Manual_final_version.pdf')


    pdf_view = tkpdf.PdfView(newWindow, file=pdf_path)
    pdf_view.grid(row=0, column=0)




root = Tk()

# Button(root, text='progress', bg=HIERNtheme.myorange, fg=HIERNtheme.mywhite, command=progress_bar_circular(root).progress_start).grid(row=10, column=20)

root.configure(background=HIERNtheme.mywhite)

icon_path = MyUtils.get_absolute_path('resources\HIERN_icon.ico')
root.iconbitmap(icon_path)

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

root.title('HIERN 48 wellplate fitting')
# root.geometry("%dx%d" % (screen_width/2, screen_height/2))

photo_path = MyUtils.get_absolute_path('resources\logo.gif')
photo1 = PhotoImage(file = photo_path)
Label (root, image = photo1, bg = "white")  .grid(row=0, column=0, columnspan=5)

welcome_Label = Label(root, bg = HIERNtheme.mywhite, fg = HIERNtheme.myblue, font = HIERNtheme.header_font, text = 'Welcome to my 48 wellplate spectral fitting program', width=60, pady=20)
welcome_Label.grid(row = 3, column = 0, columnspan=5)

# methods

PL_Label = Label(root, bg = HIERNtheme.mywhite, fg = HIERNtheme.myblue, font = HIERNtheme.header_font, text = 'PL', width=15, relief='ridge', pady=10)
PL_Label.grid(row = 5, column = 0)

PLE_Label = Label(root, bg = HIERNtheme.mywhite, fg = HIERNtheme.myblue, font = HIERNtheme.header_font, text = 'PLE', width=15, relief='ridge', pady = 10)
PLE_Label.grid(row = 5, column = 1)

reflectance_Label = Label(root, bg = HIERNtheme.mywhite, fg = HIERNtheme.myblue, font = HIERNtheme.header_font, text = 'reflectance', width=15, relief='ridge', pady = 10)
reflectance_Label.grid(row = 5, column = 2)

Raman_Label = Label(root, bg = HIERNtheme.mywhite, fg = HIERNtheme.myblue, font = HIERNtheme.header_font, text = 'Raman', width=15, relief='ridge', pady = 10)
Raman_Label.grid(row = 5, column = 3)

trPL_Label = Label(root, bg = HIERNtheme.mywhite, fg = HIERNtheme.myblue, font = HIERNtheme.header_font, text = 'tr PL', width=15, relief='ridge', pady = 10)
trPL_Label.grid(row = 5, column = 4)

help_button = Button(root, bg = HIERNtheme.myorange, fg = HIERNtheme.mywhite, font = HIERNtheme.standard_font, width = 15, text = 'help', command = lambda: help() )
help_button.grid(row=30, column=4)

# StellarNet PL buttons

# wellgui = well_gui(root)
# threeDGui = threeD_plot(root)
#PLS = PL_SN_filedialog(root)

SelectWellsButton_PL = Button(root, bg = HIERNtheme.mygreen, fg = HIERNtheme.mywhite, font = HIERNtheme.standard_font, width = 15, text = 'StellarNet - start', command = lambda: well_gui(root).show('one'))
SelectWellsButton_PL.grid(row=9, column=0)


# MyUtils.chosen = well_gui(root).MyUtils.chosen

PLS = PL_SN_filedialog(root)



folder_selected = PLS.folder_selected
all_filenames = PLS.all_filenames
BaSO4 = PLS.BaSO4



GaussFits_PL = PLS_fit.GaussFits_PL
PL_corrected = PLS_fit.PL_corrected
GaussFits_PL_norm = PLS_fit.GaussFits_PL_norm
PL_data_norm = PLS_fit.PL_data_norm

Plot_PL = Button(root, bg = HIERNtheme.myturquoise, fg = HIERNtheme.mywhite, font = HIERNtheme.standard_font, width = 15, text = 'plot', command = lambda: PLS_plot.PLS_plotting(MyUtils.chosen, path.completeName1, PL_corrected, GaussFits_PL, root))
Plot_PL.grid(row=11, column=0)

# Norm_PL = Button(root, bg = HIERNtheme.myturquoise, fg = HIERNtheme.mywhite, font = HIERNtheme.standard_font, width = 15, text = 'norm', command = lambda: PLS_plot.PLS_plotting_norm(MyUtils.chosen, path.completeName2, PL_data_norm, GaussFits_PL_norm, PL_corrected, root))
# Norm_PL.grid(row=13, column=0)

Norm_PL = Button(root, bg = HIERNtheme.myturquoise, fg = HIERNtheme.mywhite, font = HIERNtheme.standard_font, width = 15, text = 'comparison', command = lambda: PLS_plot(root).overlaying_plot())
Norm_PL.grid(row=13, column=0)


Start_3D_Button_PL = Button(root, bg = HIERNtheme.mylime, fg = HIERNtheme.mywhite, font = HIERNtheme.standard_font, width = 15, text = 'start 3D evaluation', command = lambda: threeD_plot(root).show())
Start_3D_Button_PL.grid(row=19, column=0)

# Tecan PL buttons

SelectWellsButton_PL_T = Button(root, bg = HIERNtheme.mygreen, fg = HIERNtheme.mywhite, font = HIERNtheme.standard_font, width = 15, text = 'Tecan - start', command = lambda: well_gui(root).show('six'))
SelectWellsButton_PL_T.grid(row=23, column=0)

Plot_PL_T = Button(root, bg = HIERNtheme.myturquoise, fg = HIERNtheme.mywhite, font = HIERNtheme.standard_font, width = 15, text = 'plot', command = lambda: PL_Tecan_Plot.PL_Tecan_plotting(MyUtils.chosen, PL_Tecan_Fit.PL_data, PL_Tecan_Fit.GaussFits_PL,  path.completeName1, root))
Plot_PL_T.grid(row=25, column=0)

Norm_PL_T = Button(root, bg = HIERNtheme.myturquoise, fg = HIERNtheme.mywhite, font = HIERNtheme.standard_font, width = 15, text = 'comparison', command = lambda: PL_Tecan_Plot(root).overlaying_plot())
Norm_PL_T.grid(row=27, column=0)

Start_3D_Button_PL_T = Button(root, bg = HIERNtheme.mylime, fg = HIERNtheme.mywhite, font = HIERNtheme.standard_font, width = 15, text = 'start 3D evaluation', command = lambda: threeD_plot(root).show())
Start_3D_Button_PL_T.grid(row=29, column=0)

# PLE buttons

# TPLE = PLE_Tecan_filedialog(root)

Button_PLE = Button(root, bg = HIERNtheme.mygreen, fg = HIERNtheme.mywhite, font = HIERNtheme.standard_font, width = 15, text = 'start', command = lambda: well_gui(root).show('two'))
Button_PLE.grid(row=9, column=1)

GaussFits_PLE = PLE_Tecan_fit.GaussFits_PLE
GaussFits_PLE_norm = PLE_Tecan_fit.GaussFits_PLE_norm
PLE_data_norm = PLE_Tecan_fit.PLE_data_norm
PLE_data = PLE_Tecan_fit.PLE_data
GaussCurvesT = PLE_Tecan_fit.GaussCurvesT
LinearFits_Eg = PLE_Tecan_fit.LinearFits_Eg
max_index = PLE_Tecan_fit.max_index
Eg = PLE_Tecan_fit.Eg

Plot_PLE = Button(root, bg = HIERNtheme.myturquoise, fg = HIERNtheme.mywhite, font = HIERNtheme.standard_font, width = 15, text = 'plot', command = lambda: PLE_Tecan_plot.PLE_plotting(MyUtils.chosen, PLE_data, GaussFits_PLE, path.completeName1, root))
Plot_PLE.grid(row=11, column=1)

# Norm_PLE = Button(root, bg = HIERNtheme.myturquoise, fg = HIERNtheme.mywhite, font = HIERNtheme.standard_font, width = 15, text = 'norm', command = lambda: PLE_Tecan_plot.PLE_plotting_norm(MyUtils.chosen, PLE_data, PLE_data_norm, GaussFits_PLE_norm, path.completeName2, root))
# Norm_PLE.grid(row=13, column=1)

Norm_PLE = Button(root, bg = HIERNtheme.myturquoise, fg = HIERNtheme.mywhite, font = HIERNtheme.standard_font, width = 15, text = 'comparison', command = lambda: PLE_Tecan_plot(root).overlaying_plot())
Norm_PLE.grid(row=13, column=1)

bandgap_plot = Button(root, bg=HIERNtheme.myturquoise, fg=HIERNtheme.mywhite, text='bandgap', font=HIERNtheme.standard_font, width=15, command= lambda: PLE_Tecan_plot.PLE_plotting_Eg(MyUtils.chosen, PLE_data,LinearFits_Eg, GaussCurvesT, max_index, path.completeName9, root))
bandgap_plot.grid(row=15, column=1)

Start_3D_Button_PLE = Button(root, bg = HIERNtheme.mylime, fg = HIERNtheme.mywhite, font = HIERNtheme.standard_font, width = 15, text = 'start 3D evaluation', command = lambda: threeD_plot(root).show() )
Start_3D_Button_PLE.grid(row=19, column=1)

# D_Eg = threeD_plot_Eg(root)

Start_3D_Eg_PLE = Button(root, bg = HIERNtheme.mylime, fg = HIERNtheme.mywhite, font = HIERNtheme.standard_font, width = 15, text = 'start 3D bandgap', command = lambda: threeD_plot_Eg(root).show())
Start_3D_Eg_PLE.grid(row=19, column=1)

# reflectance buttons

SelectWellsButton_reflectance = Button(root, bg = HIERNtheme.mygreen, fg = HIERNtheme.mywhite, font = HIERNtheme.standard_font, width = 15, text = 'start', command = lambda: well_gui(root).show('three'))
SelectWellsButton_reflectance.grid(row=9, column=2)

absorbance = ref_correction.absorbance

# wellgui = well_gui(root)
# MyUtils.chosen = wellgui.MyUtils.chosen
# print(MyUtils.chosen)

Plot_reflectance = Button(root, bg = HIERNtheme.myturquoise, fg = HIERNtheme.mywhite, font = HIERNtheme.standard_font, width = 15, text = 'plot', command = lambda: ref_plot.ref_plotting(MyUtils.chosen, path.completeName2, absorbance, root))
Plot_reflectance.grid(row=11, column=2)

direct_reflectance = Button(root, bg = HIERNtheme.myturquoise, fg = HIERNtheme.mywhite, font = HIERNtheme.standard_font, width = 15, text = 'direct Tauc', command = lambda: ref_plot.directEg_plotting(MyUtils.chosen, path.completeName5, absorbance, root) )
direct_reflectance.grid(row=13, column=2)

indirect_reflectance = Button(root, bg = HIERNtheme.myturquoise, fg = HIERNtheme.mywhite, font = HIERNtheme.standard_font, width = 15, text = 'indirect Tauc', command = lambda: ref_plot.indirectEg_plotting(MyUtils.chosen, path.completeName6, absorbance, root) )
indirect_reflectance.grid(row=15, column=2)

comparison_reflectance = Button(root, bg = HIERNtheme.myturquoise, fg = HIERNtheme.mywhite, font = HIERNtheme.standard_font, width = 15, text = 'comparison', command = lambda: ref_plot(root).overlaying_plot())
comparison_reflectance.grid(row=17, column=2)

Start_3D_Button_reflectance = Button(root, bg = HIERNtheme.mylime, fg = HIERNtheme.mywhite, font = HIERNtheme.standard_font, width = 15, text = 'start 3D evaluation', command = lambda: Tauc_plot_Eg(root).show() )
Start_3D_Button_reflectance.grid(row=19, column=2)


# Raman buttons

# Raman_files = Raman_dialog(root)

SelectWellsButton_Raman = Button(root, bg = HIERNtheme.mygreen, fg = HIERNtheme.mywhite, font = HIERNtheme.standard_font, width = 15, text = 'start', command = lambda: well_gui(root).show('four') )
SelectWellsButton_Raman.grid(row=9, column=3)

Raman_data = Raman_data_evaluation.Raman_data
maxima_list = Raman_data_evaluation.maxima_list
local_max = Raman_data_evaluation.local_max
LorentzFits_Raman = Raman_data_evaluation.LorentzFits_Raman
x_Raman = Raman_data_evaluation.x_Raman

Plot_peaks_Raman = Button(root, bg = HIERNtheme.myturquoise, fg = HIERNtheme.mywhite, font = HIERNtheme.standard_font, width = 15, text = 'peaks', command = lambda: Raman_plotting.Raman_peak_plotting(MyUtils.chosen, x_Raman, Raman_data, maxima_list, local_max))
Plot_peaks_Raman.grid(row=11, column=3)

# single_show = plot_selection(root)

Plot_single_Raman = Button(root, bg = HIERNtheme.myturquoise, fg = HIERNtheme.mywhite, font = HIERNtheme.standard_font, width = 15, text = 'single', command = lambda: plot_selection(root).Raman_single_plotting(folder_selected.get(), Raman_data, LorentzFits_Raman, maxima_list))
Plot_single_Raman.grid(row=13, column=3)

Plot_all_Raman = Button(root, bg = HIERNtheme.myturquoise, fg = HIERNtheme.mywhite, font = HIERNtheme.standard_font, width = 15, text = 'plot', command = lambda: Raman_plotting.Raman_fit_plotting(MyUtils.chosen, x_Raman, Raman_data, LorentzFits_Raman) )
Plot_all_Raman.grid(row=15, column=3)

comparison_Raman = Button(root, bg = HIERNtheme.myturquoise, fg = HIERNtheme.mywhite, font = HIERNtheme.standard_font, width = 15, text = 'comparison', command = lambda: Raman_plotting(root).overlaying_plot() )
comparison_Raman.grid(row=17, column=3)

Start_3D_Button_Raman = Button(root, bg = HIERNtheme.mylime, fg = HIERNtheme.mywhite, font = HIERNtheme.standard_font, width = 15, text = 'start 3D evaluation', command = lambda: plot_Raman_D(root).Raman_threeD_plotting(folder_selected.get()) )
Start_3D_Button_Raman.grid(row=19, column=3)

# tr PL buttons

SelectWellsButton_trPL = Button(root, bg = HIERNtheme.mygreen, fg = HIERNtheme.mywhite, font = HIERNtheme.standard_font, width = 15, text = 'start', command = lambda: well_gui(root).show('five') )
SelectWellsButton_trPL.grid(row=9, column=4)

# wellgui = well_gui(root)
# MyUtils.chosen = well_gui(root).MyUtils.chosen

averaged_trPL = Button(root, bg = HIERNtheme.myturquoise, fg = HIERNtheme.mywhite, font = HIERNtheme.standard_font, width = 15, text = 'averaged', command = lambda: trPL_plotting.trPL_plot_averaged_exponential(MyUtils.chosen, path.completeName11))
averaged_trPL.grid(row=11, column=4)

stretched_trPL = Button(root, bg = HIERNtheme.myturquoise, fg = HIERNtheme.mywhite, font = HIERNtheme.standard_font, width = 15, text = 'stretched', command = lambda: trPL_plotting.trPL_plot_stretched_exponential(MyUtils.chosen, path.completeName21))
stretched_trPL.grid(row=13, column=4)

comparison_trPL = Button(root, bg = HIERNtheme.myturquoise, fg = HIERNtheme.mywhite, font = HIERNtheme.standard_font, width = 15, text = 'comparison', command = lambda: trPL_plotting(root).overlaying_plot() )
comparison_trPL.grid(row=15, column=4)

averaged_3D_Button_trPL = Button(root, bg = HIERNtheme.mylime, fg = HIERNtheme.mywhite, font = HIERNtheme.standard_font, width = 15, text = 'start 3D averaged', command = lambda: threeD_plot_lifetime(root).show_averaged() )
averaged_3D_Button_trPL.grid(row=19, column=4)

stretched_3D_Button_trPL = Button(root, bg = HIERNtheme.mylime, fg = HIERNtheme.mywhite, font = HIERNtheme.standard_font, width = 15, text = 'start 3D stretched', command = lambda: threeD_plot_lifetime(root).show_stretched() )
stretched_3D_Button_trPL.grid(row=21, column=4)


# test distancing

Label(root, width=1, height=1, bg=HIERNtheme.mywhite).grid(row=10, column=5)
#Label(root, width=1, height=1, bg=HIERNtheme.mywhite).grid(row=12, column=5)
#Label(root, width=1, height=1, bg=HIERNtheme.mywhite).grid(row=14, column=5)
Label(root, width=1, height=1, bg=HIERNtheme.mywhite).grid(row=18, column=5)
Label(root, width=1, height=1, bg=HIERNtheme.mywhite).grid(row=24, column=5)
Label(root, width=1, height=1, bg=HIERNtheme.mywhite).grid(row=22, column=5)
# Label(root, width=1, height=1, bg=HIERNtheme.mywhite).grid(row=26, column=5)
Label(root, width=1, height=1, bg=HIERNtheme.mywhite).grid(row=28, column=5)
Label(root, width=1, height=1, bg=HIERNtheme.mywhite).grid(row=31, column=5)

root.mainloop()

