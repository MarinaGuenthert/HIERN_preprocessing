import pandas as pd
import numpy as np

from myutils import MyUtils
import threading
from threading import Thread

from lmfit.models import ExponentialModel
from lmfit.model import load_model

class trPL_evaluation(Thread):

    x_trPL = [None]*96
    curves = pd.DataFrame(data=None)
    Fits1 = [None]*96    
    Reports1 = [None]*96
    Fits2 = [None]*96    
    Reports2 = [None]*96

    exp1_amplitude = []
    exp2_amplitude = []
    exp3_amplitude = []
    exp1_decay = []
    exp2_decay = []
    exp3_decay = []
    t = [0] * 48

    wave = [None]*48
    maximum = [0]*48

    b_list = []
    tau_list = []

    def start(chosen, all_filenames):

        trPL_evaluation.x_trPL = [None]*96
        trPL_evaluation.curves = pd.DataFrame(data=None)
        trPL_evaluation.Fits1 = [None]*96    
        trPL_evaluation.Reports1 = [None]*96
        trPL_evaluation.Fits2 = [None]*96    
        trPL_evaluation.Reports2 = [None]*96

        trPL_evaluation.exp1_amplitude = []
        trPL_evaluation.exp2_amplitude = []
        trPL_evaluation.exp3_amplitude = []
        trPL_evaluation.exp1_decay = []
        trPL_evaluation.exp2_decay = []
        trPL_evaluation.exp3_decay = []
        trPL_evaluation.t = [0] * 48

        trPL_evaluation.wave = [None]*48
        trPL_evaluation.maximum = [0]*48

        trPL_evaluation.b_list = []
        trPL_evaluation.tau_list = []

        # print(MyUtils.chosen)
        # print(all_filenames)

        j=0

        for i in range(0,48):
            if MyUtils.plate[i] in MyUtils.chosen:

                f = open(all_filenames[j], 'r')
                # rubbish = f.readline()
                trPL_evaluation.wave.pop(i)
                trPL_evaluation.wave.insert(i, f.readline(28).strip())
                f.close()
                j = j + 1
                
        trPL_list = []

        main_dataframe = pd.DataFrame(pd.read_csv(all_filenames[0], engine = 'python', sep = '\t', header = None, on_bad_lines='skip', skiprows=87, quoting = 3, encoding='ISO-8859-1', skip_blank_lines = True))
        
        for i in range(1,len(all_filenames)):
            data = pd.read_csv(all_filenames[i], engine = 'python', sep = '\t', header = None, on_bad_lines='skip', skiprows=87, quoting = 3, encoding='ISO-8859-1', skip_blank_lines = True)
            df = pd.DataFrame(data)
            main_dataframe = pd.concat([main_dataframe,df],axis=1)

        trPL_data = main_dataframe

        # sn.heatmap(trPL_evaluation.curves.isna())
        trPL_data.dropna(inplace = True)


        # add up to 96 columns

        if len(trPL_data.columns) <= 96:
            for i in range (48):
                if MyUtils.plate[i] not in MyUtils.chosen:
                    k = i*2
                    trPL_data.insert(k, str(MyUtils.plate[i]) +'x', None)
                    trPL_data.insert(k+1, str(MyUtils.plate[i]) +'y', None)

        

        trPL_evaluation.curves = pd.concat([trPL_evaluation.curves, trPL_data.iloc[:,]], axis=1)

        # print(trPL_evaluation.curves)

        maxima_list = []
        column = [None]*48

        for i in range(0,48):
            if MyUtils.plate[i] in MyUtils.chosen:
                #print(i)
                column[i] = trPL_evaluation.curves.iloc[:,i*2+1]
                trPL_evaluation.maximum[i] = column[i].max()
                maxima_list.append(column[i].idxmax())

        #print(maxima_list)
        # print(trPL_evaluation.wave[0])
        # print(trPL_evaluation.maximum)

        trPL_evaluation.curves.drop(trPL_evaluation.curves.index[0:max(maxima_list)], inplace=True)
        trPL_evaluation.curves.reset_index(drop=True, inplace=True)

        # print(trPL_evaluation.curves)

        # normalization

        for i in range(0,48):
            trPL_evaluation.curves.iloc[:,i*2+1] = trPL_evaluation.curves.iloc[:,i*2+1]/trPL_evaluation.curves.iloc[1,i*2+1]

        print(trPL_evaluation.curves)

        # trPL_evaluation.curves = trPL_evaluation.curves.astype (np.float128, copy=False)






    def averaged_exponential(chosen, all_filenames, folder_selected):

        trPL_evaluation.start(MyUtils.chosen,all_filenames)
        
        for i in range(0,48):

            if MyUtils.plate[i] in MyUtils.chosen:
            
                trPL_evaluation.x_trPL.pop(i*2)
                trPL_evaluation.x_trPL.insert(i*2, trPL_evaluation.curves.iloc[:,i*2])
                
                exp1 = ExponentialModel(prefix='exp1_')
                pars = exp1.guess(trPL_evaluation.x_trPL[i*2], trPL_evaluation.curves.iloc[:,i*2+1])
                
                exp2 = ExponentialModel(prefix='exp2_')
                pars.update(exp2.make_params())

                exp3 = ExponentialModel(prefix='exp3_')
                pars.update(exp3.make_params())

                pars['exp1_amplitude'].set(value=0.5, min=0, max=1)
                pars['exp2_amplitude'].set(value=0.5, min=0, max=1)
                pars['exp3_amplitude'].set(value=0.5, min=0, max=1)

                pars['exp1_decay'].set(value=1000, min=100, max=10000)
                pars['exp2_decay'].set(value=1000, min=100, max=10000)
                pars['exp3_decay'].set(value=1000, min=100, max=10000)

                    
                mod = exp1 + exp2 + exp3 
                    
                trPL_evaluation.Fits1.pop(i*2)
                trPL_evaluation.Fits1.insert(i*2, mod.fit(trPL_evaluation.curves.iloc[:,i*2+1], pars, x=trPL_evaluation.x_trPL[i*2]))
                trPL_evaluation.Reports1.pop(i*2)
                trPL_evaluation.Reports1.insert(i*2, trPL_evaluation.Fits1[i*2].fit_report(min_correl=0.01))
                # print(i)
            # print('None')

        for k in range (0,48):
            if MyUtils.plate[k] in MyUtils.chosen:
                for key in trPL_evaluation.Fits1[k*2].params:
                    #print(MyUtils.plate[k])
                    if key == 'exp1_amplitude':
                        trPL_evaluation.exp1_amplitude.append(trPL_evaluation.Fits1[k*2].params[key].value)
                    if key == 'exp2_amplitude':
                        trPL_evaluation.exp2_amplitude.append(trPL_evaluation.Fits1[k*2].params[key].value)
                    if key == 'exp3_amplitude':
                        trPL_evaluation.exp3_amplitude.append(trPL_evaluation.Fits1[k*2].params[key].value)
                    if key == 'exp1_decay':
                        trPL_evaluation.exp1_decay.append(trPL_evaluation.Fits1[k*2].params[key].value)
                    if key == 'exp2_decay':
                        trPL_evaluation.exp2_decay.append(trPL_evaluation.Fits1[k*2].params[key].value)
                    if key == 'exp3_decay':
                        trPL_evaluation.exp3_decay.append(trPL_evaluation.Fits1[k*2].params[key].value)
                
            else:
                trPL_evaluation.exp1_amplitude.append(0)
                trPL_evaluation.exp2_amplitude.append(0)
                trPL_evaluation.exp3_amplitude.append(0)
                trPL_evaluation.exp1_decay.append(0)
                trPL_evaluation.exp2_decay.append(0)
                trPL_evaluation.exp3_decay.append(0)

        # print(trPL_evaluation.Fits1)
        # print(trPL_evaluation.Reports1)

        z = [0] * 48
        n = [0] * 48

        for i in range(0,48):
            if MyUtils.plate[i] in MyUtils.chosen:
                z[i] = trPL_evaluation.exp1_amplitude[i] * (trPL_evaluation.exp1_decay[i]**2) + trPL_evaluation.exp2_amplitude[i] * (trPL_evaluation.exp2_decay[i]**2) + trPL_evaluation.exp3_amplitude[i] * (trPL_evaluation.exp3_decay[i]**2)
                n[i] = trPL_evaluation.exp1_amplitude[i] * trPL_evaluation.exp1_decay[i] + trPL_evaluation.exp2_amplitude[i] * trPL_evaluation.exp2_decay[i] + trPL_evaluation.exp3_amplitude[i] * trPL_evaluation.exp3_decay[i]

                trPL_evaluation.t[i] = z[i]/n[i]

        # print(trPL_evaluation.t)

        print('done')
        




    def stretched_exponential(chosen, all_filenames, folder_selected):

        trPL_evaluation.start(MyUtils.chosen,all_filenames)



        for i in range(0,48):

            if MyUtils.plate[i] in MyUtils.chosen:

                trPL_evaluation.x_trPL.pop(i*2)
                trPL_evaluation.x_trPL.insert(i*2, trPL_evaluation.curves.iloc[:,i*2])

                # print(trPL_evaluation.x_trPL)

                def mystretchedexponential(x, tau, b):
                    return np.exp((-1.0)*(x/tau)**(1.0/b))


                mod = load_model('stretched.sav', funcdefs={'mystretchedexponential': mystretchedexponential})
                pars = mod.make_params(tau = 500, b = 0.5)

                pars['tau'].set(value = 500, min = 50)
                pars['b'].set(value = 0.5, min = 0, max = 1)


                # mod = stretched

                trPL_evaluation.Fits2.pop(i*2)
                trPL_evaluation.Fits2.insert(i*2, mod.fit(trPL_evaluation.curves.iloc[:,i*2+1], pars, x=trPL_evaluation.x_trPL[i*2]))
                trPL_evaluation.Reports2.pop(i*2)
                trPL_evaluation.Reports2.insert(i*2, trPL_evaluation.Fits2[i*2].fit_report(min_correl=0.01))
                # print(i)

        for k in range(0,48):
            if MyUtils.plate[k] in MyUtils.chosen:
                for key in trPL_evaluation.Fits2[k*2].params:
                    #print(MyUtils.plate[k])
                    if key == 'tau':
                        trPL_evaluation.tau_list.append(trPL_evaluation.Fits2[k*2].params[key].value)
                    if key == 'b':
                        trPL_evaluation.b_list.append(trPL_evaluation.Fits2[k*2].params[key].value)
            else:
                trPL_evaluation.tau_list.append(0)
                trPL_evaluation.b_list.append(0)

        print('done')


