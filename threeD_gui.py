import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['animation.ffmpeg_path'] = r'C:\FFmpeg\bin\ffmpeg.exe'

from matplotlib import animation
from tkinter import Label, Button, Tk
from myutils import MyUtils
from theme import HIERNtheme
from joining import path

import os

class threeD_plot(tk.Toplevel):
    
    def __init__(self, master: Tk):
        tk.Toplevel.__init__(self)
        
        self.__angle1 = 0
        self.__angle2 = 0
        self.__angle3 = 0
        self.__angle4 = 0
        self.__save_v = 'off'

        self.variable = tk.StringVar()
        self.__geometry = tk.StringVar()
        # self.__toggle_button = None

        self.withdraw()
        self.lift(master)
        
    def show(self):
        

        
        self.title('extrapolate fit results')
        self.__geometry.set('horizontal')
        
        # Label (self, text = 'Fitting results', bg = HIERNtheme.mywhite, fg = HIERNtheme.myblue, font = HIERNtheme.header_font) .grid(row=1, column=0, sticky=tk.W)

        # Button_plot = Button (self, text = 'Plot 3D overview', bg = HIERNtheme.myblue, fg = HIERNtheme.mywhite, font = HIERNtheme.standard_font, width = 15, command = self.__plot_3D)
        # Button_plot.grid(row=1, column=2, stick=tk.W)

        # Label (self, text = 'first', fg = HIERNtheme.myblue, bg = HIERNtheme.mywhite, font = HIERNtheme.standard_font) .grid(row=3, column=0, sticky=tk.W)

        # Button_forward1 = Button (self, text = 'turn forward', bg = HIERNtheme.mylime, fg = HIERNtheme.mywhite, font = HIERNtheme.standard_font, width = 15, command=self.__forward1)
        # Button_forward1.grid(row=3, column=1, sticky=tk.W)

        # Button_backward1 = Button (self, text = 'turn backward', bg = HIERNtheme.mylime, fg = HIERNtheme.mywhite, font = HIERNtheme.standard_font, width = 15, command=self.__backward1)
        # Button_backward1.grid(row=3, column=2, sticky=tk.W) 

        # Label (self, text = 'second', fg = HIERNtheme.myblue, bg = HIERNtheme.mywhite, font = HIERNtheme.standard_font) .grid(row=5, column=0, sticky=tk.W)

        # Button_forward2 = Button (self, text = 'turn forward', bg = HIERNtheme.mylime, fg = HIERNtheme.mywhite, font = HIERNtheme.standard_font, width = 15, command=self.__forward2)
        # Button_forward2.grid(row=5, column=1, sticky=tk.W)

        # Button_backward2 = Button (self, text = 'turn backward', bg = HIERNtheme.mylime, fg = HIERNtheme.mywhite, font = HIERNtheme.standard_font, width = 15, command=self.__backward2)
        # Button_backward2.grid(row=5, column=2, sticky=tk.W)

        # Label (self, text = 'third', fg = HIERNtheme.myblue, bg = HIERNtheme.mywhite, font = HIERNtheme.standard_font) .grid(row=7, column=0, sticky=tk.W)

        # Button_forward3 = Button (self, text = 'turn forward', bg = HIERNtheme.mylime, fg = HIERNtheme.mywhite, font = HIERNtheme.standard_font, width = 15, command=self.__forward3)
        # Button_forward3.grid(row=7, column=1, sticky=tk.W)

        # Button_backward3 = Button (self, text = 'turn backward', bg = HIERNtheme.mylime, fg = HIERNtheme.mywhite, font = HIERNtheme.standard_font, width = 15, command=self.__backward3)
        # Button_backward3.grid(row=7, column=2, sticky=tk.W)

        # Label (self, text = 'fourth', fg = HIERNtheme.myblue, bg = HIERNtheme.mywhite, font = HIERNtheme.standard_font) .grid(row=9, column=0, sticky=tk.W)

        # Button_forward4 = Button (self, text = 'turn forward', bg = HIERNtheme.mylime, fg = HIERNtheme.mywhite, font = HIERNtheme.standard_font, width = 15, command=self.__forward4)
        # Button_forward4.grid(row=9, column=1, sticky=tk.W)

        # Button_backward4 = Button (self, text = 'turn backward', bg = HIERNtheme.mylime, fg = HIERNtheme.mywhite, font = HIERNtheme.standard_font, width = 15, command=self.__backward4)
        # Button_backward4.grid(row=9, column=2, sticky=tk.W)

        # Button_forward_all = Button (self, text = 'turn all forward', bg = HIERNtheme.myblue, fg = HIERNtheme.mywhite, font = HIERNtheme.standard_font, width = 15, command=self.__forward_all)
        # Button_forward_all.grid(row=11, column=1, sticky=tk.W)

        # Button_backward_all = Button (self, text = 'turn all backward', bg = HIERNtheme.myblue, fg = HIERNtheme.mywhite, font = HIERNtheme.standard_font, width = 15, command=self.__backward_all)
        # Button_backward_all.grid(row=11, column=2, sticky=tk.W)

        #Button_save = Button (self, text = 'save figure', bg = HIERNtheme.myblue, fg = HIERNtheme.mywhite, font = HIERNtheme.standard_font, width = 15, command=self.__save)
        #Button_save.grid(row =11, column = 3, sticky = tk.W)

        label_angle = Label (self, text = 'which well should be in front for the 3D snapshot?', bg= HIERNtheme.mywhite, fg=HIERNtheme.myblue, font = HIERNtheme.header_font)
        label_angle.grid(row=7, column=0, sticky=tk.W)

        self.variable.set('Select well')

        angles = ['A1', 'A8', 'F1', 'F8']

        opt = tk.OptionMenu(self, self.variable, *angles)
        opt.grid(row = 8, column = 0, sticky=tk.W)
        opt.config(bg=HIERNtheme.mylime)

        geometry_Label = Label(self, text='In which way should the 3D plots be alligned?', bg=HIERNtheme.mywhite, fg=HIERNtheme.myblue, font=HIERNtheme.header_font)
        geometry_Label.grid(row=10, column=0, sticky = tk.W)

        self.__toggle_button = Button(self, text="horizontal", bg=HIERNtheme.mygreen, fg=HIERNtheme.mywhite, font=HIERNtheme.standard_font, command=self.__Simpletoggle)
        self.__toggle_button.grid(row=11, column=0, sticky=tk.W)

        submit_Button = Button(self, text='submit', bg=HIERNtheme.myorange, fg=HIERNtheme.mywhite, font=HIERNtheme.standard_font, command=lambda:self.__plot_3D(self.geometry, self.variable.get()))
        submit_Button.grid(row=13, column=5)

        self.configure(background=HIERNtheme.mywhite)

        self.update_idletasks()
        self.deiconify()

        #self.mainloop()

    def __Simpletoggle(self):
        
        if self.__toggle_button.config('text')[-1] == 'vertical':
            self.__toggle_button.config(text='horizontal', bg=HIERNtheme.mygreen)
            self.__geometry.set('horizontal')
        else:
            self.__toggle_button.config(text='vertical', bg=HIERNtheme.myturquoise)
            self.__geometry.set('vertical')


    # interactive 3D plot



    # def __forward_all(self):
    #     #global self.__angle1, self.__angle2, self.__angle3, self.__angle4
    #     self.__angle1 = self.__angle1 + 45
    #     self.__angle2 = self.__angle2 + 45
    #     self.__angle3 = self.__angle3 + 45
    #     self.__angle4 = self.__angle4 + 45
    #     self.__plot_3D()

    # def __backward_all(self):
    #     #global self.__angle1, self.__angle2, self.__angle3, self.__angle4
    #     self.__angle1 = self.__angle1 - 45
    #     self.__angle2 = self.__angle2 - 45
    #     self.__angle3 = self.__angle3 - 45
    #     self.__angle4 = self.__angle4 - 45
    #     self.__plot_3D()

    # def __forward1(self):
    #     #global self.__angle1
    #     self.__angle1 = self.__angle1 + 45
    #     self.__plot_3D()


    # def __backward1(self):
    #     #global self.__angle1
    #     self.__angle1 = self.__angle1 - 45
    #     self.__plot_3D()

    # def __forward2(self):
    #     #global self.__angle2
    #     self.__angle2 = self.__angle2 + 45
    #     self.__plot_3D()


    # def __backward2(self):
    #     #global self.__angle2
    #     self.__angle2 = self.__angle2 - 45
    #     self.__plot_3D()

    # def __forward3(self):
    #     #global self.__angle3
    #     self.__angle3 = self.__angle3 + 45
    #     self.__plot_3D()


    # def __backward3(self):
    #     #global self.__angle3
    #     self.__angle3 = self.__angle3- 45
    #     self.__plot_3D()

    # def __forward4(self):
    #     #global self.__angle4
    #     self.__angle4 = self.__angle4 + 45
    #     self.__plot_3D()


    # def __backward4(self):
    #     #global self.__angle4
    #     self.__angle4 = self.__angle4 - 45
    #     self.__plot_3D()

    # def __save(self):
    #     #global self.__save_v
    #     self.__save_v = 'on'
    #     self.__plot_3D()

    def __plot_3D(self, geometry, variable):

        dz1 = []
        dz2 = []
        dz3 = []
        dz4 = []
        #global self.__save_v

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

        if self.__geometry.get() == 'horizontal':

            fig=plt.figure(figsize=(10, 2.5), dpi=100)

            ax1=fig.add_subplot(141, projection='3d')
            ax2=fig.add_subplot(142, projection='3d')
            ax3=fig.add_subplot(143, projection='3d')
            ax4=fig.add_subplot(144, projection='3d')

            print('horizontal')

        elif self.__geometry.get() == 'vertical':

            fig=plt.figure(figsize=(2.5, 10), dpi=100)

            ax1=fig.add_subplot(411, projection='3d')
            ax2=fig.add_subplot(412, projection='3d')
            ax3=fig.add_subplot(413, projection='3d')
            ax4=fig.add_subplot(414, projection='3d')

            print('vertical')

        if self.variable.get() == 'A1':
            
            ax1.view_init(azim=315)
            ax2.view_init(azim=315)
            ax3.view_init(azim=315)
            ax4.view_init(azim=315)
        
        elif self.variable.get() == 'A8':

            ax1.view_init(azim=225)
            ax2.view_init(azim=225)
            ax3.view_init(azim=225)
            ax4.view_init(azim=225)

        elif self.variable.get() == 'F1':

            ax1.view_init(azim=45)
            ax2.view_init(azim=45)
            ax3.view_init(azim=45)
            ax4.view_init(azim=45)

        elif self.variable.get() == 'F8':

            ax1.view_init(azim=135)
            ax2.view_init(azim=135)
            ax3.view_init(azim=135)
            ax4.view_init(azim=135)

        ax1.set_title('height')
        ax2.set_title('center')
        ax3.set_title('amplitude')
        ax4.set_title('fwhm')

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

        g = os.path.join(self.__geometry.get(), path.completeName5)
        plt.savefig(g, transparent = False)

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

        f = os.path.join(self.__geometry.get(), path.completeNameD)
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


