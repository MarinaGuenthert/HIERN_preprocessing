import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt

from trPL_fit import trPL_evaluation
plt.rcParams['animation.ffmpeg_path'] = r'C:\FFmpeg\bin\ffmpeg.exe'

from matplotlib import animation
from tkinter import Label, Button, Tk
from theme import HIERNtheme
from joining import path

from trPL_fit import trPL_evaluation



class threeD_plot_lifetime(tk.Toplevel):
    
    def __init__(self, master: Tk):
        tk.Toplevel.__init__(self)
        
        self.__angle1 = 0
        self.__angle2 = 0
        self.__angle3 = 0
        self.__angle4 = 0
        self.__save_v = 'off'

        self.variable = tk.StringVar()
        self.__geometry = tk.StringVar()

        self.withdraw()
        self.lift(master)
        
    def show_averaged(self):
        

        
        self.title('extrapolate fit results')
        self.__geometry.set('horizontal')
        
        # Label (self, text = 'Fitting results', bg = HIERNtheme.mywhite, fg = HIERNtheme.myblue, font = HIERNtheme.header_font) .grid(row=1, column=0, sticky=tk.W)

        # Button_plot = Button (self, text = 'Plot 3D overview', bg = HIERNtheme.myblue, fg = HIERNtheme.mywhite, font = HIERNtheme.standard_font, width = 15, command = self.__plot_3D)
        # Button_plot.grid(row=1, column=2, stick=tk.W)

        # Button_forward_all = Button (self, text = 'turn all forward', bg = HIERNtheme.myblue, fg = HIERNtheme.mywhite, font = HIERNtheme.standard_font, width = 15, command=self.__forward_all)
        # Button_forward_all.grid(row=11, column=1, sticky=tk.W)

        # Button_backward_all = Button (self, text = 'turn all backward', bg = HIERNtheme.myblue, fg = HIERNtheme.mywhite, font = HIERNtheme.standard_font, width = 15, command=self.__backward_all)
        # Button_backward_all.grid(row=11, column=2, sticky=tk.W)
        label_angle = Label (self, text = 'which well should be in front for the 3D snapshot?', bg= HIERNtheme.mywhite, fg=HIERNtheme.myblue, font = HIERNtheme.header_font)
        label_angle.grid(row=7, column=0, sticky=tk.W)

        self.variable.set('Select well')

        angles = ['A1', 'A8', 'F1', 'F8']

        opt = tk.OptionMenu(self, self.variable, *angles)
        opt.grid(row = 8, column = 0, sticky=tk.W)
        opt.config(bg=HIERNtheme.mylime)

        submit_Button = Button(self, text='submit', bg=HIERNtheme.myorange, fg=HIERNtheme.mywhite, font=HIERNtheme.standard_font, command=lambda:self.__plot_3D_averaged_lifetime(self.geometry, self.variable.get()))
        submit_Button.grid(row=13, column=5)

        self.configure(background=HIERNtheme.mywhite)

        self.update_idletasks()
        self.deiconify()



    def show_stretched(self):
        

        
        self.title('extrapolate fit results')
        self.__geometry.set('horizontal')
        
        # Label (self, text = 'Fitting results', bg = HIERNtheme.mywhite, fg = HIERNtheme.myblue, font = HIERNtheme.header_font) .grid(row=1, column=0, sticky=tk.W)

        # Button_plot = Button (self, text = 'Plot 3D overview', bg = HIERNtheme.myblue, fg = HIERNtheme.mywhite, font = HIERNtheme.standard_font, width = 15, command = self.__plot_3D)
        # Button_plot.grid(row=1, column=2, stick=tk.W)

        # Button_forward_all = Button (self, text = 'turn all forward', bg = HIERNtheme.myblue, fg = HIERNtheme.mywhite, font = HIERNtheme.standard_font, width = 15, command=self.__forward_all)
        # Button_forward_all.grid(row=11, column=1, sticky=tk.W)

        # Button_backward_all = Button (self, text = 'turn all backward', bg = HIERNtheme.myblue, fg = HIERNtheme.mywhite, font = HIERNtheme.standard_font, width = 15, command=self.__backward_all)
        # Button_backward_all.grid(row=11, column=2, sticky=tk.W)
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

        submit_Button = Button(self, text='submit', bg=HIERNtheme.myorange, fg=HIERNtheme.mywhite, font=HIERNtheme.standard_font, command=lambda:self.__plot_3D_stretched_lifetime(self.geometry, self.variable.get()))
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


    def __plot_3D_averaged_lifetime(self, geometry, variable):

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

        result1 = np.array(trPL_evaluation.t)


        

        fig=plt.figure(figsize=(2.5, 2.5), dpi=100)

        ax1=fig.add_subplot(111, projection='3d')


        if self.variable.get() == 'A1':
            
            ax1.view_init(azim=315)
        
        elif self.variable.get() == 'A8':

            ax1.view_init(azim=225)



        elif self.variable.get() == 'F1':

            ax1.view_init(azim=45)



        elif self.variable.get() == 'F8':

            ax1.view_init(azim=135)



        ax1.set_title('averaged lifetimes')


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

        ax1.bar3d(xposM.ravel(), yposM.ravel(), dz1*0, dx, dy, dz1, color=blub)

        fig.patch.set_facecolor(HIERNtheme.mywhite)

        g = path.completeName10
        plt.savefig(g, transparent = False)

        def init():
            ax1.bar3d(xposM.ravel(), yposM.ravel(), dz1*0, dx, dy, dz1, color=blub)
            return fig,

        def animate(i):
            ax1.view_init(elev=30., azim=1.0*i)
            return fig,

        # Animate
        ani = animation.FuncAnimation(fig, animate, init_func=init,
                                    frames=360, interval=200, blit=False)  

        f = path.completeName14 
        writervideo = animation.FFMpegWriter(fps=60) 
        ani.save(f, writer=writervideo)  

        plt.show()
        self.destroy


    def __plot_3D_stretched_lifetime(self, geometry, variable):
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

            result1 = np.array(trPL_evaluation.tau_list)
            result2 = np.array(trPL_evaluation.b_list)


            if self.__geometry.get() == 'horizontal':

                fig=plt.figure(figsize=(5, 2.5), dpi=100)

                ax1=fig.add_subplot(121, projection='3d')
                ax2=fig.add_subplot(122, projection='3d')


                print('horizontal')

            elif self.__geometry.get() == 'vertical':

                fig=plt.figure(figsize=(2.5, 5), dpi=100)

                ax1=fig.add_subplot(211, projection='3d')
                ax2=fig.add_subplot(212, projection='3d')


                print('vertical')

            if self.variable.get() == 'A1':
                
                ax1.view_init(azim=315)
                ax2.view_init(azim=315)

            
            elif self.variable.get() == 'A8':

                ax1.view_init(azim=225)
                ax2.view_init(azim=225)


            elif self.variable.get() == 'F1':

                ax1.view_init(azim=45)
                ax2.view_init(azim=45)


            elif self.variable.get() == 'F8':

                ax1.view_init(azim=135)
                ax2.view_init(azim=135)



            ax1.set_title('lifetimes')
            ax2.set_title('heterogeneity')


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

            ax2.bar3d(xposM.ravel(), yposM.ravel(), dz2*0, dx, dy, dz2, color=blub)

            fig.patch.set_facecolor(HIERNtheme.mywhite)

            g =  path.completeName20 # + self.__geometry.get()
            plt.savefig(g, transparent = False)

            def init():
                ax1.bar3d(xposM.ravel(), yposM.ravel(), dz1*0, dx, dy, dz1, color=blub)
                ax2.bar3d(xposM.ravel(), yposM.ravel(), dz2*0, dx, dy, dz2, color=blub)
                return fig,

            def animate(i):
                ax1.view_init(elev=30., azim=1.0*i)
                ax2.view_init(elev=30., azim=1.0*i)
                return fig,

            # Animate
            ani = animation.FuncAnimation(fig, animate, init_func=init,
                                        frames=360, interval=200, blit=False)  

            f =  path.completeName24 # + self.__geometry.get()
            writervideo = animation.FFMpegWriter(fps=60) 
            ani.save(f, writer=writervideo)  

            plt.show()
            self.destroy()


