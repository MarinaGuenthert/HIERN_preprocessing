# from Raman_filedialog import Raman_dialog
import scipy as sp
import pandas as pd
from threading import Thread

from lmfit.models import LorentzianModel
from lmfit.models import PolynomialModel
from lmfit.models import QuadraticModel
from lmfit.models import LinearModel

from scipy.signal import find_peaks

from myutils import MyUtils


class Raman_data_evaluation(Thread):

    
    LorentzFits_Raman = [None]*96 
    BaselineFit = [None]*96   
    Reports_Raman = [None]*96
    x_Raman = [None]*96
    Raman_data = pd.DataFrame(data=None)
    local_max = [None]*96
    maxima_list = [None]*96
    problem = [None]*96

    def Raman_findpeaks(chosen, SiO2, all_filenames, folder_selected, baseline, minimum, maximum):

        Raman_data_evaluation.LorentzFits_Raman = [None]*96    
        Raman_data_evaluation.Reports_Raman = [None]*96
        Raman_data_evaluation.x_Raman = [None]*96
        Raman_data_evaluation.Raman_data = pd.DataFrame(data=None)
        Raman_data_evaluation.local_max = [None]*96
        Raman_data_evaluation.maxima_list = [None]*96
        Raman_data_evaluation.problem = [None]*96

        # import Raman data

        Raman_list = []

        main_dataframe = pd.DataFrame(pd.read_csv(all_filenames[0], engine = 'python', sep = '\t', header = None, on_bad_lines='skip', skiprows=150))
        
        if MyUtils.plate[0] not in MyUtils.chosen:
            main_dataframe.insert(0, MyUtils.plate[0]+'x', None)
            main_dataframe.insert(1, MyUtils.plate[0]+'y', None)

        for i in range(1,len(all_filenames)):
        # for i in range(1,48):
            # if MyUtils.plate[i] in MyUtils.chosen:
            data = pd.read_csv(all_filenames[i], engine = 'python', sep = '\t', header = None, on_bad_lines='skip', skiprows=150)
            df = pd.DataFrame(data)
            main_dataframe = pd.concat([main_dataframe,df],axis=1)
            # else:
            #     main_dataframe.insert(i, MyUtils.plate[i]+'x', None)
            #     main_dataframe.insert(i+1, MyUtils.plate[i]+'y', None)
        # print(main_dataframe[0:10])

        length = len(main_dataframe.columns)
        # print(length)

        for i in range(1,48):
            if MyUtils.plate[i] not in MyUtils.chosen:
        #         if length > 2*i:
                main_dataframe.insert(2*i, MyUtils.plate[i]+'x', None)
                main_dataframe.insert(2*i+1, MyUtils.plate[i]+'y', None)
                    # print(main_dataframe[0:10])
        #         if length <= 2*i:
        #             df = pd.DataFrame([[None, None]], columns=[MyUtils.plate[i] + 'x', MyUtils.plate[i] + 'y'])
        #             main_dataframe = pd.concat([main_dataframe,df], axis=1)
                    # print(main_dataframe[0:10])
                    # main_dataframe.append(MyUtils.plate[i]+'y', None)

        Raman_data_evaluation.Raman_data = pd.concat([Raman_data_evaluation.Raman_data, main_dataframe], axis = 1)

        # print(Raman_data_evaluation.Raman_data.iloc[0:10])


        # correction for SiO2 peak at 521 cm^-1

        SiO2_spectrum = pd.DataFrame(pd.read_csv(SiO2, engine = 'python', sep = '\t', header = None, on_bad_lines='skip', skiprows=150))

        #print(SiO2_spectrum)

        x_SiO2 = SiO2_spectrum.iloc[:,1]
        peaks, properties = find_peaks(x_SiO2, height = 165)
            
        #print(SiO2_spectrum.iloc[peaks[0],0])

        pos = SiO2_spectrum.iloc[peaks[0],0]

        diff = 521 - pos

        #print(diff)
        #print(Raman_data_evaluation.Raman_data.iloc[5,0])

        for k in range(0,96,2):
            if k%2 == 0:
                j = int(k/2)
                if MyUtils.plate[j] in MyUtils.chosen:
                    Raman_data_evaluation.Raman_data.iloc[:,k] = Raman_data_evaluation.Raman_data.iloc[:,k] + diff

        #print(Raman_data_evaluation.Raman_data.iloc[5,0])

        #from scipy.signal import find_peaks


        local_max_x = [0]
        local_max_y = [0]

        #x = Raman_data_evaluation.Raman_data.iloc[0:290,1]
        #peaks, properties = find_peaks(x, prominence = (None, 15), distance = 20, height = 163.75)
        #print(peaks)

        # baseline correction

        if baseline == 'on':

            for k in range(0, 96, 2):
                if k%2 == 0:
                    j = int(k/2)

                    if MyUtils.plate[j] in MyUtils.chosen:

                        Raman_data_evaluation.x_Raman.pop(k)
                        Raman_data_evaluation.x_Raman.insert(k, Raman_data_evaluation.Raman_data.iloc[:290,k])

                        quadratic = QuadraticModel(nan_policy = 'omit', prefix='quadratic_')
                        pars = quadratic.guess(Raman_data_evaluation.x_Raman[k], Raman_data_evaluation.Raman_data.iloc[:290,k+1])

                        pars['quadratic_a'].set(value=100000)
                        pars['quadratic_b'].set(value=180000000)

                        mod = quadratic

                        Raman_data_evaluation.BaselineFit.pop(k)
                        Raman_data_evaluation.BaselineFit.insert(k, mod.fit(Raman_data_evaluation.Raman_data.iloc[:290,k+1], pars, x=Raman_data_evaluation.x_Raman[k]))

                        # substract baseline

                        Raman_data_evaluation.Raman_data.iloc[:290, k+1] = Raman_data_evaluation.Raman_data.iloc[:290, k+1] - Raman_data_evaluation.BaselineFit[k].best_fit




        for k in range(0,96,2):
            # print('bla')
            if k%2 == 0:
                # print('yes')
                j = int(k/2)
                if MyUtils.plate[j] in MyUtils.chosen:
                    #Raman_data_evaluation.maxima_list[k] = Raman_data_evaluation.local_max_x
                    #Raman_data_evaluation.local_max[k] = Raman_data_evaluation.local_max_y
                    #print(Raman_data_evaluation.maxima_list)
                    #print(Raman_data_evaluation.local_max)
                    x = Raman_data_evaluation.Raman_data.iloc[0:290,k+1]
                    peaks, properties = find_peaks(x, prominence = (float(minimum), float(maximum)), distance = 20) # height = 50, 
                    #print(peaks)
                    #Raman_data_evaluation.local_max[k] = peaks.tolist()
                    test = peaks.tolist()
                    local_max_x = [0]
                    local_max_y = [0]
                    for bla in test:
                        peak_y = Raman_data_evaluation.Raman_data.iloc[bla, k+1]
                        peak_x = Raman_data_evaluation.Raman_data.iloc[bla,k]
                        #print(peak_x)
                        local_max_x.append(peak_x)
                        local_max_y.append(peak_y)
                        #print(Raman_data_evaluation.local_max_x)
                    Raman_data_evaluation.maxima_list.pop(k)
                    Raman_data_evaluation.maxima_list.insert(k, local_max_x)
                    Raman_data_evaluation.local_max.pop(k)
                    Raman_data_evaluation.local_max.insert(k, local_max_y)



        #print(Raman_data_evaluation.maxima_list)
        #print(Raman_data_evaluation.local_max)


    def Raman_fitting(chosen, SiO2, all_filenames, folder_selected, baseline, minimum, maximum):

        # Raman_data_evaluation.LorentzFits_Raman = [None]*96    
        # Raman_data_evaluation.Reports_Raman = [None]*96
        # Raman_data_evaluation.x_Raman = [None]*96
        # Raman_data_evaluation.Raman_data = pd.DataFrame(data=None)
        # Raman_data_evaluation.local_max = [None]*96
        # Raman_data_evaluation.maxima_list = [None]*96
        # Raman_data_evaluation.problem = [None]*96


        parameters_Raman = [None]*96

            
        # lorentzian model

        for k in range(0,96,2):
            if k%2 == 0:
                j = int(k/2)

                if MyUtils.plate[j] in MyUtils.chosen:
            
                    
                    Raman_data_evaluation.x_Raman.pop(k)
                    Raman_data_evaluation.x_Raman.insert(k, Raman_data_evaluation.Raman_data.iloc[:290,k])
                    
                    linear = LinearModel()
                    pars = linear.guess(Raman_data_evaluation.x_Raman[k], Raman_data_evaluation.Raman_data.iloc[:290,k+1])
                    
                    # quadratic = QuadraticModel(nan_policy = 'omit', prefix='quadratic_')
                    # pars.update(quadratic.make_params())

                    # pars['quadratic_a'].set(value=100000)
                    # pars['quadratic_b'].set(value=180000000)

                    if len(Raman_data_evaluation.maxima_list[k]) == 2:
                        
                        #print(plate[n])
                    
                        lorentz1 = LorentzianModel(prefix='l1_')
                        pars.update(lorentz1.make_params())

                        pars['l1_center'].set(value=Raman_data_evaluation.maxima_list[k][1], min=Raman_data_evaluation.maxima_list[k][1] -10, max=Raman_data_evaluation.maxima_list[k][1] +10)
                        pars['l1_amplitude'].set(value=5, min=1) #, max=Raman_data_evaluation.maxima_list[k][1] +10)

                        mod = lorentz1 + linear #+ quadratic #+ lorentz3 #+ polynomial #  + lorentz4 
                        
                        Raman_data_evaluation.LorentzFits_Raman.pop(k)
                        Raman_data_evaluation.LorentzFits_Raman.insert(k, mod.fit(Raman_data_evaluation.Raman_data.iloc[:290,k+1], pars, x=Raman_data_evaluation.x_Raman[k]))
                        Raman_data_evaluation.Reports_Raman.pop(k)
                        Raman_data_evaluation.Reports_Raman.insert(k, Raman_data_evaluation.LorentzFits_Raman[k].fit_report(min_correl=0.01))
                        
                        if Raman_data_evaluation.LorentzFits_Raman[k].redchi >= 0.02:
                            
                            #print(plate[n])
                            
                            lorentz2 = LorentzianModel(prefix='l2_')
                            pars.update(lorentz2.make_params())
                            pars['l2_center'].set(value=Raman_data_evaluation.maxima_list[k][1])#, min=130, max=170)
                            pars['l2_amplitude'].set(value=5, min=1) #, max=Raman_data_evaluation.maxima_list[k][1] +10)
                            
                            mod = lorentz1 + lorentz2 + linear #+ quadratic #+ lorentz3 #+ polynomial #  + lorentz4 
                        
                            Raman_data_evaluation.LorentzFits_Raman.pop(k)
                            Raman_data_evaluation.LorentzFits_Raman.insert(k, mod.fit(Raman_data_evaluation.Raman_data.iloc[:290,k+1], pars, x=Raman_data_evaluation.x_Raman[k]))
                            Raman_data_evaluation.Reports_Raman.pop(k)
                            Raman_data_evaluation.Reports_Raman.insert(k, Raman_data_evaluation.LorentzFits_Raman[k].fit_report(min_correl=0.01))
                            
                    #      Raman_data_evaluation.maxima_list[k].append(Raman_data_evaluation.maxima_list[k][1])
                    #     print(str(k))
                        #    k = k - 2
                        #   print('bla' +str(k))
                    
                    if len(Raman_data_evaluation.maxima_list[k]) == 3:
                        
                        #print(plate[n])
                    #  print(str(k))
                    
                        lorentz1 = LorentzianModel(prefix='l1_')
                        pars.update(lorentz1.make_params())

                        lorentz2 = LorentzianModel(prefix='l2_')
                        pars.update(lorentz2.make_params())

                        pars['l1_center'].set(value=Raman_data_evaluation.maxima_list[k][1], min=Raman_data_evaluation.maxima_list[k][1] -10, max=Raman_data_evaluation.maxima_list[k][1] +10)
                        pars['l2_center'].set(value=Raman_data_evaluation.maxima_list[k][2], min=Raman_data_evaluation.maxima_list[k][2] -10, max=Raman_data_evaluation.maxima_list[k][2] +10)
                        pars['l1_amplitude'].set(value=5, min=1) #, max=Raman_data_evaluation.maxima_list[k][1] +10)
                        pars['l2_amplitude'].set(value=5, min=1) #, max=Raman_data_evaluation.maxima_list[k][1] +10)

                        mod = lorentz1 + lorentz2 + linear #+ quadratic #+ lorentz3 #+ polynomial #  + lorentz4 
                        
                        Raman_data_evaluation.LorentzFits_Raman.pop(k)
                        Raman_data_evaluation.LorentzFits_Raman.insert(k, mod.fit(Raman_data_evaluation.Raman_data.iloc[:290,k+1], pars, x=Raman_data_evaluation.x_Raman[k]))
                        Raman_data_evaluation.Reports_Raman.pop(k)
                        Raman_data_evaluation.Reports_Raman.insert(k, Raman_data_evaluation.LorentzFits_Raman[k].fit_report(min_correl=0.01))
                        
                        if Raman_data_evaluation.LorentzFits_Raman[k].redchi >= 0.02:
                            
                            #print(plate[n])
                            
                            lorentz3 = LorentzianModel(prefix='l3_')
                            pars.update(lorentz3.make_params())
                            pars['l3_center'].set(value=Raman_data_evaluation.maxima_list[k][1])#, min=130, max=170)
                            pars['l3_amplitude'].set(value=5, min=1) #, max=Raman_data_evaluation.maxima_list[k][1] +10)
                            
                            mod = lorentz1 + lorentz2 + linear + lorentz3 #+ quadratic #+ polynomial #  + lorentz4 
                        
                            Raman_data_evaluation.LorentzFits_Raman.pop(k)
                            Raman_data_evaluation.LorentzFits_Raman.insert(k, mod.fit(Raman_data_evaluation.Raman_data.iloc[:290,k+1], pars, x=Raman_data_evaluation.x_Raman[k]))
                            Raman_data_evaluation.Reports_Raman.pop(k)
                            Raman_data_evaluation.Reports_Raman.insert(k, Raman_data_evaluation.LorentzFits_Raman[k].fit_report(min_correl=0.01))
                    
                    elif len(Raman_data_evaluation.maxima_list[k]) == 4:
                        
                        #print(plate[n])
                    # print(str(k))
                    
                        lorentz1 = LorentzianModel(prefix='l1_')
                        pars.update(lorentz1.make_params())

                        lorentz2 = LorentzianModel(prefix='l2_')
                        pars.update(lorentz2.make_params())


                        lorentz3 = LorentzianModel(prefix='l3_')
                        pars.update(lorentz3.make_params())

                        pars['l1_center'].set(value=Raman_data_evaluation.maxima_list[k][1], min=Raman_data_evaluation.maxima_list[k][1] -10, max=Raman_data_evaluation.maxima_list[k][1] +10)
                        pars['l2_center'].set(value=Raman_data_evaluation.maxima_list[k][2], min=Raman_data_evaluation.maxima_list[k][2] -10, max=Raman_data_evaluation.maxima_list[k][2] +10)
                        pars['l3_center'].set(value=Raman_data_evaluation.maxima_list[k][3], min=Raman_data_evaluation.maxima_list[k][3] -10, max=Raman_data_evaluation.maxima_list[k][3] +10)
                        pars['l1_amplitude'].set(value=5, min=1) #, max=Raman_data_evaluation.maxima_list[k][1] +10)
                        pars['l2_amplitude'].set(value=5, min=1) #, max=Raman_data_evaluation.maxima_list[k][1] +10)
                        pars['l3_amplitude'].set(value=5, min=1) #, max=Raman_data_evaluation.maxima_list[k][1] +10)
                    

                        mod = lorentz1 + lorentz2 + linear + lorentz3 #+ quadratic  #+ polynomial #  + lorentz4 
                        
                        Raman_data_evaluation.LorentzFits_Raman.pop(k)
                        Raman_data_evaluation.LorentzFits_Raman.insert(k, mod.fit(Raman_data_evaluation.Raman_data.iloc[:290,k+1], pars, x=Raman_data_evaluation.x_Raman[k]))
                        Raman_data_evaluation.Reports_Raman.pop(k)
                        Raman_data_evaluation.Reports_Raman.insert(k, Raman_data_evaluation.LorentzFits_Raman[k].fit_report(min_correl=0.01))
                        
                        if Raman_data_evaluation.LorentzFits_Raman[k].redchi >= 0.02:
                            
                            #print(plate[n])
                            
                            lorentz4 = LorentzianModel(prefix='l4_')
                            pars.update(lorentz4.make_params())
                            pars['l4_center'].set(value=Raman_data_evaluation.maxima_list[k][1])#, min=130, max=170)
                            pars['l4_amplitude'].set(value=5, min=1) #, max=Raman_data_evaluation.maxima_list[k][1] +10)
                            
                            mod = lorentz1 + lorentz2 + linear + lorentz3 + lorentz4 #+ quadratic
                        
                            Raman_data_evaluation.LorentzFits_Raman.pop(k)
                            Raman_data_evaluation.LorentzFits_Raman.insert(k, mod.fit(Raman_data_evaluation.Raman_data.iloc[:290,k+1], pars, x=Raman_data_evaluation.x_Raman[k]))
                            Raman_data_evaluation.Reports_Raman.pop(k)
                            Raman_data_evaluation.Reports_Raman.insert(k, Raman_data_evaluation.LorentzFits_Raman[k].fit_report(min_correl=0.01))
                        
                    # if Raman_data_evaluation.Raman_data_evaluation.LorentzFits_Raman[k].redchi >= 0.02:
                        #    Raman_data_evaluation.maxima_list[k].append(Raman_data_evaluation.maxima_list[k][1])
                        #   print(str(k))
                        #  k = k - 2
                        # print('bla' +str(k))
                        
                    elif len(Raman_data_evaluation.maxima_list[k]) == 5:
                        
                        #print(plate[n])
                    # print(str(k))
                    
                        lorentz1 = LorentzianModel(prefix='l1_')
                        pars.update(lorentz1.make_params())

                        lorentz2 = LorentzianModel(prefix='l2_')
                        pars.update(lorentz2.make_params())

                        lorentz3 = LorentzianModel(prefix='l3_')
                        pars.update(lorentz3.make_params())
                        
                        lorentz4 = LorentzianModel(prefix='l4_')
                        pars.update(lorentz4.make_params())

                        pars['l1_center'].set(value=Raman_data_evaluation.maxima_list[k][1], min=Raman_data_evaluation.maxima_list[k][1] -10, max=Raman_data_evaluation.maxima_list[k][1] +10)
                        pars['l2_center'].set(value=Raman_data_evaluation.maxima_list[k][2], min=Raman_data_evaluation.maxima_list[k][2] -10, max=Raman_data_evaluation.maxima_list[k][2] +10)
                        pars['l3_center'].set(value=Raman_data_evaluation.maxima_list[k][3], min=Raman_data_evaluation.maxima_list[k][3] -10, max=Raman_data_evaluation.maxima_list[k][3] +10)
                        pars['l4_center'].set(value=Raman_data_evaluation.maxima_list[k][4], min=Raman_data_evaluation.maxima_list[k][4] -10, max=Raman_data_evaluation.maxima_list[k][4] +10)
                        pars['l1_amplitude'].set(value=5, min=1) #, max=Raman_data_evaluation.maxima_list[k][1] +10)
                        pars['l2_amplitude'].set(value=5, min=1) #, max=Raman_data_evaluation.maxima_list[k][1] +10)
                        pars['l3_amplitude'].set(value=5, min=1) #, max=Raman_data_evaluation.maxima_list[k][1] +10)
                        pars['l4_amplitude'].set(value=5, min=1) #, max=Raman_data_evaluation.maxima_list[k][1] +10)
                        
                

                        mod = lorentz1 + lorentz2 + linear + lorentz3 + lorentz4 #+ quadratic #+ polynomial  
                    
                        Raman_data_evaluation.LorentzFits_Raman.pop(k)
                        Raman_data_evaluation.LorentzFits_Raman.insert(k, mod.fit(Raman_data_evaluation.Raman_data.iloc[:290,k+1], pars, x=Raman_data_evaluation.x_Raman[k]))
                        Raman_data_evaluation.Reports_Raman.pop(k)
                        Raman_data_evaluation.Reports_Raman.insert(k, Raman_data_evaluation.LorentzFits_Raman[k].fit_report(min_correl=0.01)) 
                        
                        if Raman_data_evaluation.LorentzFits_Raman[k].redchi >= 0.02:
                            
                            #print(plate[n])
                            
                            lorentz5 = LorentzianModel(prefix='l5_')
                            pars.update(lorentz5.make_params())
                            pars['l5_center'].set(value=Raman_data_evaluation.maxima_list[k][1])#, min=130, max=170)
                            pars['l5_amplitude'].set(value=5, min=1) #, max=Raman_data_evaluation.maxima_list[k][1] +10)
                            
                            mod = lorentz1 + lorentz2 + linear + lorentz3 + lorentz4 + lorentz5 #+ quadratic
                        
                            Raman_data_evaluation.LorentzFits_Raman.pop(k)
                            Raman_data_evaluation.LorentzFits_Raman.insert(k, mod.fit(Raman_data_evaluation.Raman_data.iloc[:290,k+1], pars, x=Raman_data_evaluation.x_Raman[k]))
                            Raman_data_evaluation.Reports_Raman.pop(k)
                            Raman_data_evaluation.Reports_Raman.insert(k, Raman_data_evaluation.LorentzFits_Raman[k].fit_report(min_correl=0.01))
                        
                    # if Raman_data_evaluation.Raman_data_evaluation.LorentzFits_Raman[k].redchi >= 0.02:
                        #    Raman_data_evaluation.maxima_list[k].append(Raman_data_evaluation.maxima_list[k][1])
                        #   print(str(k))
                        #  k = k - 2
                        # print('bla' +str(k))
                    
                    elif len(Raman_data_evaluation.maxima_list[k]) == 6:
                        
                        #print(plate[n])
                        #print(str(k))
                    
                        lorentz1 = LorentzianModel(prefix='l1_')
                        pars.update(lorentz1.make_params())

                        lorentz2 = LorentzianModel(prefix='l2_')
                        pars.update(lorentz2.make_params())

                        lorentz3 = LorentzianModel(prefix='l3_')
                        pars.update(lorentz3.make_params())
                        
                        lorentz4 = LorentzianModel(prefix='l4_')
                        pars.update(lorentz4.make_params())
                        
                        lorentz5 = LorentzianModel(prefix='l5_')
                        pars.update(lorentz5.make_params())

                        pars['l1_center'].set(value=Raman_data_evaluation.maxima_list[k][1], min=Raman_data_evaluation.maxima_list[k][1] -10, max=Raman_data_evaluation.maxima_list[k][1] +10)
                        pars['l2_center'].set(value=Raman_data_evaluation.maxima_list[k][2], min=Raman_data_evaluation.maxima_list[k][2] -10, max=Raman_data_evaluation.maxima_list[k][2] +10)
                        pars['l3_center'].set(value=Raman_data_evaluation.maxima_list[k][3], min=Raman_data_evaluation.maxima_list[k][3] -10, max=Raman_data_evaluation.maxima_list[k][3] +10)
                        pars['l4_center'].set(value=Raman_data_evaluation.maxima_list[k][4], min=Raman_data_evaluation.maxima_list[k][4] -10, max=Raman_data_evaluation.maxima_list[k][4] +10)
                        pars['l5_center'].set(value=Raman_data_evaluation.maxima_list[k][5], min=Raman_data_evaluation.maxima_list[k][5] -10, max=Raman_data_evaluation.maxima_list[k][5] +10)
                        pars['l1_amplitude'].set(value=5, min=1) #, max=Raman_data_evaluation.maxima_list[k][1] +10)
                        pars['l2_amplitude'].set(value=5, min=1) #, max=Raman_data_evaluation.maxima_list[k][1] +10)
                        pars['l3_amplitude'].set(value=5, min=1) #, max=Raman_data_evaluation.maxima_list[k][1] +10)
                        pars['l4_amplitude'].set(value=5, min=1) #, max=Raman_data_evaluation.maxima_list[k][1] +10)
                        pars['l5_amplitude'].set(value=5, min=1) #, max=Raman_data_evaluation.maxima_list[k][1] +10)
                

                        mod = lorentz1 + lorentz2 + linear + lorentz3 + lorentz4 + lorentz5 #+ quadratic #+ polynomial
                    
                    # Lorentzian Fit

                        Raman_data_evaluation.LorentzFits_Raman.pop(k)
                        Raman_data_evaluation.LorentzFits_Raman.insert(k, mod.fit(Raman_data_evaluation.Raman_data.iloc[:290,k+1], pars, x=Raman_data_evaluation.x_Raman[k]))
                        Raman_data_evaluation.Reports_Raman.pop(k)
                        Raman_data_evaluation.Reports_Raman.insert(k, Raman_data_evaluation.LorentzFits_Raman[k].fit_report(min_correl=0.01))
                        
                        if Raman_data_evaluation.LorentzFits_Raman[k].redchi >= 0.02:
                            
                            #print(plate[n])
                            
                            lorentz6 = LorentzianModel(prefix='l6_')
                            pars.update(lorentz6.make_params())
                            pars['l6_center'].set(value=Raman_data_evaluation.maxima_list[k][1])#, min=130, max=170)
                            pars['l6_amplitude'].set(value=5, min=1) #, max=Raman_data_evaluation.maxima_list[k][1] +10)
                            
                            mod = lorentz1 + lorentz2 + linear + lorentz3 + lorentz4 + lorentz5 + lorentz6 #+ quadratic
                        
                            Raman_data_evaluation.LorentzFits_Raman.pop(k)
                            Raman_data_evaluation.LorentzFits_Raman.insert(k, mod.fit(Raman_data_evaluation.Raman_data.iloc[:290,k+1], pars, x=Raman_data_evaluation.x_Raman[k]))
                            Raman_data_evaluation.Reports_Raman.pop(k)
                            Raman_data_evaluation.Reports_Raman.insert(k, Raman_data_evaluation.LorentzFits_Raman[k].fit_report(min_correl=0.01))
                        
                        #if Raman_data_evaluation.Raman_data_evaluation.LorentzFits_Raman[k].redchi >= 0.02:
                        #   Raman_data_evaluation.maxima_list[k].append(Raman_data_evaluation.maxima_list[k][1])
                        #  print(str(k))
                        # k = k - 2     
                            #print('bla' + str(k))
                        
                        
                    elif len(Raman_data_evaluation.maxima_list[k]) == 7:
                        
                        #print(plate[n])
                        #print(str(k))
                    
                        lorentz1 = LorentzianModel(prefix='l1_')
                        pars.update(lorentz1.make_params())

                        lorentz2 = LorentzianModel(prefix='l2_')
                        pars.update(lorentz2.make_params())

                        lorentz3 = LorentzianModel(prefix='l3_')
                        pars.update(lorentz3.make_params())
                        
                        lorentz4 = LorentzianModel(prefix='l4_')
                        pars.update(lorentz4.make_params())
                        
                        lorentz5 = LorentzianModel(prefix='l5_')
                        pars.update(lorentz5.make_params())
                        
                        lorentz6 = LorentzianModel(prefix='l6_')
                        pars.update(lorentz6.make_params())

                        pars['l1_center'].set(value=Raman_data_evaluation.maxima_list[k][1], min=Raman_data_evaluation.maxima_list[k][1] -10, max=Raman_data_evaluation.maxima_list[k][1] +10)
                        pars['l2_center'].set(value=Raman_data_evaluation.maxima_list[k][2], min=Raman_data_evaluation.maxima_list[k][2] -10, max=Raman_data_evaluation.maxima_list[k][2] +10)
                        pars['l3_center'].set(value=Raman_data_evaluation.maxima_list[k][3], min=Raman_data_evaluation.maxima_list[k][3] -10, max=Raman_data_evaluation.maxima_list[k][3] +10)
                        pars['l4_center'].set(value=Raman_data_evaluation.maxima_list[k][4], min=Raman_data_evaluation.maxima_list[k][4] -10, max=Raman_data_evaluation.maxima_list[k][4] +10)
                        pars['l5_center'].set(value=Raman_data_evaluation.maxima_list[k][5], min=Raman_data_evaluation.maxima_list[k][5] -10, max=Raman_data_evaluation.maxima_list[k][5] +10)
                        pars['l6_center'].set(value=Raman_data_evaluation.maxima_list[k][6], min=Raman_data_evaluation.maxima_list[k][6] -10, max=Raman_data_evaluation.maxima_list[k][6] +10)
                        pars['l1_amplitude'].set(value=5, min=1) #, max=Raman_data_evaluation.maxima_list[k][1] +10)
                        pars['l2_amplitude'].set(value=5, min=1) #, max=Raman_data_evaluation.maxima_list[k][1] +10)
                        pars['l3_amplitude'].set(value=5, min=1) #, max=Raman_data_evaluation.maxima_list[k][1] +10)
                        pars['l4_amplitude'].set(value=5, min=1) #, max=Raman_data_evaluation.maxima_list[k][1] +10)
                        pars['l5_amplitude'].set(value=5, min=1) #, max=Raman_data_evaluation.maxima_list[k][1] +10)
                        pars['l6_amplitude'].set(value=5, min=1) #, max=Raman_data_evaluation.maxima_list[k][1] +10)
                

                        mod = lorentz1 + lorentz2 + linear + lorentz3 + lorentz4 + lorentz5 + lorentz6 #+ quadratic #+ polynomial 

                # Lorentzian Fit

                        Raman_data_evaluation.LorentzFits_Raman.pop(k)
                        Raman_data_evaluation.LorentzFits_Raman.insert(k, mod.fit(Raman_data_evaluation.Raman_data.iloc[:290,k+1], pars, x=Raman_data_evaluation.x_Raman[k]))
                        Raman_data_evaluation.Reports_Raman.pop(k)
                        Raman_data_evaluation.Reports_Raman.insert(k, Raman_data_evaluation.LorentzFits_Raman[k].fit_report(min_correl=0.01))
                        
                        if Raman_data_evaluation.LorentzFits_Raman[k].redchi >= 0.02:
                            
                            #print(plate[n])
                            
                            lorentz7 = LorentzianModel(prefix='l7_')
                            pars.update(lorentz7.make_params())
                            pars['l7_center'].set(value=Raman_data_evaluation.maxima_list[k][1])#, min=130, max=170)
                            pars['l7_amplitude'].set(value=5, min=1) #, max=Raman_data_evaluation.maxima_list[k][1] +10)
                            
                            mod = lorentz1 + lorentz2 + linear + lorentz3 + lorentz4 + lorentz5 + lorentz6 + lorentz7 #+ quadratic
                        
                            Raman_data_evaluation.LorentzFits_Raman.pop(k)
                            Raman_data_evaluation.LorentzFits_Raman.insert(k, mod.fit(Raman_data_evaluation.Raman_data.iloc[:290,k+1], pars, x=Raman_data_evaluation.x_Raman[k]))
                            Raman_data_evaluation.Reports_Raman.pop(k)
                            Raman_data_evaluation.Reports_Raman.insert(k, Raman_data_evaluation.LorentzFits_Raman[k].fit_report(min_correl=0.01))
                    

                    elif len(Raman_data_evaluation.maxima_list[k]) == 8:
                        
                        #print(plate[n])
                        #print(str(k))
                    
                        lorentz1 = LorentzianModel(prefix='l1_')
                        pars.update(lorentz1.make_params())

                        lorentz2 = LorentzianModel(prefix='l2_')
                        pars.update(lorentz2.make_params())

                        lorentz3 = LorentzianModel(prefix='l3_')
                        pars.update(lorentz3.make_params())
                        
                        lorentz4 = LorentzianModel(prefix='l4_')
                        pars.update(lorentz4.make_params())
                        
                        lorentz5 = LorentzianModel(prefix='l5_')
                        pars.update(lorentz5.make_params())
                        
                        lorentz6 = LorentzianModel(prefix='l6_')
                        pars.update(lorentz6.make_params())

                        lorentz7 = LorentzianModel(prefix='l7_')
                        pars.update(lorentz7.make_params())

                        pars['l1_center'].set(value=Raman_data_evaluation.maxima_list[k][1], min=Raman_data_evaluation.maxima_list[k][1] -10, max=Raman_data_evaluation.maxima_list[k][1] +10)
                        pars['l2_center'].set(value=Raman_data_evaluation.maxima_list[k][2], min=Raman_data_evaluation.maxima_list[k][2] -10, max=Raman_data_evaluation.maxima_list[k][2] +10)
                        pars['l3_center'].set(value=Raman_data_evaluation.maxima_list[k][3], min=Raman_data_evaluation.maxima_list[k][3] -10, max=Raman_data_evaluation.maxima_list[k][3] +10)
                        pars['l4_center'].set(value=Raman_data_evaluation.maxima_list[k][4], min=Raman_data_evaluation.maxima_list[k][4] -10, max=Raman_data_evaluation.maxima_list[k][4] +10)
                        pars['l5_center'].set(value=Raman_data_evaluation.maxima_list[k][5], min=Raman_data_evaluation.maxima_list[k][5] -10, max=Raman_data_evaluation.maxima_list[k][5] +10)
                        pars['l6_center'].set(value=Raman_data_evaluation.maxima_list[k][6], min=Raman_data_evaluation.maxima_list[k][6] -10, max=Raman_data_evaluation.maxima_list[k][6] +10)
                        pars['l7_center'].set(value=Raman_data_evaluation.maxima_list[k][7], min=Raman_data_evaluation.maxima_list[k][7] -10, max=Raman_data_evaluation.maxima_list[k][7] +10)
                        pars['l1_amplitude'].set(value=5, min=1) #, max=Raman_data_evaluation.maxima_list[k][1] +10)
                        pars['l2_amplitude'].set(value=5, min=1) #, max=Raman_data_evaluation.maxima_list[k][1] +10)
                        pars['l3_amplitude'].set(value=5, min=1) #, max=Raman_data_evaluation.maxima_list[k][1] +10)
                        pars['l4_amplitude'].set(value=5, min=1) #, max=Raman_data_evaluation.maxima_list[k][1] +10)
                        pars['l5_amplitude'].set(value=5, min=1) #, max=Raman_data_evaluation.maxima_list[k][1] +10)
                        pars['l6_amplitude'].set(value=5, min=1) #, max=Raman_data_evaluation.maxima_list[k][1] +10)
                        pars['l7_amplitude'].set(value=5, min=1) 

                        mod = lorentz1 + lorentz2 + linear + lorentz3 + lorentz4 + lorentz5 + lorentz6 + lorentz7 #+ quadratic #+ polynomial 

                # Lorentzian Fit

                        Raman_data_evaluation.LorentzFits_Raman.pop(k)
                        Raman_data_evaluation.LorentzFits_Raman.insert(k, mod.fit(Raman_data_evaluation.Raman_data.iloc[:290,k+1], pars, x=Raman_data_evaluation.x_Raman[k]))
                        Raman_data_evaluation.Reports_Raman.pop(k)
                        Raman_data_evaluation.Reports_Raman.insert(k, Raman_data_evaluation.LorentzFits_Raman[k].fit_report(min_correl=0.01))
                        
                        if Raman_data_evaluation.LorentzFits_Raman[k].redchi >= 0.02:
                            
                            #print(plate[n])
                            
                            lorentz8 = LorentzianModel(prefix='l8_')
                            pars.update(lorentz8.make_params())
                            pars['l8_center'].set(value=Raman_data_evaluation.maxima_list[k][1])#, min=130, max=170)
                            pars['l8_amplitude'].set(value=5, min=1) #, max=Raman_data_evaluation.maxima_list[k][1] +10)
                            
                            mod = lorentz1 + lorentz2 + linear + lorentz3 + lorentz4 + lorentz5 + lorentz6 + lorentz7 + lorentz8 #+ quadratic
                        
                            Raman_data_evaluation.LorentzFits_Raman.pop(k)
                            Raman_data_evaluation.LorentzFits_Raman.insert(k, mod.fit(Raman_data_evaluation.Raman_data.iloc[:290,k+1], pars, x=Raman_data_evaluation.x_Raman[k]))
                            Raman_data_evaluation.Reports_Raman.pop(k)
                            Raman_data_evaluation.Reports_Raman.insert(k, Raman_data_evaluation.LorentzFits_Raman[k].fit_report(min_correl=0.01))
                    

                    else:

                        # mod = linear + quadratic

                        Raman_data_evaluation.Reports_Raman.pop(k)
                        Raman_data_evaluation.Reports_Raman.insert(k, "not able to fit")
                        #print(Raman_data_evaluation.Raman_data_evaluation.x_Raman[0:10])

                        

        # difference = []
        # percent = []
        # problem_list = []

        # for i in range(0,96,2):
        #     problem_list.clear()
        #     difference.clear()
        #     percent.clear()


        #     for point in range(0,len(Raman_data_evaluation.maxima_list[i])):

        #         if Raman_data_evaluation.maxima_list[i][point] != 'None':

        #             print(Raman_data_evaluation.Raman_data.iloc[Raman_data_evaluation.maxima_list[i][point]:Raman_data_evaluation.maxima_list[i][point+1],i+1])
        #             print(Raman_data_evaluation.LorentzFits_Raman[i].best_fit[Raman_data_evaluation.maxima_list[i][point]])

        #             difference.append(Raman_data_evaluation.Raman_data.iloc[Raman_data_evaluation.maxima_list[i][point]:Raman_data_evaluation.maxima_list[i][point+1],i+1] - Raman_data_evaluation.LorentzFits_Raman[i].best_fit[Raman_data_evaluation.maxima_list[i][point]])
        #             percent.append(Raman_data_evaluation.Raman_data.iloc[Raman_data_evaluation.maxima_list[i][point]:Raman_data_evaluation.maxima_list[i][point+1],i+1] /100 * 5)

        #             if difference[point] >= percent[point]:
        #                 problem_list.append('yes')
        #             else:
        #                 problem_list.append('no')
            
        #     Raman_data_evaluation.problem.pop(i)
        #     Raman_data_evaluation.problem.insert(i, problem_list)


        # Raman fit correction

        for k in range(0,96,2):
            if k%2 == 0:

                j = int(k/2)

                if MyUtils.plate[j] in MyUtils.chosen:
                    if len(Raman_data_evaluation.maxima_list[k]) <= 8 and len(Raman_data_evaluation.maxima_list[k]) >=2:

                        difference = Raman_data_evaluation.Raman_data.iloc[0:290,k+1] - Raman_data_evaluation.LorentzFits_Raman[k].best_fit

                        if (difference >= 2).any():
                            Raman_data_evaluation.problem[k] = 'yes'
                        else:
                            Raman_data_evaluation.problem[k] = 'no'
                    else:
                        Raman_data_evaluation.problem[k] = 'no'
                

        print(Raman_data_evaluation.problem)
        print('done')



