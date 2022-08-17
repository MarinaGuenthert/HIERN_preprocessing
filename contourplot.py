import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.tri as tri
from matplotlib import cm
import scipy
from scipy.interpolate import griddata
# from colorspacious import cspace_converter

fn = r'C:\Users\mguen\Documents\Studium\Master_of_Science\HI-ERN\Masterthesis\measurements\original\PL_PLE\StellarNet\luminescence_365nm\plate2\untreated\vertical\PL_fit_height.csv' # path to Excel file
# df = pd.read_excel(fn_summary,engine='openpyxl',sheet_name = sn) # load corresponding dataset
df = pd.read_csv(fn, sep=',', engine='python') # load corresponding dataset
# df.shape

print(df)

# df.columns
# df.iloc[0,1]
x = [0.00, 0.10, 0.20, 0.40, 0.60, 1.00]
# y = [0.00, 0.010, 0.020, 0.030, 0.050, 0.070, 0.090, 0.10]
y = [0.00, 0.10, 0.20, 0.30, 0.50, 0.70, 0.90, 1.00]

t = np.zeros((48, 3))
irow=0

for ii, x0 in enumerate(x):
    for jj, y0 in enumerate(y):
        t[irow, 0] = x0
        t[irow,1] = y0
        t[irow,2] = df.iloc[ii,jj+1]
        irow += 1
        


df = pd.DataFrame(t,columns=["x", "y", "height"])

xgrid = [None]*48
ygrid = [None]*48
zgrid = [None]*48

print(df)

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
fig,ax = plt.subplots(figsize=plt.figaspect(0.33))
plt.axis('off')
# fig = plt.figure(figsize=plt.figaspect(0.33))
# fig.suptitle('A tale of 2 subplots')

# First subplot
ax = fig.add_subplot(1, 3, 1)

t1 = np.arange(0.0, 5.0, 0.1)
t2 = np.arange(0.0, 5.0, 0.02)
t3 = np.arange(0.0, 2.0, 0.01)

# ax.plot(t1, f(t1), 'bo',
#         t2, f(t2), 'k--', markerfacecolor='green')
# # ax.grid(True)
# ax.set_ylabel('Bi content')

CS = ax.contour(xi,yi,zi,15,linewidths=0.2, colors='k')#cmap='BrBG')
CS = ax.contourf(xi,yi,zi,15,cmap='BrBG_r')
fig.colorbar(CS)
# fig.colorbar() # draw colorbar
# plot data points.
# fig.scatter(x,y,marker='o',c='k',s=5)
# fig.xlim(-0,1)
# fig.ylim(-0,1)
# fig.title('height')
# fig.set_xlabel('Ag content')
# fig.set_ylabel('Bi content')

# Second subplot
ax = fig.add_subplot(1,3,2, projection='3d')

X = np.arange(-5, 5, 0.25)
Y = np.arange(-5, 5, 0.25)
X, Y = np.meshgrid(xgrid, ygrid)
R = np.sqrt(X**2 + Y**2)
Z = np.sin(R)

surf = ax.plot_surface(xi, yi, zi, cmap='BrBG_r')
fig.colorbar(surf, shrink = 0.5)
# ax.set_zlim(-1, 1)

# plt.show()



# Larry's code

ax = fig.add_subplot(1, 3, 3)

csetf=ax.contourf(xi,yi,zi,40, zdir='z', offset=0.00,alpha=0.85,cmap='BrBG_r') #,vmin=vmin,vmax=vmax) # use this one for flat contours
cset=ax.scatter(x,y,s=15,c=z, edgecolor = 'black',cmap='BrBG_r',alpha=0.85) #WAS viridis alpha=1   c=self.y.reshape(-1,),
fig.colorbar(csetf)
ax.set_xlim(-0.1,1.1)
ax.set_ylim(-0.1,1.1)



plt.show()
# if self.X_test!=[]:
#     for x,y,z in zip(pred1_plot_test,pred2_plot_test,self.y.reshape(-1,)):
#         ax2.scatter(x,y, facecolor='white', edgecolor = 'black', alpha=1,
#         vmin=np.amin(self.y.reshape(-1,)),vmax=amax(self.y.reshape(-1,)))  

