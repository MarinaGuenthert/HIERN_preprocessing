from cmath import sqrt
import pandas as pd
import numpy as np
# import scalar
import math
import matplotlib.pyplot as plt
import theme
import os

from myutils import MyUtils


plate = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8']
chosen = ['B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8']

# # reflectance data

# # BaSO4 = 'C:\Users\mguen\Documents\Studium\Master_of_Science\HI-ERN\Masterthesis\measurements\original\PL_PLE\StellarNet\Xenonlamp.SSM'
# path = 'C:\Users\mguen\Documents\Studium\Master_of_Science\HI-ERN\Masterthesis\measurements\original\PL_PLE\StellarNet\reflectance\plate2\untreated'
# ending = '.SSM'

# all_filenames = [None]*48

# for i in range(0,48):
#     all_filenames[i] = os.path.join(path, plate[i], ending)

# BaSO4_spectrum = pd.DataFrame(pd.read_csv(r'C:\Users\mguen\Documents\Studium\Master_of_Science\HI-ERN\Masterthesis\measurements\original\PL_PLE\StellarNet\Xenonlamp.SSM', engine = 'python', sep = '\s+', on_bad_lines='skip', skiprows=2, header = None, quoting = 3))

# r_list = []

# main_dataframe = pd.DataFrame(pd.read_csv(all_filenames[0], engine = 'python', sep = '\s+', header = None, on_bad_lines='skip', skiprows=2, quoting = 3))

# for i in range(1,46):
#     data = pd.read_csv(all_filenames[i], engine = 'python', sep = '\s+', header = None, on_bad_lines='skip', skiprows=2, quoting = 3)
#     df = pd.DataFrame(data)
#     main_dataframe = pd.concat([main_dataframe,df],axis=1)

# r_data = main_dataframe

# absorbance = pd.DataFrame(data=None)

# absorbance = pd.concat([absorbance, r_data.iloc[0:832,]], axis=1)

# for i in range(0,96,2):

#     absorbance.iloc[0:832,i+1] = (1/(BaSO4_spectrum.iloc[0:832,1] / r_data.iloc[0:832,i+1]))/100
#     absorbance.iloc[0:832,i] = 1240/ r_data.iloc[0:832,i]


df = reflectance_Eg = pd.DataFrame(pd.read_csv(r'C:\Users\mguen\Documents\Studium\Master_of_Science\HI-ERN\Masterthesis\measurements\original\PL_PLE\StellarNet\reflectance\plate2\untreated\test2\reflectance_direct_Eg.csv', sep=',', engine='python'))
PLE_table = pd.DataFrame(pd.read_csv(r'C:\Users\mguen\Documents\Studium\Master_of_Science\HI-ERN\Masterthesis\measurements\original\PL_PLE\Tecan\28012022_plate1\results\PLE_all_parameters_stderr.csv', sep=';', engine='python'))
PL_table = pd.DataFrame(pd.read_csv(r'C:\Users\mguen\Documents\Studium\Master_of_Science\HI-ERN\Masterthesis\measurements\original\PL_PLE\StellarNet\luminescence_365nm\plate2\untreated\test\PL_fit_parameters_stderr.csv', sep=';', engine='python'))
Raman_table =pd.DataFrame(pd.read_csv(r'C:\Users\mguen\Documents\Studium\Master_of_Science\HI-ERN\Masterthesis\measurements\original\Raman\31012022-plate1\results\Raman_A1g_peaks.txt', engine='python'))

# print(PLE_table.iloc[0:20])
# print(PL_table.iloc[0:20])

# PLE_table.dropna(inplace=True)

# print(PLE_table)

# t = np.zeros((48, 1))
t = [None]*48
irow=0

for ii in range(0,6):
    for jj in range(0,8):
        t[jj-8*ii] = df.iloc[ii,jj+1]
        irow += 1

print(t)

PLE_amplitude_list = [None]*48
PLE_center_list = [None]*48
PLE_sigma_list = [None]*48
PLE_Eg_list = [0]*48

PL_center_list = [None]*48
PL_sigma_list = [None]*48
PL_amplitude_list = [None]*48

E_phonon = [None]*48
# E_phonon = [0.03729]*48  # default values

print(PL_table)

for i in range (0,48):
    # if MyUtils.plate[i] in MyUtils.chosen:
    PLE_amplitude_list[i] = PLE_table.iloc[1+i*11,2]
    PLE_center_list[i] = PLE_table.iloc[2+i*11,2]
    PLE_sigma_list[i] = PLE_table.iloc[3+i*11,2]
    if not PLE_table.iloc[10+i*11,2] == None:
        PLE_Eg_list[i] = PLE_table.iloc[10+i*11,2]

    PL_amplitude_list[i] = PL_table.iloc[i*5,2]
    PL_center_list[i] = PL_table.iloc[1+i*5,2]
    PL_sigma_list[i] = PL_table.iloc[2+i*5,2]
    E_phonon[i] = Raman_table.iloc[i,0]*1/8065.5#*1000

# print(PLE_sigma_list)
# print(PL_sigma_list)
# print(PLE_center_list)
# print(PL_center_list)
# print(PLE_amplitude_list)
# print(PL_amplitude_list)

print(E_phonon)


# PL and PLE curve

def gaussian(x, sigma, A, center):
    # return np.exp((-(x-center)**2)/2*sigma**2)
    return (A/(sigma*sqrt(2*math.pi)))*np.exp((-(x-center)**2)/(2*sigma**2))


PLE_ydata = [None]*48
PL_ydata = [None]*48

for i in range(0,48):
    xdata = np.arange(0, 10, 0.01)
    PLE_sigma = float(PLE_sigma_list[i])
    PLE_center = float(PLE_center_list[i])
    PLE_A = float(PLE_amplitude_list[i])
    PLE_ydata[i] = gaussian(x=xdata, sigma=PLE_sigma, A=PLE_A, center=PLE_center)

    PL_sigma = PL_sigma_list[i]
    PL_center = PL_center_list[i]
    PL_A = PL_amplitude_list[i]
    PL_ydata[i] = gaussian(x=xdata, sigma=PL_sigma, A=PL_A, center=PL_center)
    # PL_ydata = pd.DataFrame(PL_ydata)


def factorial(n):
    if n == 0:
        return 1
    else:
        return n*factorial(n-1)

S_list = [0]*48
# E_phonon = [0.03729]*48  # default values
energy_x = [0]*48
energy_y = [0]*48



# print(PLE_Eg_list)

for i in range(0,48):
    if PLE_Eg_list[i] == 'None':
        PLE_Eg_list.pop(i)
        PLE_Eg_list.insert(i, 0.0)

# print(PLE_Eg_list)

# print(PL_ydata)


maxima_list = [0]*48
for i in range(0,48):
    arr = PL_ydata[i]
    result = np.where(arr == np.amax(arr))
    maxima_list[i] = result
# print(maxima_list)


for i in range(0,48):
    if not PLE_table.iloc[10+i*11,2] == None:
        # print(PLE_Eg_list[i])
        # print(PL_ydata[i].max())
        S_list[i] = ((float(t[i])-xdata[maxima_list[i]].max())/E_phonon[i])/2
        S_list[i] = S_list[i].real
        S_list = np.round(S_list)
        # S_list[i] = int(S_list[i])
        # S_list[i] = round(((float(PLE_Eg_list[i])-PL_ydata[i].max())/E_phonon[i])/2)
        # print('yippie')
        x_list = [0]*30
        y_list = [0]*30
        for k in range(0,30):
            x_list.pop(k)
            x_list.insert(k, float(t[i])-(2*k*E_phonon[i]))
            y_list.pop(k)
            y_list.insert(k, S_list[i]**k * np.exp(-S_list[i])/factorial(n=k))
            # energy_x[i][k] = PLE_Eg_list[i]-(2*k*E_phonon[i])
            # energy_y[i][k] = S_list[i]**k * np.exp(-S_list[i])/factorial(n=k)
            # print('yeay')

        energy_x[i] = x_list
        energy_y[i] = y_list

def NormalizeData(data):
    return (data-np.min(data))/(np.max(data)- np.min(data))

for i in range(0,48):
    energy_y[i] = NormalizeData(energy_y[i])

# print(S_list)
# print('energy_x')
# print(energy_x)
# print('energy_y')
# print(energy_y)

# i = 1
# plt.bar(energy_x[i], energy_y[i], width=E_phonon[i])
# plt.show()


# plotting

red = [1.00, 0.84, 0.70, 0.56, 0.42, 0.28, 0.14, 0.00]
green = [0.00, 0.20, 0.40, 0.60, 0.80, 1.00]
blue = [0.00]
alpha = [1.00]


fig, axs = plt.subplots(6, 8, sharex=True, sharey=True, figsize = (20,15))

fig.text(0.5, 0.0, 'energy [eV]', ha='center')
fig.text(0.0, 0.5, ' normalized intensity', va='center', rotation='vertical')

plt.xlim([1, 5])
plt.ylim([0, 1.1])

i = 0

for i in range(0,48):

    for i in range(0,8):
        k = i*2
        j = 0
        axs[j,i-8*j].set_title(MyUtils.plate[i])
        if MyUtils.plate[i] in chosen:
            if PLE_Eg_list[i] > 0.0:
                axs[j,i-8*j].plot(xdata, PLE_ydata[i]/PLE_ydata[i].max(), color=[red[i-8*j],green[j],blue[0],alpha[0]], linewidth=1.5)
                axs[j,i-8*j].plot(xdata, PL_ydata[i]/PL_ydata[i].max(), '--', color=[red[i-8*j],green[j],blue[0],alpha[0]], linewidth=1.5)
                axs[j,i-8*j].bar(energy_x[i], energy_y[i], width=E_phonon[i], color=[0.38,0.38,0.38,1])
                # axs[j,i-8*j].plot(absorbance.iloc[:832,k], absorbance.iloc[:832,k+1], 'o', color=[red[i-8*j],green[j],blue[0],alpha[0]], linewidth=1.5)
            # axs[j,i-8*j].plot(trPL_evaluation.x_trPL[k], trPL_evaluation.Fits2[i*2].best_fit, '--', color=[0.38,0.38,0.38,1], linewidth=1.5)
    for i in range(8,16):
        k = i*2
        j = 1
        axs[j,i-8*j].set_title(MyUtils.plate[i])
        if MyUtils.plate[i] in chosen:
            if PLE_Eg_list[i] > 0.0:
                axs[j,i-8*j].plot(xdata, PLE_ydata[i]/PLE_ydata[i].max(), color=[red[i-8*j],green[j],blue[0],alpha[0]], linewidth=1.5)
                axs[j,i-8*j].plot(xdata, PL_ydata[i]/PL_ydata[i].max(), '--', color=[red[i-8*j],green[j],blue[0],alpha[0]], linewidth=1.5)
                axs[j,i-8*j].bar(energy_x[i], energy_y[i], width=E_phonon[i], color=[0.38,0.38,0.38,1])
                # axs[j,i-8*j].plot(absorbance.iloc[:832,k], absorbance.iloc[:832,k+1], 'o', color=[red[i-8*j],green[j],blue[0],alpha[0]], linewidth=1.5)
    for i in range(16,24):
        k = i*2
        j = 2
        axs[j,i-8*j].set_title(MyUtils.plate[i])
        if MyUtils.plate[i] in chosen:
            if PLE_Eg_list[i] > 0.0:
                axs[j,i-8*j].plot(xdata, PLE_ydata[i]/PLE_ydata[i].max(), color=[red[i-8*j],green[j],blue[0],alpha[0]], linewidth=1.5)
                axs[j,i-8*j].plot(xdata, PL_ydata[i]/PL_ydata[i].max(), '--', color=[red[i-8*j],green[j],blue[0],alpha[0]], linewidth=1.5)
                axs[j,i-8*j].bar(energy_x[i], energy_y[i], width=E_phonon[i], color=[0.38,0.38,0.38,1])
                # axs[j,i-8*j].plot(absorbance.iloc[:832,k], absorbance.iloc[:832,k+1], 'o', color=[red[i-8*j],green[j],blue[0],alpha[0]], linewidth=1.5)
    for i in range(24,32):
        k = i*2
        j = 3
        axs[j,i-8*j].set_title(MyUtils.plate[i])
        if MyUtils.plate[i] in chosen:
            if PLE_Eg_list[i] > 0.0:
                axs[j,i-8*j].plot(xdata, PLE_ydata[i]/PLE_ydata[i].max(), color=[red[i-8*j],green[j],blue[0],alpha[0]], linewidth=1.5)
                axs[j,i-8*j].plot(xdata, PL_ydata[i]/PL_ydata[i].max(), '--', color=[red[i-8*j],green[j],blue[0],alpha[0]], linewidth=1.5)
                axs[j,i-8*j].bar(energy_x[i], energy_y[i], width=E_phonon[i], color=[0.38,0.38,0.38,1])
                # axs[j,i-8*j].plot(absorbance.iloc[:832,k], absorbance.iloc[:832,k+1], 'o', color=[red[i-8*j],green[j],blue[0],alpha[0]], linewidth=1.5)
    for i in range(32,40):
        k = i*2
        j = 4
        axs[j,i-8*j].set_title(MyUtils.plate[i])
        if MyUtils.plate[i] in chosen:
            if PLE_Eg_list[i] > 0.0:
                axs[j,i-8*j].plot(xdata, PLE_ydata[i]/PLE_ydata[i].max(), color=[red[i-8*j],green[j],blue[0],alpha[0]], linewidth=1.5)
                axs[j,i-8*j].plot(xdata, PL_ydata[i]/PL_ydata[i].max(), '--', color=[red[i-8*j],green[j],blue[0],alpha[0]], linewidth=1.5)
                axs[j,i-8*j].bar(energy_x[i], energy_y[i], width=E_phonon[i], color=[0.38,0.38,0.38,1])
                # axs[j,i-8*j].plot(absorbance.iloc[:832,k], absorbance.iloc[:832,k+1], 'o', color=[red[i-8*j],green[j],blue[0],alpha[0]], linewidth=1.5)
    for i in range(40,48):
        k = i*2
        j = 5
        axs[j,i-8*j].set_title(MyUtils.plate[i])
        if MyUtils.plate[i] in chosen:
            if PLE_Eg_list[i] > 0.0:
                axs[j,i-8*j].plot(xdata, PLE_ydata[i]/PLE_ydata[i].max(), color=[red[i-8*j],green[j],blue[0],alpha[0]], linewidth=1.5)
                axs[j,i-8*j].plot(xdata, PL_ydata[i]/PL_ydata[i].max(), '--', color=[red[i-8*j],green[j],blue[0],alpha[0]], linewidth=1.5)
                axs[j,i-8*j].bar(energy_x[i], energy_y[i], width=E_phonon[i], color=[0.38,0.38,0.38,1])  
                # axs[j,i-8*j].plot(absorbance.iloc[:832,k], absorbance.iloc[:832,k+1], 'o', color=[red[i-8*j],green[j],blue[0],alpha[0]], linewidth=1.5)      
                
    for ax in axs.flat:
        ax.label_outer()

fig.tight_layout()
fig.patch.set_facecolor('white')
# axs.set_xlim(1,5)
plt.savefig('STE_large.png', transparent = False)
plt.show()

print('done')


