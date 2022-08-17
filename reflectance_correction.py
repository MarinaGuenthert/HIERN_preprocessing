from cgi import test
import pandas as pd
from threading import Thread
import scipy

from scipy.signal import find_peaks

from myutils import MyUtils
from lmfit.models import LinearModel


class ref_correction(Thread):

    absorbance = pd.DataFrame(data=None)
    LinearFits_direct = [None]*48
    LinearFits_indirect = [None]*48
    max_index = [None]*48
    Eg_direct = [None]*48
    Eg_indirect = [None]*48
    test = [0.0] *48
    points = [0.0] *48
    
    def ref_correcting(BaSO4, chosen, all_filenames, folder_selected):

        ref_correction.Eg_direct.clear()
        ref_correction.Eg_indirect.clear()

        ref_correction.absorbance = pd.DataFrame(data=None)
        ref_correction.LinearFits_direct = [None]*48
        ref_correction.LinearFits_indirect = [None]*48
        ref_correction.max_index = [None]*48
        ref_correction.Eg_direct = [None]*48
        ref_correction.Eg_indirect = [None]*48



        # import measurements

        # print(MyUtils.chosen)

        BaSO4_spectrum = pd.DataFrame(pd.read_csv(BaSO4, engine = 'python', sep = '\s+', on_bad_lines='skip', skiprows=2, header = None, quoting = 3))

        r_list = []

        main_dataframe = pd.DataFrame(pd.read_csv(all_filenames[0], engine = 'python', sep = '\s+', header = None, on_bad_lines='skip', skiprows=2, quoting = 3))
        
        for i in range(1,len(all_filenames)):
            data = pd.read_csv(all_filenames[i], engine = 'python', sep = '\s+', header = None, on_bad_lines='skip', skiprows=2, quoting = 3)
            df = pd.DataFrame(data)
            main_dataframe = pd.concat([main_dataframe,df],axis=1)

        r_data = main_dataframe


        # add up to 96 columns

        if len(r_data.columns) <= 96:
            for i in range (48):
                if MyUtils.plate[i] not in MyUtils.chosen:
                    k = i*2
                    r_data.insert(k, str(MyUtils.plate[i]) +'x', None)
                    r_data.insert(k+1, str(MyUtils.plate[i]) +'y', None)

        # data evaluation (divide lamp reference by sample spectrum)

        ref_correction.absorbance = pd.concat([ref_correction.absorbance, r_data.iloc[0:832,]], axis=1)

        for i in range(0,96,2):

            ref_correction.absorbance.iloc[0:832,i+1] = (1/(BaSO4_spectrum.iloc[0:832,1] / r_data.iloc[0:832,i+1]))/100
            ref_correction.absorbance.iloc[0:832,i] = 1240/ r_data.iloc[0:832,i]

        # preparing Kubelka-Munk function

        for i in range (0,144,3):
            ref_correction.absorbance.insert(i+2, 'K' + str(i/3), (1-ref_correction.absorbance.iloc[0:832,i+1])**2)

        
        for i in range (0,192,4):
            ref_correction.absorbance.insert(i+3, 'S' + str(i/4), 2*ref_correction.absorbance.iloc[0:832,i+1])


        for i in range (0,240,5):
            ref_correction.absorbance.insert(i+4, '(K/S)*hv' + str(i/5), (ref_correction.absorbance.iloc[0:832,i+2]/ref_correction.absorbance.iloc[0:832,i+3])*ref_correction.absorbance.iloc[0:832,i])




    # direct Tauc plot
    # define fitting range for bandgap
        for n in range (0,48):
            if MyUtils.plate[n] in MyUtils.chosen:

                ref_correction.max_index.pop(n)
                ref_correction.max_index.insert(n, ref_correction.absorbance.iloc[0:832,n*5+4].idxmax())
            else:
                ref_correction.max_index.pop(n)
                ref_correction.max_index.insert(n, 0.0)

            # print(ref_correction.max_index)

        
        parameters_direct = [None]*48
        #ref_correction.LinearFits_Eg = [None]*48

        for i in range(0,48):

            if MyUtils.plate[n] in MyUtils.chosen:

                peaks, properties = find_peaks(ref_correction.absorbance.iloc[:,i*5+4])# , prominence = [1, 2000])
                ref_correction.test[i] = peaks.tolist()
                ref_correction.points[i] = ref_correction.absorbance.iloc[ref_correction.test[i], i*5]


        # print(ref_correction.test)
        # print(ref_correction.points)

        mod = LinearModel()

        for k in range(0,48):
            if MyUtils.plate[k] in MyUtils.chosen:
                x_ref = ref_correction.absorbance.iloc[max(ref_correction.test[k])+15:max(ref_correction.test[k])+45,k*5]
                # print(x_ref)
                parameters_direct[k] =  mod.guess(ref_correction.absorbance.iloc[max(ref_correction.test[k])+15:max(ref_correction.test[k])+45,k*5+4]**2, x=x_ref)
                ref_correction.LinearFits_direct.pop(k) 
                ref_correction.LinearFits_direct.insert(k, mod.fit(ref_correction.absorbance.iloc[max(ref_correction.test[k])+15:max(ref_correction.test[k])+45,k*5+4]**2, parameters_direct[k], x=x_ref))  

                # print(ref_correction.LinearFits_Eg)          

        # for k in range(0,48):
        #     if MyUtils.plate[k] in MyUtils.chosen:
        #         x_ref = ref_correction.absorbance.iloc[ref_correction.max_index[k]+15:ref_correction.max_index[k]+45,k*5]
        #         parameters_direct[k] =  mod.guess(ref_correction.absorbance.iloc[ref_correction.max_index[k]+15:ref_correction.max_index[k]+45,k*5+4]**2, x=x_ref)
        #         ref_correction.LinearFits_direct.pop(k) 
        #         ref_correction.LinearFits_direct.insert(k, mod.fit(ref_correction.absorbance.iloc[ref_correction.max_index[k]+15:ref_correction.max_index[k]+45,k*5+4]**2, parameters_direct[k], x=x_ref)) 

        # equation y=m*x+t

        m_direct = [None]*48
        t_direct = [None]*48
        #Eg = [None]*48

        for n in range(0,48):
            if MyUtils.plate[n] in MyUtils.chosen:
                for name, param in ref_correction.LinearFits_direct[n].params.items():
                    if name == 'slope':
                        m_direct[n] = param.value
                    elif name == 'intercept':
                        t_direct[n] = param.value

        for n in range(0,48):
            if MyUtils.plate[n] in MyUtils.chosen:
                ref_correction.Eg_direct[n] = -(t_direct[n]/m_direct[n])
                if ref_correction.Eg_direct[n] < 0:
                    MyUtils.Eg_list_direct.append(0)

                else:
                    MyUtils.Eg_list_direct.append(ref_correction.Eg_direct[n])

            else:
                MyUtils.Eg_list_direct.append(0)    

        # print(ref_correction.Eg_direct)    

    

    # indirect Tauc plot
    # define fitting range for bandgap
        # for n in range (0,48):

        #     ref_correction.max_index.pop(n)
        #     ref_correction.max_index.insert(n, ref_correction.absorbance.iloc[0:832,n*5+4].idxmax())

            # print(ref_correction.max_index)


        parameters_indirect = [None]*48
        #ref_correction.LinearFits_Eg = [None]*48

        mod = LinearModel()

        # for k in range(0,48):
        #     if MyUtils.plate[k] in MyUtils.chosen:
        #         x_ref = ref_correction.absorbance.iloc[ref_correction.max_index[k]+15:ref_correction.max_index[k]+45,k*5]
        #         parameters_indirect[k] =  mod.guess(ref_correction.absorbance.iloc[ref_correction.max_index[k]+15:ref_correction.max_index[k]+45,k*5+4]**(1/2), x=x_ref)
        #         ref_correction.LinearFits_indirect.pop(k) 
        #         ref_correction.LinearFits_indirect.insert(k, mod.fit(ref_correction.absorbance.iloc[ref_correction.max_index[k]+15:ref_correction.max_index[k]+45,k*5+4]**(1/2), parameters_indirect[k], x=x_ref))  

        #         # print(ref_correction.LinearFits_Eg)     
                # 
        for k in range(0,48):
            if MyUtils.plate[k] in MyUtils.chosen:
                x_ref = ref_correction.absorbance.iloc[max(ref_correction.test[k])+15:max(ref_correction.test[k])+45,k*5]
                parameters_indirect[k] =  mod.guess(ref_correction.absorbance.iloc[max(ref_correction.test[k])+15:max(ref_correction.test[k])+45,k*5+4]**2, x=x_ref)
                ref_correction.LinearFits_indirect.pop(k) 
                ref_correction.LinearFits_indirect.insert(k, mod.fit(ref_correction.absorbance.iloc[max(ref_correction.test[k])+15:max(ref_correction.test[k])+45,k*5+4]**(1/2), parameters_indirect[k], x=x_ref))      
            
        # equation y=m*x+t

        m_indirect = [None]*48
        t_indirect = [None]*48
        #Eg = [None]*48

        for n in range(0,48):
            if MyUtils.plate[n] in MyUtils.chosen:
                for name, param in ref_correction.LinearFits_indirect[n].params.items():
                    if name == 'slope':
                        m_indirect[n] = param.value
                    elif name == 'intercept':
                        t_indirect[n] = param.value

        for n in range(0,48):
            if MyUtils.plate[n] in MyUtils.chosen:
                ref_correction.Eg_indirect[n] = -(t_indirect[n]/m_indirect[n])

                if ref_correction.Eg_indirect[n] < 0:
                    MyUtils.Eg_list_indirect.append(0)

                else:

                    MyUtils.Eg_list_indirect.append(ref_correction.Eg_indirect[n])

            else:
                MyUtils.Eg_list_indirect.append(0)    

        # print(ref_correction.Eg_indirect)    

            
            


