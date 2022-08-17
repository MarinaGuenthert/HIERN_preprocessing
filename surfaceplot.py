import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.tri as tri
from matplotlib import cm
import scipy
from scipy.interpolate import griddata
from matplotlib.ticker import LinearLocator
# from colorspacious import cspace_converter

fn = diluted = r'C:\Users\mguen\Documents\Studium\Master_of_Science\HI-ERN\Masterthesis\measurements\original\PL_PLE\StellarNet\luminescence_365nm\plate2\untreated\vertical\PL_fit_height.csv' # path to Excel file
# df = pd.read_excel(fn_summary,engine='openpyxl',sheet_name = sn) # load corresponding dataset
df = pd.read_csv(fn, sep=',', engine='python') # load corresponding dataset
# df.shape

# print(df)

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
        t[irow,2] = df.iloc[ii,jj+1] #*3/4
        irow += 1
        


df = pd.DataFrame(t,columns=["x", "y", "height"])

xgrid = [None]*48
ygrid = [None]*48
zgrid = [None]*48

for ii in range(0,len(df)):
     xgrid[ii] = df.iloc[ii,0]
     ygrid[ii] = df.iloc[ii,1]
     zgrid[ii] = df.iloc[ii,2]

x = xgrid
y = ygrid
z = zgrid



fig, ax = plt.subplots(figsize=(12,8), dpi=200, subplot_kw={"projection": "3d"})


X = x
Y = y
X, Y = np.meshgrid(X, Y)
Z = griddata((x,y), z, (X,Y), method='cubic')

x_i = np.linspace(0,1,100)
y_i = np.linspace(0,1,100)
X_i, Y_i = np.meshgrid(x_i, y_i)
Z_i = griddata((x, y), z, (X_i, Y_i), method='cubic')

# Plot the surface.
surf = ax.plot_surface(X_i, Y_i, Z_i, cmap='BrBG_r', rstride=1, cstride=1, 
                       linewidth=0, antialiased=False, alpha=0.5)

ax.scatter(X, Y, c=Z, edgecolor = 'black',cmap='BrBG_r')#,alpha=0.85)

# Customize the z axis.
# ax.set_zlim(-1.01, 1.01)
ax.zaxis.set_major_locator(LinearLocator(10))
# A StrMethodFormatter is used automatically
ax.zaxis.set_major_formatter('{x:.02f}')

# ax.contour(X, Y, Z, 10, lw=3, cmap='BrBG_r', linestyles="solid", offset=-1)
# ax.contour(X, Y, Z, 10, lw=3, colors='k', linestyles="solid")

ax.contourf(X, Y, Z, 40, zdir='z', offset=0.00,alpha=0.85,cmap='BrBG_r')
# ax.contour(X, Y, Z, zdir='x', offset=-0.1, cmap='BrBG_r')
# ax.contour(X, Y, Z, zdir='y', offset=1.1, cmap='BrBG_r')


ax.set_xlabel('Ag content')

ax.set_ylabel('Bi content')

ax.set_zlabel('parameter')

ax.set_title('surface plot of ...')


# Add a color bar which maps values to colors.
fig.colorbar(surf, shrink=0.5, aspect=5)




plt.show()