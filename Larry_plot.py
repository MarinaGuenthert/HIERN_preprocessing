import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.tri as tri
from matplotlib import cm
import scipy as sp
from scipy.interpolate import griddata
from scipy import ndimage
from matplotlib.ticker import LinearLocator
# from colorspacious import cspace_converter

# fn = diluted = r'C:\Users\mguen\Documents\Studium\Master_of_Science\HI-ERN\Masterthesis\measurements\diluted\PLE\untreated\plate2\bandgap\PLE_fit_Eg.csv'
fn = original = r'C:\Users\mguen\Documents\Studium\Master_of_Science\HI-ERN\Masterthesis\measurements\iodide\StellarNet\reflectance\test\reflectance_direct_Eg.csv' # path to Excel file # path to Excel file
# df = pd.read_excel(fn_summary,engine='openpyxl',sheet_name = sn) # load corresponding dataset
df = pd.read_csv(fn, sep=',', engine='python') # load corresponding dataset
# df.shape

# print(df)

vmin=2
vmax=5
filter_switch = 'off'

# df.columns
# df.iloc[0,1]
x = [0.00, 0.10, 0.20, 0.40, 0.60, 1.00]
# x_r = [0.40, 0.45, 0.55, 0.65, 0.80, 0.90]
# y = [0.00, 0.010, 0.020, 0.030, 0.050, 0.070, 0.090, 0.10]
# y_r = [0.01, 0.0125, 0.015, 0.0225, 0.035, 0.0475, 0.055, 0.06]
y = [0.00, 0.10, 0.20, 0.30, 0.50, 0.70, 0.90, 1.00]

# x = x_r
# y = y_r

t = np.zeros((48, 3))
irow=0

for ii, x0 in enumerate(x):
    for jj, y0 in enumerate(y):
        t[irow, 0] = x0
        t[irow,1] = y0
        t[irow,2] = df.iloc[ii,jj+1] #*3/4
        irow += 1
        


df = pd.DataFrame(t,columns=["x", "y", "height"])

xgrid = [None]*48
ygrid = [None]*48
zgrid = [None]*48

# print(df)

for ii in range(0,len(df)):
     xgrid[ii] = df.iloc[ii,0]
     ygrid[ii] = df.iloc[ii,1]
     zgrid[ii] = df.iloc[ii,2]


x = xgrid
y = ygrid
z = zgrid
# define grid.
xi = np.linspace(0,1,100)
# yi = np.linspace(0,0.1,100)
yi = np.linspace(0,1,100)
# grid the data.

if filter_switch== 'on':
    z = result = sp.ndimage.median_filter(z, size=4)
# Z_i = griddata((x, y), z, (X_i, Y_i), method='cubic')
zi = griddata((x, y), z, (xi[None,:], yi[:,None]), method='cubic')

# CS = plt.contour(xi,yi,zi,15,linewidths=0.2, colors='k')#cmap='BrBG')
# CS = plt.contourf(xi,yi,zi,15,cmap='BrBG_r')
# plt.colorbar() # draw colorbar
# # plot data points.
# plt.scatter(x,y,marker='o',c='k',s=5)
# plt.xlim(-0,1)
# plt.ylim(-0,1)
# plt.title('height')
# plt.set_xlabel('Ag content')
# plt.set_ylabel('Bi content')
# plt.savefig('with_lines.png')
# plt.show()

# Set up a figure twice as tall as it is wide
fig,ax = plt.subplots(figsize=(5,5))
# plt.axis('off')
# fig = plt.figure(figsize=plt.figaspect(0.33))
# fig.suptitle('A tale of 2 subplots')

# First subplot


# Larry's code


csetf=ax.contourf(xi,yi,zi,40, zdir='z', offset=0.00,alpha=0.85,cmap='BrBG_r')#,vmin=vmin,vmax=vmax) # use this one for flat contours
cset=ax.scatter(x,y,s=15,c=z, edgecolor = 'black',cmap='BrBG_r',alpha=0.85)#,vmin=vmin,vmax=vmax) #WAS viridis alpha=1   c=self.y.reshape(-1,),
fig.colorbar(csetf)
ax.set_title('Eg')
ax.set_xlabel('Ag content')
ax.set_ylabel('Bi content')
ax.set_xlim(-0.0,1.0)
# ax.set_ylim(-0.02,0.12)
ax.set_ylim(-0.0,1.0)

plt.show()
# if self.X_test!=[]:
#     for x,y,z in zip(pred1_plot_test,pred2_plot_test,self.y.reshape(-1,)):
#         ax2.scatter(x,y, facecolor='white', edgecolor = 'black', alpha=1,
#         vmin=np.amin(self.y.reshape(-1,)),vmax=amax(self.y.reshape(-1,)))  

