
import pandas as pd

from myutils import MyUtils
from threading import Thread

from lmfit.models import GaussianModel




class PL_Tecan_Fit(Thread):
    
    GaussFits_PL = [None]*48
    GaussFits_PL_norm = [None]*48
    PL_data_norm = [None]*48
    PL_data = pd.DataFrame(data=None)
    x_PL = [None]

    # GaussCurvesT = pd.DataFrame(data=None)
    # LinearFits_Eg = [None]*48
    # max_index = [None]*48
    # Eg = [None]*48
    
   
    # @staticmethod
    def PL_Tecan_fitting(chosen, filename, folder_selected):

        PL_Tecan_Fit.GaussFits_PL = [None]*48
        PL_Tecan_Fit.GaussFits_PL_norm = [None]*48
        PL_Tecan_Fit.PL_data_norm = [None]*48
        PL_Tecan_Fit.PL_data = pd.DataFrame(data=None)
        PL_Tecan_Fit.x_PL = [None]


        PL_Tecan_Fit.PL_data = pd.read_csv(filename, engine = 'python', sep = '\t', header = 0)

        for i in range(0,48):

            if MyUtils.plate[i] not in MyUtils.chosen:

                PL_Tecan_Fit.PL_data.insert(loc=i+1, column=MyUtils.plate[i], value=None)


        # Jacobian        

        PL_Tecan_Fit.PL_data["Energy"] = 1240/PL_Tecan_Fit.PL_data["Wavel."]
        PL_Tecan_Fit.PL_data['Jacobian'] = PL_Tecan_Fit.PL_data["Energy"]**2

        # l = 1
        for l in range(1,49):

            if MyUtils.plate[l-1] in MyUtils.chosen:
            
                PL_Tecan_Fit.PL_data.iloc[:, l] = (PL_Tecan_Fit.PL_data.iloc[:, 50]*PL_Tecan_Fit.PL_data.iloc[:, l])



        parameters_PL = [None]*48
        # PL_Tecan_Fit.GaussFits_PL = [None]*48

        PL_Tecan_Fit.x_PL.pop(0)
        PL_Tecan_Fit.x_PL.insert(0,PL_Tecan_Fit.PL_data.iloc[:,49])

        print(PL_Tecan_Fit.PL_data)

        x_PL = PL_Tecan_Fit.PL_data.iloc[:,49]

        mod = GaussianModel()

        for k in range(0,48):

            if MyUtils.plate[k] in MyUtils.chosen:
                parameters_PL[k] =  mod.guess(PL_Tecan_Fit.PL_data.iloc[:,k+1], x=x_PL)
                parameters_PL[k]['center'].set(min=PL_Tecan_Fit.PL_data.iloc[-1,49], max=PL_Tecan_Fit.PL_data.iloc[0,49])
                PL_Tecan_Fit.GaussFits_PL.pop(k)
                PL_Tecan_Fit.GaussFits_PL.insert(k, mod.fit(PL_Tecan_Fit.PL_data.iloc[:,k+1], parameters_PL[k], x=x_PL))

        for k in range (0,48):
            if MyUtils.plate[k] in MyUtils.chosen:
                for key in PL_Tecan_Fit.GaussFits_PL[k].params:
                    #print(MyUtils.plate[k])
                    if key == 'center':
                        if PL_Tecan_Fit.GaussFits_PL[k].params[key].value < 0:
                            MyUtils.center_list.append(0)
                        else:
                            MyUtils.center_list.append(PL_Tecan_Fit.GaussFits_PL[k].params[key].value)
                    if key == 'amplitude':
                        if PL_Tecan_Fit.GaussFits_PL[k].params[key].value < 0:
                            MyUtils.amplitude_list.append(0)
                        else:
                            MyUtils.amplitude_list.append(PL_Tecan_Fit.GaussFits_PL[k].params[key].value)
                    if key == 'height':
                        if PL_Tecan_Fit.GaussFits_PL[k].params[key].value < 0:
                            MyUtils.height_list.append(0)
                        else:
                            MyUtils.height_list.append(PL_Tecan_Fit.GaussFits_PL[k].params[key].value)
                    if key == 'fwhm':
                        if PL_Tecan_Fit.GaussFits_PL[k].params[key].value < 0:
                            MyUtils.fwhm_list.append(0)
                        else:
                            MyUtils.fwhm_list.append(PL_Tecan_Fit.GaussFits_PL[k].params[key].value)
                        #print(key, "=", GaussFits_PL[k].params[key].value, "+/-", GaussFits_PL[k].params[key].stderr)
                    #print(key, "=", GaussFits_PL[k].params[key].value, "+/-", GaussFits_PL[k].params[key].stderr)
            else:
                MyUtils.center_list.append(0)
                MyUtils.amplitude_list.append(0)
                MyUtils.height_list.append(0)
                MyUtils.fwhm_list.append(0)

        # print(MyUtils.center_list)


        # PL_Tecan_Fit.PL_data_norm = [None]*48
        # PL_Tecan_Fit.GaussFits_PL_norm = [None]*48

        for m in range(1,49):

            if MyUtils.plate[m-1] in MyUtils.chosen:
                PL_Tecan_Fit.PL_data_norm.pop(m-1)
                PL_Tecan_Fit.PL_data_norm.insert(m-1, PL_Tecan_Fit.PL_data.iloc[:,m]/PL_Tecan_Fit.PL_data.iloc[:,m].max())
                PL_Tecan_Fit.GaussFits_PL_norm.pop(m-1)
                PL_Tecan_Fit.GaussFits_PL_norm.insert(m-1, PL_Tecan_Fit.GaussFits_PL[m-1].best_fit/PL_Tecan_Fit.GaussFits_PL[m-1].best_fit.max())