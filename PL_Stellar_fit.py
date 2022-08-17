from threading import Thread
import pandas as pd
import threading

from myutils import MyUtils

from lmfit.models import GaussianModel
from scipy.signal import find_peaks


class PLS_fit(Thread):
    
    GaussFits_PL = [None]*48
    GaussFits_PL_norm = [None]*48
    PL_data_norm = [None]*48
    PL_corrected = pd.DataFrame(data=None)
    
   
    @staticmethod
    def PLS_fitting(BaSO4, chosen, all_filenames, folder_selected):

        print('los gehts')

        PLS_fit.GaussFits_PL = [None]*48
        PLS_fit.GaussFits_PL_norm = [None]*48
        PLS_fit.PL_data_norm = [None]*48
        PLS_fit.PL_corrected = pd.DataFrame(data=None)
               
        # import measurements

        BaSO4_spectrum = pd.DataFrame(pd.read_csv(BaSO4, engine = 'python', sep = '\s+', on_bad_lines='skip', skiprows=2, header = None, quoting = 3))


        PL_list = []

        main_dataframe = pd.DataFrame(pd.read_csv(all_filenames[0], engine = 'python', sep = '\s+', header = None, on_bad_lines='skip', skiprows=2, quoting = 3))

        for i in range(1,len(all_filenames)):
            data = pd.read_csv(all_filenames[i], engine = 'python', sep = '\s+', header = None, on_bad_lines='skip', skiprows=2, quoting = 3)
            df = pd.DataFrame(data)
            main_dataframe = pd.concat([main_dataframe,df],axis=1)

        PL_data = pd.DataFrame(data=None)
        PL_data = pd.concat([PL_data, main_dataframe], axis=1)

        # add up to 96 columns

        if len(PL_data.columns) <= 96:
            for i in range (48):
                if MyUtils.plate[i] not in MyUtils.chosen:
                    k = i*2
                    PL_data.insert(k, str(MyUtils.plate[i]) +'x', None)
                    PL_data.insert(k+1, str(MyUtils.plate[i]) +'y', None)



        # PL LED correction

        y_BaSO4 = BaSO4_spectrum.iloc[:,1]
        peaks, properties = find_peaks(y_BaSO4, height = 30000)

        value = BaSO4_spectrum.iloc[peaks[0],1]

        # data evaluation (divide lamp reference by sample spectrum)

        PLS_fit.PL_corrected = pd.concat([PLS_fit.PL_corrected,PL_data], axis=1)

        for k in range(0,48,1):
            i = k*2
            if MyUtils.plate[k] in MyUtils.chosen:
                PLS_fit.PL_corrected.iloc[:,i+1] = PL_data.iloc[:,i+1] - (BaSO4_spectrum.iloc[:,1] / value * PL_data.iloc[peaks[0],i+1])
                PLS_fit.PL_corrected.iloc[:,i] = 1240/ PL_data.iloc[:,i]

        PLS_fit.PL_corrected.drop(PLS_fit.PL_corrected.index[0:450], inplace=True)
        PLS_fit.PL_corrected.reset_index(drop=True, inplace=True)
        
        #print(PLS_fit.PL_corrected)

        # Gaussian Fit

        parameters_PL = [None]*48
        #GaussFits_PL = [None]*48
        #GaussFits_PL = []

        mod = GaussianModel()

        for k in range(0,48):
            i = k*2
            if MyUtils.plate[k] in MyUtils.chosen:
                parameters_PL[k] =  mod.guess(PLS_fit.PL_corrected.iloc[:1200,i+1], x=PLS_fit.PL_corrected.iloc[:1200,i])
                parameters_PL[k]['center'].set(min=PLS_fit.PL_corrected.iloc[-1,i], max=PLS_fit.PL_corrected.iloc[0,i])
                blub = mod.fit(PLS_fit.PL_corrected.iloc[:1200,i+1], parameters_PL[k], x=PLS_fit.PL_corrected.iloc[:1200,i])
                PLS_fit.GaussFits_PL.pop(k)
                PLS_fit.GaussFits_PL.insert(k, blub)
                
        for k in range (0,48):
            if MyUtils.plate[k] in MyUtils.chosen:
                for key in PLS_fit.GaussFits_PL[k].params:
                    #print(MyUtils.plate[k])
                    if key == 'center':
                        if PLS_fit.GaussFits_PL[k].params[key].value < 0:
                            MyUtils.center_list.append(0)
                        else:
                            MyUtils.center_list.append(PLS_fit.GaussFits_PL[k].params[key].value)
                    if key == 'amplitude':
                        if PLS_fit.GaussFits_PL[k].params[key].value < 0:
                            MyUtils.amplitude_list.append(0)
                        else:
                            MyUtils.amplitude_list.append(PLS_fit.GaussFits_PL[k].params[key].value)
                    if key == 'height':
                        if PLS_fit.GaussFits_PL[k].params[key].value < 0:
                            MyUtils.height_list.append(0)
                        else:
                            MyUtils.height_list.append(PLS_fit.GaussFits_PL[k].params[key].value)
                    if key == 'fwhm':
                        if PLS_fit.GaussFits_PL[k].params[key].value < 0:
                            MyUtils.fwhm_list.append(0)
                        else:
                            MyUtils.fwhm_list.append(PLS_fit.GaussFits_PL[k].params[key].value)
                        #print(key, "=", GaussFits_PL[k].params[key].value, "+/-", GaussFits_PL[k].params[key].stderr)
                    #print(key, "=", GaussFits_PL[k].params[key].value, "+/-", GaussFits_PL[k].params[key].stderr)
            else:
                MyUtils.center_list.append(0)
                MyUtils.amplitude_list.append(0)
                MyUtils.height_list.append(0)
                MyUtils.fwhm_list.append(0)
                
        # normalization

        for m in range(0,48):
            k = m*2
            if MyUtils.plate[m] in MyUtils.chosen:
                PLS_fit.PL_data_norm.pop(m)
                PLS_fit.PL_data_norm.insert(m, PLS_fit.PL_corrected.iloc[:1200,k+1]/PLS_fit.PL_corrected.iloc[200:1200,k+1].max())
                PLS_fit.GaussFits_PL_norm.pop(m)
                PLS_fit.GaussFits_PL_norm.insert(m, PLS_fit.GaussFits_PL[m].best_fit/PLS_fit.GaussFits_PL[m].best_fit.max())
        


        # print(type(PLS_fit.GaussFits_PL[5].best_fit))
        # print(PLS_fit.GaussFits_PL[5].best_fit[0])
            
        #return PLS_fit.PL_corrected, PLS_fit.PL_data_norm