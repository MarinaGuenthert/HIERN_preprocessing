import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.tri as tri
from matplotlib import cm
import scipy as sp
from scipy.interpolate import griddata
from scipy import ndimage
# from colorspacious import cspace_converter

diluted = r'C:\Users\mguen\Documents\Studium\Master_of_Science\HI-ERN\Masterthesis\measurements\diluted\PL\StellarNet\365nm\plate2\untreated\results\PL_fit_amplitude.csv'
original = r'C:\Users\mguen\Documents\Studium\Master_of_Science\HI-ERN\Masterthesis\measurements\original\PL_PLE\StellarNet\luminescence_365nm\plate2\untreated\results\PL_fit_amplitude.csv' # path to Excel file

# df = pd.read_excel(fn_summary,engine='openpyxl',sheet_name = sn) # load corresponding dataset
df1 = pd.read_csv(original, sep=',', engine='python') # load corresponding dataset
df2 = pd.read_csv(diluted, sep=',', engine='python') # load corresponding dataset
# df.shape

# print(df)

vmin=0
vmax=4000
filter_switch = 'off'

# df.columns
# df.iloc[0,1]
x = [0.00, 0.10, 0.20, 0.40, 0.60, 1.00]
y2 = [0.00, 0.01, 0.02, 0.03, 0.05, 0.07, 0.09, 0.10]
y1 = [0.00, 0.10, 0.20, 0.30, 0.50, 0.70, 0.90, 1.00]

t1 = np.zeros((48, 3))
irow=0

for ii, x0 in enumerate(x):
    for jj, y0 in enumerate(y1):
        t1[irow, 0] = x0
        t1[irow,1] = y0
        t1[irow,2] = df1.iloc[ii,jj+1]
        irow += 1

t2 = np.zeros((48, 3))
irow=0

for ii, x0 in enumerate(x):
    for jj, y0 in enumerate(y2):
        t2[irow, 0] = x0
        t2[irow,1] = y0
        t2[irow,2] = df2.iloc[ii,jj+1]   * 0.71
        irow += 1
        


df1 = pd.DataFrame(t1,columns=["x", "y", "value"])
df2 = pd.DataFrame(t2,columns=['x', 'y', 'value'])

#print(df1)
#print(df2)

frames = [df1, df2]
df= pd.concat(frames)

xgrid = [None]*96
ygrid = [None]*96
zgrid = [None]*96

xgrid1 = [None]*48
ygrid1 = [None]*48
zgrid1 = [None]*48

xgrid2 = [None]*48
ygrid2 = [None]*48
zgrid2 = [None]*48

#print(df)

for ii in range(0,len(df1)):
     xgrid1[ii] = df1.iloc[ii,0]
     ygrid1[ii] = df1.iloc[ii,1]
     zgrid1[ii] = df1.iloc[ii,2]


x1 = xgrid1
y1 = ygrid1
z1 = zgrid1
# define grid.
xi1 = np.linspace(0,1,100)
yi1 = np.linspace(0,1,100)
# grid the data.

if filter_switch== 'on':
    z1 = result = sp.ndimage.median_filter(z1, size=4)
zi1 = griddata((x1, y1), z1, (xi1[None,:], yi1[:,None]), method='cubic')


for ii in range(0,len(df2)):
     xgrid2[ii] = df2.iloc[ii,0]
     ygrid2[ii] = df2.iloc[ii,1]
     zgrid2[ii] = df2.iloc[ii,2]


x2 = xgrid2
y2 = ygrid2
z2 = zgrid2
# define grid.
xi2 = np.linspace(0,1,100)
yi2 = np.linspace(0,0.1,100)
# yi = np.linspace(0,1,100)
# grid the data.

if filter_switch== 'on':
    z2 = result = sp.ndimage.median_filter(z2, size=4)
# Z_i = griddata((x, y), z, (X_i, Y_i), method='cubic')
zi2 = griddata((x2, y2), z2, (xi2[None,:], yi2[:,None]), method='cubic')

for ii in range(0,len(df)):
     xgrid[ii] = df.iloc[ii,0]
     ygrid[ii] = df.iloc[ii,1]
     zgrid[ii] = df.iloc[ii,2]

x = xgrid
y = ygrid
z = zgrid
# define grid.
xi = np.linspace(0,1,100)
yi = np.linspace(0,1,100)
# grid the data.

if filter_switch== 'on':
    z = result = sp.ndimage.median_filter(z, size=4)
zi = griddata((x, y), z, (xi[None,:], yi[:,None]), method='cubic')


fig2=plt.figure(figsize=(10, 4), dpi=100)
fig2.subplots_adjust(right=0.9, wspace=0.65)

ax1=fig2.add_subplot(131, aspect=1.3)
ax2=fig2.add_subplot(132, aspect=13)
ax3=fig2.add_subplot(133, aspect=1.3)
cbar_ax = fig2.add_axes([0.92, 0.20, 0.01, 0.59])


# Larry's code

csetf=ax1.contourf(xi1,yi1,zi1,40, zdir='z', offset=0.00,alpha=0.85,cmap='BrBG_r',vmin=vmin,vmax=vmax) # use this one for flat contours
cset=ax1.scatter(x1,y1,s=15,c=z1, edgecolor = 'black',cmap='BrBG_r',alpha=0.85,vmin=vmin,vmax=vmax) #WAS viridis alpha=1   c=self.y.reshape(-1,),
# cbar=fig2.colorbar(csetf, cax=cbar_ax)
ax1.set_title('0-100% Bi 0-100% Ag', y=1.0, pad=14)
ax1.set_xlabel('Ag content')
ax1.set_ylabel('Bi content')
ax1.set_xlim(0.0,1.0)
ax1.set_ylim(0.0,1.0)

csetf=ax2.contourf(xi2,yi2,zi2,40, zdir='z', offset=0.00,alpha=0.85,cmap='BrBG_r',vmin=vmin,vmax=vmax) # use this one for flat contours
cset=ax2.scatter(x2,y2,s=15,c=z2, edgecolor = 'black',cmap='BrBG_r',alpha=0.85,vmin=vmin,vmax=vmax) #WAS viridis alpha=1   c=self.y.reshape(-1,),
# cbar=fig2.colorbar(csetf, cax=cbar_ax)
ax2.set_title('0-10% Bi 0-100% Ag', y=1.0, pad=14)
ax2.set_xlabel('Ag content')
ax2.set_ylabel('Bi content')
ax2.set_xlim(0.0,1.0)
ax2.set_ylim(0.0,0.10)


csetf=ax3.contourf(xi,yi,zi,40, zdir='z', offset=0.00,alpha=0.85,cmap='BrBG_r',vmin=vmin,vmax=vmax) # use this one for flat contours
cset=ax3.scatter(x,y,s=15,c=z, edgecolor = 'black',cmap='BrBG_r',alpha=0.85, vmin=vmin, vmax=vmax) #WAS viridis alpha=1   c=self.y.reshape(-1,),
cbar=fig2.colorbar(csetf, cax=cbar_ax)
ax3.set_title('total amplitude', y=1.0, pad=14)
ax3.set_xlabel('Ag content')
ax3.set_ylabel('Bi content')
ax3.set_xlim(0.0,1.0)
ax3.set_ylim(0.0,1.0)




plt.show()
# if self.X_test!=[]:
#     for x,y,z in zip(pred1_plot_test,pred2_plot_test,self.y.reshape(-1,)):
#         ax2.scatter(x,y, facecolor='white', edgecolor = 'black', alpha=1,
#         vmin=np.amin(self.y.reshape(-1,)),vmax=amax(self.y.reshape(-1,)))  

