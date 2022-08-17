from cmath import nan
from tkinter import HORIZONTAL
from tkinter.tix import X_REGION
from turtle import right
import pandas as pd
import csv
import os
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.tri as tri
from matplotlib import cm
from matplotlib import animation
import scipy as sp
from scipy.interpolate import griddata
from scipy import ndimage
from matplotlib.ticker import LinearLocator
plt.rcParams['animation.ffmpeg_path'] = r'C:\FFmpeg\bin\ffmpeg.exe'
# from colorspacious import cspace_converter

Cs2InBi100AgNa100 = r'C:\Users\mguen\Documents\Studium\Master_of_Science\HI-ERN\Masterthesis\measurements\HT\InBi_0-100_NaAg_0-100\PL\results\PL_fit_center.csv' # path to Excel file
Cs2InBi10AgNa100 = r'C:\Users\mguen\Documents\Studium\Master_of_Science\HI-ERN\Masterthesis\measurements\HT\InBi_0-10_NaAg_0-100\PL\results\PL_fit_center.csv' # path to Excel file
Cs2InBi1AgNa100 = r'C:\Users\mguen\Documents\Studium\Master_of_Science\HI-ERN\Masterthesis\measurements\HT\InBi_0-1_NaAg_0-100\PL\results\PL_fit_center.csv' # path to Excel file
Cs2InBi100AgNa10 = r'C:\Users\mguen\Documents\Studium\Master_of_Science\HI-ERN\Masterthesis\measurements\HT\InBi_0-100_NaAg_0-10\PL\results\PL_fit_center.csv' # path to Excel file
record = r'C:\Users\mguen\Documents\Studium\Master_of_Science\HI-ERN\Masterthesis\measurements\HT\InBi_1-6_NaAg_40-90\PL\results\PL_fit_center.csv'# path to Excel file
# df = pd.read_excel(fn_summary,engine='openpyxl',sheet_name = sn) # load corresponding dataset
df_Bi100 = pd.read_csv(Cs2InBi100AgNa100, sep=',', engine='python') # load corresponding dataset
df_Bi10 = pd.read_csv(Cs2InBi10AgNa100, sep=',', engine='python') # load corresponding dataset
df_Bi1 = pd.read_csv(Cs2InBi1AgNa100, sep=',', engine='python') # load corresponding dataset
df_Ag10 = pd.read_csv(Cs2InBi100AgNa10, sep=',', engine='python') # load corresponding dataset
df_record = pd.read_csv(record, sep=',', engine='python') # load corresponding dataset


vmin = 1.9
vmax = 2.3
filter_switch = 'on'


x_100 = [0.00, 0.10, 0.30, 0.50, 0.80, 1.00]
x_10 = [0.00, 0.010, 0.030, 0.050, 0.080, 0.10]
x_r = [0.40, 0.45, 0.55, 0.65, 0.80, 0.90]

y_100 = [0.00, 0.05, 0.10, 0.25, 0.50, 0.75, 0.90, 1.00]
y_10 = [0.00, 0.005, 0.010, 0.025, 0.050, 0.075, 0.090, 0.10]
y_1 = [0.00, 0.0005, 0.0010, 0.0025, 0.0050, 0.0075, 0.0090, 0.01]
y_r = [0.01, 0.0125, 0.015, 0.0225, 0.035, 0.0475, 0.055, 0.06]

t_Bi100 = np.zeros((48, 3))
t_Bi10 = np.zeros((48, 3))
t_Bi1 = np.zeros((48, 3))
t_Ag10 = np.zeros((48, 3))
t_record = np.zeros((48, 3))
irow=0

# Bi100
for ii, x0 in enumerate(x_100):
    for jj, y0 in enumerate(y_100):
        t_Bi100[irow, 0] = x0
        t_Bi100[irow,1] = y0
        t_Bi100[irow,2] = df_Bi100.iloc[ii,jj+1]  #*3/4
        irow += 1

# Bi10
irow=0
for ii, x0 in enumerate(x_100):
    for jj, y0 in enumerate(y_10):
        t_Bi10[irow, 0] = x0
        t_Bi10[irow,1] = y0
        t_Bi10[irow,2] = df_Bi10.iloc[ii,jj+1]  # /1.7765
        irow += 1

# Bi1
irow=0
for ii, x0 in enumerate(x_100):
    for jj, y0 in enumerate(y_1):
        t_Bi1[irow, 0] = x0
        t_Bi1[irow,1] = y0
        t_Bi1[irow,2] = df_Bi1.iloc[ii,jj+1]  # /1.7522
        irow += 1

# Ag10
irow=0
for ii, x0 in enumerate(x_10):
    for jj, y0 in enumerate(y_100):
        t_Ag10[irow, 0] = x0
        t_Ag10[irow,1] = y0
        t_Ag10[irow,2] = df_Ag10.iloc[ii,jj+1]  # /1.6234
        irow += 1

# record
irow=0
for ii, x0 in enumerate(x_r):
    for jj, y0 in enumerate(y_r):
        t_record[irow, 0] = x0
        t_record[irow,1] = y0
        t_record[irow,2] = df_record.iloc[ii,jj+1]   # *0.4801
        irow += 1
        

df_1 = pd.DataFrame(t_Bi100,columns=["x", "y", "center"])
df_2 = pd.DataFrame(t_Bi10,columns=["x", "y", "center"])
df_3 = pd.DataFrame(t_Bi1,columns=["x", "y", "center"])
df_4 = pd.DataFrame(t_Ag10,columns=["x", "y", "center"])
df_5 = pd.DataFrame(t_record,columns=["x", "y", "center"])

# with open('fit_center_Bi100_Ag100.csv', 'w', newline='') as csvfile:
#     spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
#     spamwriter.writerow(['x (Ag)', 'y (Bi)', 'z'])
#     for n in range(0,48):
#         spamwriter.writerow([df_1.iloc[n,0], df_1.iloc[n,1], df_1.iloc[n,2]])

# with open('fit_center_Bi10_Ag100.csv', 'w', newline='') as csvfile:
#     spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
#     spamwriter.writerow(['x (Ag)', 'y (Bi)', 'z'])
#     for n in range(0,48):
#         spamwriter.writerow([df_2.iloc[n,0], df_2.iloc[n,1], df_2.iloc[n,2]])

# with open('fit_center_Bi1_Ag100.csv', 'w', newline='') as csvfile:
#     spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
#     spamwriter.writerow(['x (Ag)', 'y (Bi)', 'z'])
#     for n in range(0,48):
#         spamwriter.writerow([df_3.iloc[n,0], df_3.iloc[n,1], df_3.iloc[n,2]])

# with open('fit_center_Bi100_Ag10.csv', 'w', newline='') as csvfile:
#     spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
#     spamwriter.writerow(['x (Ag)', 'y (Bi)', 'z'])
#     for n in range(0,48):
#         spamwriter.writerow([df_4.iloc[n,0], df_4.iloc[n,1], df_4.iloc[n,2]])

# with open('fit_center_record.csv', 'w', newline='') as csvfile:
#     spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
#     spamwriter.writerow(['x (Ag)', 'y (Bi)', 'z'])
#     for n in range(0,48):
#         spamwriter.writerow([df_5.iloc[n,0], df_5.iloc[n,1], df_5.iloc[n,2]])

frames = [df_1, df_2, df_3, df_4, df_5]
df= pd.concat(frames)



print(len(df))


xgrid = [None]*len(df)
ygrid = [None]*len(df)
zgrid = [None]*len(df)

for ii in range(0,len(df)):
     xgrid[ii] = df.iloc[ii,0]
     ygrid[ii] = df.iloc[ii,1]
     zgrid[ii] = df.iloc[ii,2]

# with open('fit_center_total.csv', 'w', newline='') as csvfile:
#     spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
#     spamwriter.writerow(['x (Ag)', 'y (Bi)', 'z'])
#     for n in range(0,len(df)):
#         spamwriter.writerow([df.iloc[n,0], df.iloc[n,1], df.iloc[n,2]])

x = xgrid
y = ygrid
z = zgrid




X = x
Y = y
X, Y = np.meshgrid(X, Y)

g = np.zeros((len(x), 2))
for i in range(0,len(g)):
    g[i,0]=x[i]
    g[i,1]=y[i]

# new_array = [tuple(row) for row in g]
# uniques = np.unique(new_array, axis=0)

# grid=np.zeros((100,2))

x_i = np.linspace(0.05,1,100)
y_i = np.linspace(0.015,1,100)
X_i, Y_i = np.meshgrid(x_i, y_i)

# filter_switch = 'on'

if filter_switch== 'on':
    z = result = sp.ndimage.median_filter(z, size=5)
Z_i = griddata((x, y), z, (X_i, Y_i), method='cubic')

# filter_switch = 'off'



fig3, ax = plt.subplots(figsize=(12,8), dpi=200, subplot_kw={"projection": "3d"})

# surf = ax.plot_surface(xi, yi, zi, cmap='BrBG_r', rstride=1, cstride=1, linewidth=1.0, antialiased=False, vmin=vmin, vmax=vmax)#, alpha=0.5)
surf = ax.plot_surface(X_i, Y_i, Z_i, cmap='BrBG_r', rstride=1, cstride=1, linewidth=1.0, antialiased=False, vmin=vmin, vmax=vmax)#, alpha=0.5)
ax.plot_wireframe(X_i, Y_i, Z_i, color='grey', lw=0.25, alpha=0.5)
ax.w_xaxis.set_pane_color((0.8, 0.8, 0.8, 1.0))
ax.w_yaxis.set_pane_color((0.8, 0.8, 0.8, 1.0))
ax.w_zaxis.set_pane_color((0.8, 0.8, 0.8, 1.0))

ax.contourf(X_i, Y_i, Z_i, 40, zdir='z', offset=vmin,alpha=1.00,cmap='BrBG_r', vmin=vmin, vmax=vmax)

fig3.colorbar(surf, shrink=0.7)#, shrink=2.0, aspect=0.5)
ax.view_init(elev=10., azim=45)


ax.set_xlabel('Ag content')
ax.set_xlim(0.0, 1.00)

ax.set_ylabel('Bi content')
ax.set_ylim(0.0, 1.00)

ax.set_zlabel('parameter')
ax.set_zlim(vmin, vmax)

ax.set_title('surface plot of PL center')
plt.savefig('PL_center_3D.png', transparent = False)

# Add a color bar which maps values to colors.
# fig.colorbar(surf, shrink=0.5, aspect=5)


# def init():
#     surf
#     return fig,

# def animate(i):
#     ax.view_init(elev=30., azim=1.0*i)
#     return fig,

# # Animate
# ani = animation.FuncAnimation(fig, animate, init_func=init,
#                             frames=360, interval=200, blit=False)  

# f = 'test2.mp4'
# writervideo = animation.FFMpegWriter(fps=60) 
# ani.save(f, writer=writervideo)  

# fig,ax = plt.subplots()


fig2=plt.figure(figsize=(15, 3), dpi=100)
fig2.subplots_adjust(right=0.8, wspace=0.55)
# cbar_ax = fig2.add_axes([0.10, 0.85, 0.85, 0.05])


ax1=fig2.add_subplot(151, aspect=130)
ax2=fig2.add_subplot(152, aspect=13)
ax3=fig2.add_subplot(153, aspect=1.3)
ax4=fig2.add_subplot(154, aspect=0.13)
ax5=fig2.add_subplot(155, aspect=13)

p0 = ax1.get_position().get_points().flatten()
p1 = ax5.get_position().get_points().flatten()
# p2 = ax[2].get_position().get_points().flatten()

# cbar_ax = fig2.add_axes([p0[0], 0.95, p1[2]-p0[0], 0.02])
cbar_ax = fig2.add_axes([0.82, 0.22, 0.01, 0.55])
levels = np.linspace(vmin, vmax, 20)# int((vmax-vmin)/10))



# interpolation for each individual plate

# plate 1 % Bi 


xgrid = [None]*48
ygrid = [None]*48
zgrid = [None]*48

# print(df)

for ii in range(0,48):
     xgrid[ii] = df_3.iloc[ii,0]
     ygrid[ii] = df_3.iloc[ii,1]
     zgrid[ii] = df_3.iloc[ii,2]

x = xgrid
y = ygrid
z = zgrid

# define grid.
xi = np.linspace(0,1,100)
yi = np.linspace(0,0.01,100)
Xi, Yi = np.meshgrid(xi, yi)
# grid the data.
if filter_switch== 'on':
    z = result = sp.ndimage.median_filter(z, size=5)
zi = griddata((x, y), z, (xi[None,:], yi[:,None]), method='cubic')

csetf=ax1.contourf(xi,yi,zi,40, zdir='z', offset=0.00,alpha=0.85,cmap='BrBG_r', vmin=vmin, vmax=vmax) #,vmin=vmin,vmax=vmax) # use this one for flat contours
cset=ax1.scatter(x,y,s=15,c=z, edgecolor = 'black',cmap='BrBG_r',alpha=0.85, vmin=vmin, vmax=vmax) #WAS viridis alpha=1   c=self.y.reshape(-1,),
# fig2.colorbar(csetf, cax=cbar_ax)
ax1.set_title('0-1% Bi 0-100% Ag', y=1.0, pad=14)
ax1.set_xlabel('Ag content')
ax1.set_ylabel('Bi content')
ax1.set_xlim(0.0,1.0)
ax1.set_ylim(0.0,0.01)

# plate 10% Bi

for ii in range(0,48):
     xgrid[ii] = df_2.iloc[ii,0]
     ygrid[ii] = df_2.iloc[ii,1]
     zgrid[ii] = df_2.iloc[ii,2]

x = xgrid
y = ygrid
z = zgrid

# define grid.
xi = np.linspace(0,1,100)
yi = np.linspace(0,0.1,100)
# grid the data.
if filter_switch== 'on':
    z = result = sp.ndimage.median_filter(z, size=5)
zi = griddata((x, y), z, (xi[None,:], yi[:,None]), method='cubic')

csetf=ax2.contourf(xi,yi,zi,40, zdir='z', offset=0.00,alpha=0.85,cmap='BrBG_r', vmin=vmin, vmax=vmax) #,vmin=vmin,vmax=vmax) # use this one for flat contours
cset=ax2.scatter(x,y,s=15,c=z, edgecolor = 'black',cmap='BrBG_r',alpha=0.85, vmin=vmin, vmax=vmax) #WAS viridis alpha=1   c=self.y.reshape(-1,),
# fig2.colorbar(csetf, cax=cbar_ax)
ax2.set_title('0-10% Bi 0-100% Ag', y=1.0, pad=14)
ax2.set_xlabel('Ag content')
ax2.set_ylabel('Bi content')
ax2.set_xlim(0.0,1.0)
ax2.set_ylim(0.00,0.1)

# plate 100% Bi and 100% Na

for ii in range(0,48):
     xgrid[ii] = df_1.iloc[ii,0]
     ygrid[ii] = df_1.iloc[ii,1]
     zgrid[ii] = df_1.iloc[ii,2]

x = xgrid
y = ygrid
z = zgrid

# define grid.
xi = np.linspace(0,1,100)
yi = np.linspace(0,1,100)
# grid the data.
if filter_switch== 'on':
    z = result = sp.ndimage.median_filter(z, size=5)
zi = griddata((x, y), z, (xi[None,:], yi[:,None]), method='cubic')

csetf3=ax3.contourf(xi,yi,zi,40,levels=levels, zdir='z', offset=0.00,alpha=0.85,cmap='BrBG_r', vmin=vmin, vmax=vmax) #,vmin=vmin,vmax=vmax) # use this one for flat contours
cset=ax3.scatter(x,y,s=15,c=z, edgecolor = 'black',cmap='BrBG_r',alpha=0.85, vmin=vmin, vmax=vmax) #WAS viridis alpha=1   c=self.y.reshape(-1,),
# fig2.colorbar(csetf, cax=cbar_ax)
ax3.set_title('0-100% Bi 0-100% Ag', y=1.0, pad=14)
ax3.set_xlabel('Ag content')
ax3.set_ylabel('Bi content')
ax3.set_xlim(0.0,1.0)
ax3.set_ylim(0.0,1.0)

# plate 10% Ag

for ii in range(0,48):
     xgrid[ii] = df_4.iloc[ii,0]
     ygrid[ii] = df_4.iloc[ii,1]
     zgrid[ii] = df_4.iloc[ii,2]

x = xgrid
y = ygrid
z = zgrid

# define grid.
xi = np.linspace(0,0.1,100)
yi = np.linspace(0,1,100)
# grid the data.
if filter_switch== 'on':
    z = result = sp.ndimage.median_filter(z, size=5)
zi = griddata((x, y), z, (xi[None,:], yi[:,None]), method='cubic')

csetf=ax4.contourf(xi,yi,zi,40, zdir='z', offset=0.00,alpha=0.85,cmap='BrBG_r', vmin=vmin, vmax=vmax) #,vmin=vmin,vmax=vmax) # use this one for flat contours
cset=ax4.scatter(x,y,s=15,c=z, edgecolor = 'black',cmap='BrBG_r',alpha=0.85, vmin=vmin, vmax=vmax) #WAS viridis alpha=1   c=self.y.reshape(-1,),
# fig2.colorbar(csetf, cax=cbar_ax)
ax4.set_title('0-100% Bi 0-10% Ag', y=1.0, pad=14)
ax4.set_xlabel('Ag content')
ax4.set_ylabel('Bi content')
ax4.set_xlim(0.0,0.1)
ax4.set_ylim(0.0,1.0)

# record plate

for ii in range(0,48):
     xgrid[ii] = df_5.iloc[ii,0]
     ygrid[ii] = df_5.iloc[ii,1]
     zgrid[ii] = df_5.iloc[ii,2]

x = xgrid
y = ygrid
z = zgrid

# define grid.
xi = np.linspace(0.4,0.9,100)
yi = np.linspace(0.01,0.06,100)
# grid the data.
if filter_switch== 'on':
    z = result = sp.ndimage.median_filter(z, size=5)
zi = griddata((x, y), z, (xi[None,:], yi[:,None]), method='cubic')

csetf=ax5.contourf(xi,yi,zi,40, zdir='z', offset=0.00,alpha=0.85,cmap='BrBG_r', vmin=vmin, vmax=vmax) #,vmin=vmin,vmax=vmax) # use this one for flat contours
cset=ax5.scatter(x,y,s=15,c=z, edgecolor = 'black',cmap='BrBG_r',alpha=0.85, vmin=vmin, vmax=vmax) #WAS viridis alpha=1   c=self.y.reshape(-1,),
cbar=fig2.colorbar(csetf3, cax=cbar_ax) #, orientation='horizontal', ticks=[0, 5000, 10000])
ax5.set_title('1-6% Bi 40-90% Ag', y=1.0, pad=14)
ax5.set_xlabel('Ag content')
ax5.set_ylabel('Bi content')
ax5.set_xlim(0.4,0.9)
ax5.set_ylim(0.01,0.06)

# cbar.ax.minorticks_on()
# cbar.set_ticks([0, 10000.0])
# cbar.ax5.set_xticklabels([0,5000,10000])



plt.savefig('PL_center_all.png', transparent = False)




df.sort_values(['x', 'y'], ascending=[True, True], inplace=True)


for i in range(0, len(df)-1):
    if df.iloc[i,2] == nan:
        print('nan')
    else:
        if df.iloc[i,0] == df.iloc[i+1,0] and df.iloc[i,1] == df.iloc[i+1,1]:
            j = i + 1
            z_sum = df.iloc[i,2]
            count = 1

            while df.iloc[i,0] == df.iloc[j,0] and df.iloc[i,1] == df.iloc[j,1]:
                z_sum = z_sum + df.iloc[j,2]
                count+=1
                df.iloc[j,2] = nan
                j+=1
            
            z_mean=z_sum/count
            df.iloc[i,2] = z_mean


df.dropna(inplace=True)

xgrid = [None]*len(df)
ygrid = [None]*len(df)
zgrid = [None]*len(df)

for ii in range(0,len(df)):
     xgrid[ii] = df.iloc[ii,0]
     ygrid[ii] = df.iloc[ii,1]
     zgrid[ii] = df.iloc[ii,2]

# with open('fit_center_total.csv', 'w', newline='') as csvfile:
#     spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
#     spamwriter.writerow(['x (Ag)', 'y (Bi)', 'z'])
#     for n in range(0,len(df)):
#         spamwriter.writerow([df.iloc[n,0], df.iloc[n,1], df.iloc[n,2]])

x = xgrid
y = ygrid
z = zgrid




X = x
Y = y
X, Y = np.meshgrid(X, Y)

g = np.zeros((len(x), 2))
for i in range(0,len(g)):
    g[i,0]=x[i]
    g[i,1]=y[i]

# new_array = [tuple(row) for row in g]
# uniques = np.unique(new_array, axis=0)

# grid=np.zeros((100,2))

x_i = np.linspace(0.05,1,100)
y_i = np.linspace(0.015,1,100)
X_i, Y_i = np.meshgrid(x_i, y_i)

# filter_switch = 'on'

if filter_switch== 'on':
    z = result = sp.ndimage.median_filter(z, size=5)
Z_i = griddata((x, y), z, (X_i, Y_i), method='cubic')


xi = np.mgrid[ 0.05:1:100j, 0.015:1:100j]

import scipy.interpolate

xi, yi = np.mgrid[0.05:1:100j, 0.015:1:100j]

positions = np.vstack([xi.ravel(), yi.ravel()]).T


fig, ax = plt.subplots(figsize=(12,8), dpi=200, subplot_kw={"projection": "3d"})


interp = scipy.interpolate.RBFInterpolator(g, z, neighbors=None, smoothing=0.01, kernel='thin_plate_spline', epsilon=None, degree=None) (positions)



zi = np.zeros((100, 2))

zi = interp

zi = zi.reshape(xi.shape)

# print(zi)

# zi = interp.reshape(100, 100)


# Plot the surface.
surf = ax.plot_surface(xi, yi, zi, cmap='BrBG_r', rstride=1, cstride=1, linewidth=1.0, antialiased=False, vmin=vmin, vmax=vmax)#, alpha=0.5)
# # surf = ax.plot_surface(X_i, Y_i, Z_i, cmap='BrBG_r', rstride=1, cstride=1, linewidth=1.0, antialiased=False, vmin=vmin, vmax=vmax)#, alpha=0.5)
ax.plot_wireframe(xi, yi, zi, color='grey', lw=0.25, alpha=0.5)
# ax.plot_wireframe(X_i, Y_i, Z_i, color='grey', lw=0.25, alpha=0.5)
ax.w_xaxis.set_pane_color((0.8, 0.8, 0.8, 1.0))
ax.w_yaxis.set_pane_color((0.8, 0.8, 0.8, 1.0))
ax.w_zaxis.set_pane_color((0.8, 0.8, 0.8, 1.0))
# ax.scatter(x, y, c=z, edgecolor = 'black',cmap='BrBG_r', s=5)#,alpha=0.85) # real measured points


# Customize the z axis.
# ax.set_zlim(-1.01, 1.01)
# ax.zaxis.set_major_locator(LinearLocator(10))
# A StrMethodFormatter is used automatically
# ax.zaxis.set_major_formatter('{x:.02f}')

# ax.contour(X, Y, Z, 10, lw=3, cmap='BrBG_r', linestyles="solid", offset=-1)
# ax.contour(X, Y, Z, 10, lw=3, colors='k', linestyles="solid")

# ax.contour(X_i, Y_i, Z_i, 10, lw=3, colors="k", linestyles="solid")

ax.contourf(xi, yi, zi, 40, zdir='z', offset=vmin,alpha=1.00,cmap='BrBG_r', vmin=vmin, vmax=vmax)
# ax.contour(X, Y, Z, zdir='x', offset=-0.1, cmap='BrBG_r')
# ax.contour(X, Y, Z, zdir='y', offset=1.1, cmap='BrBG_r')

fig.colorbar(surf, shrink=0.7)#, shrink=2.0, aspect=0.5)
ax.view_init(elev=10., azim=45)


ax.set_xlabel('Ag content')
ax.set_xlim(0.0, 1.00)

ax.set_ylabel('Bi content')
ax.set_ylim(0.0, 1.00)

ax.set_zlabel('parameter')
ax.set_zlim(vmin, vmax)

ax.set_title('smoothed surface plot of PL center')
plt.savefig('PL_center_smooth_3D.png', transparent = False)


plt.show()