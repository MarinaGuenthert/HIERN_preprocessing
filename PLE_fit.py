
import pandas as pd
import numpy as np

import threading
from threading import Thread
from myutils import MyUtils

from lmfit.models import GaussianModel
from lmfit.models import LinearModel




class PLE_Tecan_fit(Thread):
    
    GaussFits_PLE = [None]*48
    GaussFits_PLE_norm = [None]*48
    PLE_data_norm = [None]*48
    PLE_data = pd.DataFrame(data=None)
    GaussCurvesT = pd.DataFrame(data=None)
    LinearFits_Eg = [None]*48
    max_index = [None]*48
    Eg = [None]*48
    
   
    # @staticmethod
    def PLE_fitting(chosen, filename, folder_selected):

        PLE_Tecan_fit.GaussFits_PLE = [None]*48
        PLE_Tecan_fit.GaussFits_PLE_norm = [None]*48
        PLE_Tecan_fit.PLE_data_norm = [None]*48
        PLE_Tecan_fit.PLE_data = pd.DataFrame(data=None)
        PLE_Tecan_fit.GaussCurvesT = pd.DataFrame(data=None)
        PLE_Tecan_fit.LinearFits_Eg = [None]*48
        PLE_Tecan_fit.max_index = [None]*48
        PLE_Tecan_fit.Eg = [None]*48


        # import PLE measurements

        PLE_Tecan_fit.PLE_data = pd.read_csv(filename, engine = 'python', sep = '\t', header = 0)

        for i in range(0,48):

            if MyUtils.plate[i] not in MyUtils.chosen:

                PLE_Tecan_fit.PLE_data.insert(loc=i+1, column=MyUtils.plate[i], value=0.0)


        # Jacobian correction
        PLE_Tecan_fit.PLE_data["Energy"] = 1240/PLE_Tecan_fit.PLE_data["Wavel."]
        PLE_Tecan_fit.PLE_data['Jacobian'] = PLE_Tecan_fit.PLE_data["Energy"]**2

        # l = 1
        for l in range(1,49):

            if MyUtils.plate[l-1] in MyUtils.chosen:
            
                PLE_Tecan_fit.PLE_data.iloc[:, l] = (PLE_Tecan_fit.PLE_data.iloc[:, 50]*PLE_Tecan_fit.PLE_data.iloc[:, l])


            
        # Gaussian Fit

        parameters_PLE = [None]*48
        #PLE_Tecan_fit.GaussFits_PLE = [None]*48

        x_PLE = PLE_Tecan_fit.PLE_data.iloc[:,49]
        mod = GaussianModel()

        for k in range(0,48):

            if MyUtils.plate[k] in MyUtils.chosen:
                parameters_PLE[k] =  mod.guess(PLE_Tecan_fit.PLE_data.iloc[:,k+1], x=x_PLE)
                parameters_PLE[k]['center'].set(min=PLE_Tecan_fit.PLE_data.iloc[-1,49], max=PLE_Tecan_fit.PLE_data.iloc[0,49])
                blub = mod.fit(PLE_Tecan_fit.PLE_data.iloc[:,k+1], parameters_PLE[k], x=x_PLE)
                PLE_Tecan_fit.GaussFits_PLE.pop(k)
                PLE_Tecan_fit.GaussFits_PLE.insert(k, blub)

        for k in range (0,48):
            if MyUtils.plate[k] in MyUtils.chosen:
                for key in PLE_Tecan_fit.GaussFits_PLE[k].params:
                    #print(MyUtils.plate[k])
                    if key == 'center':
                        if PLE_Tecan_fit.GaussFits_PLE[k].params[key].value < 0:
                            MyUtils.center_list.append(0)
                        else:
                            MyUtils.center_list.append(PLE_Tecan_fit.GaussFits_PLE[k].params[key].value)
                    if key == 'amplitude':
                        if PLE_Tecan_fit.GaussFits_PLE[k].params[key].value < 0:
                            MyUtils.amplitude_list.append(0)
                        else:
                            MyUtils.amplitude_list.append(PLE_Tecan_fit.GaussFits_PLE[k].params[key].value)
                    if key == 'height':
                        if PLE_Tecan_fit.GaussFits_PLE[k].params[key].value < 0:
                            MyUtils.height_list.append(0)
                        else:
                            MyUtils.height_list.append(PLE_Tecan_fit.GaussFits_PLE[k].params[key].value)
                    if key == 'fwhm':
                        if PLE_Tecan_fit.GaussFits_PLE[k].params[key].value < 0:
                            MyUtils.fwhm_list.append(0)
                        else:
                            MyUtils.fwhm_list.append(PLE_Tecan_fit.GaussFits_PLE[k].params[key].value)
                        #print(key, "=", GaussFits_PL[k].params[key].value, "+/-", GaussFits_PL[k].params[key].stderr)
                    #print(key, "=", GaussFits_PL[k].params[key].value, "+/-", GaussFits_PL[k].params[key].stderr)
            else:
                MyUtils.center_list.append(0)
                MyUtils.amplitude_list.append(0)
                MyUtils.height_list.append(0)
                MyUtils.fwhm_list.append(0)
          
            
        # normalization

        #PLE_Tecan_fit.PLE_data_norm = [None]*48
        #PLE_Tecan_fit.GaussFits_PLE_norm = [None]*48

        # print(PLE_Tecan_fit.GaussFits_PLE[0].best_fit)

        for m in range(1,49):
            if MyUtils.plate[m-1] in MyUtils.chosen:
                #PLE_Tecan_fit.PLE_data_norm[m-1] = PLE_Tecan_fit.PLE_data.iloc[:,m]/PLE_Tecan_fit.PLE_data.iloc[0:200,m].max()
                PLE_Tecan_fit.PLE_data_norm.pop(m-1)
                PLE_Tecan_fit.PLE_data_norm.insert(m-1, PLE_Tecan_fit.PLE_data.iloc[:,m]/PLE_Tecan_fit.GaussFits_PLE[m-1].best_fit.max())
                if not PLE_Tecan_fit.GaussFits_PLE[m-1].best_fit.max() == 0.0:
                    PLE_Tecan_fit.GaussFits_PLE_norm.pop(m-1) 
                    PLE_Tecan_fit.GaussFits_PLE_norm.insert(m-1, (PLE_Tecan_fit.GaussFits_PLE[m-1].best_fit)/(PLE_Tecan_fit.GaussFits_PLE[m-1].best_fit.max()))
                    # print(PLE_Tecan_fit.GaussFits_PLE[m-1].best_fit.max())
                else:
                    PLE_Tecan_fit.GaussFits_PLE_norm.pop(m-1) 
                    PLE_Tecan_fit.GaussFits_PLE_norm.insert(m-1, PLE_Tecan_fit.GaussFits_PLE[m-1].best_fit)
            else:
                PLE_Tecan_fit.GaussFits_PLE_norm.pop(m-1)
                PLE_Tecan_fit.GaussFits_PLE_norm.insert(m-1, [0.0, 0.0, 0.0])
                
        # print(PLE_Tecan_fit.GaussFits_PLE_norm[0])



        # convert gaussian fit list to dataframe and transpose

        #for m in range(0,48):
        #    PLE_Tecan_fit.GaussFits_PLE_norm[m-1] = PLE_Tecan_fit.GaussFits_PLE[m-1].best_fit/PLE_Tecan_fit.GaussFits_PLE[m-1].best_fit.max()
            
        
        GaussCurves = pd.DataFrame (PLE_Tecan_fit.GaussFits_PLE_norm)
        #print (GaussCurves.iloc[:,0])

        PLE_Tecan_fit.GaussCurvesT = pd.concat([PLE_Tecan_fit.GaussCurvesT, GaussCurves.transpose()], axis=1)


        print (PLE_Tecan_fit.GaussCurvesT)

        # PLE_Tecan_fit.GaussCurvesT = PLE_Tecan_fit.GaussCurvesT.replace(to_replace=None, value=[0.0, 0.0], inplace=True, regex=True)

        # print (PLE_Tecan_fit.GaussCurvesT)


        # define fitting range for bandgap

        PLE_Tecan_fit.max_index = PLE_Tecan_fit.GaussCurvesT.idxmax()

        print(PLE_Tecan_fit.max_index)


        parameters_Eg = [None]*48
        #PLE_Tecan_fit.LinearFits_Eg = [None]*48

        mod = LinearModel()

        # print(PLE_Tecan_fit.max_index)

        for k in range(0,48):
            if MyUtils.plate[k] in MyUtils.chosen:
                # print(type(PLE_Tecan_fit.max_index[k]))
                if isinstance(PLE_Tecan_fit.max_index[k], np.integer) == True:
                    if PLE_Tecan_fit.max_index[k] <= 245:
                        # print('x')
                        x_PLE = PLE_Tecan_fit.PLE_data.iloc[int(PLE_Tecan_fit.max_index[k]+15):int(PLE_Tecan_fit.max_index[k]+45),49]
                        # print(x_PLE)
                        parameters_Eg[k] =  mod.guess(PLE_Tecan_fit.GaussCurvesT.iloc[int(PLE_Tecan_fit.max_index[int(k)]+15):int(PLE_Tecan_fit.max_index[int(k)]+45),k], x=x_PLE)
                        PLE_Tecan_fit.LinearFits_Eg.pop(k) 
                        PLE_Tecan_fit.LinearFits_Eg.insert(k, mod.fit(PLE_Tecan_fit.GaussCurvesT.iloc[int(PLE_Tecan_fit.max_index[int(k)]+15):int(PLE_Tecan_fit.max_index[int(k)]+45),k], parameters_Eg[k], x=x_PLE))  

        # print(PLE_Tecan_fit.LinearFits_Eg)          
            
        # equation y=m*x+t

        m = [None]*48
        t = [None]*48
        #Eg = [None]*48
        MyUtils.Eg_list.clear()

        for n in range(0,48): 
            if MyUtils.plate[n] in MyUtils.chosen:
                if isinstance(PLE_Tecan_fit.max_index[n], np.integer) == True:
                    if not PLE_Tecan_fit.LinearFits_Eg[n] == None:
                        for name, param in PLE_Tecan_fit.LinearFits_Eg[n].params.items():
                            if name == 'slope':
                                m[n] = param.value
                            elif name == 'intercept':
                                t[n] = param.value

        for n in range(0,48):
            if MyUtils.plate[n] in MyUtils.chosen:
                if isinstance(PLE_Tecan_fit.max_index[n], np.integer) == True:
                    if not PLE_Tecan_fit.LinearFits_Eg[n] == None and t[n] != 0.0 and m[n] != 0.0:
                        # print('t: ' + str(t[n]))
                        # print('m: ' + str(m[n]))

                        PLE_Tecan_fit.Eg[n] = -(t[n]/m[n])

                        if PLE_Tecan_fit.Eg[n] < 0:
                            MyUtils.Eg_list.append(0)
                        else:
                            MyUtils.Eg_list.append(PLE_Tecan_fit.Eg[n])


                    else:
                        MyUtils.Eg_list.append(0)  

                else:
                    MyUtils.Eg_list.append(0)  
            else:
                MyUtils.Eg_list.append(0)  

        print(MyUtils.Eg_list)      
            