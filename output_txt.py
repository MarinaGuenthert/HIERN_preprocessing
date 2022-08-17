from myutils import MyUtils
import csv
import numpy
from reflectance_correction import ref_correction
from trPL_fit import trPL_evaluation

class save_files:
    
    def save_Gauss_PL(completeName3, completeName4, completeName11, completeName21, completeName22, completeName23, completeName24, completeName25, GaussFits_PL, chosen, completeName10):
       
        # save fit to output

        f = open(completeName3, "w")
        for it in range(0,48):
            if MyUtils.plate[it] in MyUtils.chosen:
                f.write('\n' + MyUtils.plate[it] + '\n')
                f.write(GaussFits_PL[it].fit_report(min_correl=0.25))
        f.close()

        # g = open(completeName4, "w")
        # for n in range(0,48):
        #     if MyUtils.plate[n] in MyUtils.chosen:
        #         g.write('\n' + MyUtils.plate[n] + '\n')
        #         g.write('Parameter    Value       Stderr' + '\n')
        #         for name, param in GaussFits_PL[n].params.items():
        #             g.write(f'{name:7s} {param.value:11.5f} {param.stderr:11.5f}' + '\n')
        # g.close()

        with open(completeName10, 'w', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=';',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow(['well', 'Parameter', 'Value', 'Stderr'])
            for n in range(0,48):
                if MyUtils.plate[n] in MyUtils.chosen:
                    for name, param in GaussFits_PL[n].params.items():
                        spamwriter.writerow([MyUtils.plate[n], name, param.value, param.stderr])

        with open(completeName11, 'w', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow(['well', 'amplitude', 'center', 'fwhm', 'height'])
            for n in range(0,48):
                spamwriter.writerow([MyUtils.plate[n], MyUtils.amplitude_list[n], MyUtils.center_list[n], MyUtils.fwhm_list[n], MyUtils.height_list[n]])

        letter = ['A', 'B', 'C', 'D', 'E', 'F']
            
        with open(completeName21, 'w', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow(['amplitude', '1', '2', '3', '4', '5', '6', '7', '8' ])
            for j in range(0,6):
                spamwriter.writerow([letter[j], MyUtils.amplitude_list[0+j*8], MyUtils.amplitude_list[1+j*8], MyUtils.amplitude_list[2+j*8], MyUtils.amplitude_list[3+j*8], MyUtils.amplitude_list[4+j*8], MyUtils.amplitude_list[5+j*8], MyUtils.amplitude_list[6+j*8], MyUtils.amplitude_list[7+j*8] ])
            
        with open(completeName22, 'w', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow(['center', '1', '2', '3', '4', '5', '6', '7', '8' ])
            for j in range(0,6):
                spamwriter.writerow([letter[j], MyUtils.center_list[0+j*8], MyUtils.center_list[1+j*8], MyUtils.center_list[2+j*8], MyUtils.center_list[3+j*8], MyUtils.center_list[4+j*8], MyUtils.center_list[5+j*8], MyUtils.center_list[6+j*8], MyUtils.center_list[7+j*8] ])
            
        with open(completeName23, 'w', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow(['fwhm', '1', '2', '3', '4', '5', '6', '7', '8' ])
            for j in range(0,6):
                spamwriter.writerow([letter[j], MyUtils.fwhm_list[0+j*8], MyUtils.fwhm_list[1+j*8], MyUtils.fwhm_list[2+j*8], MyUtils.fwhm_list[3+j*8], MyUtils.fwhm_list[4+j*8], MyUtils.fwhm_list[5+j*8], MyUtils.fwhm_list[6+j*8], MyUtils.fwhm_list[7+j*8] ])
            
        with open(completeName24, 'w', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow(['height', '1', '2', '3', '4', '5', '6', '7', '8' ])
            for j in range(0,6):
                spamwriter.writerow([letter[j], MyUtils.height_list[0+j*8], MyUtils.height_list[1+j*8], MyUtils.height_list[2+j*8], MyUtils.height_list[3+j*8], MyUtils.height_list[4+j*8], MyUtils.height_list[5+j*8], MyUtils.height_list[6+j*8], MyUtils.height_list[7+j*8] ])



    def save_PLE(chosen, completeName3, completeName4, completeName6, completeName7, completeName8, completeName11, completeName20, completeName21, completeName22, completeName23, completeName24, completeName25, GaussFits_PLE, LinearFits_Eg, Eg, max_index):

        f = open(completeName3, "w")
        for it in range(0,48):
            if MyUtils.plate[it] in MyUtils.chosen:
                f.write('\n' + MyUtils.plate[it] + '\n')
                f.write(GaussFits_PLE[it].fit_report(min_correl=0.25))
        f.close()

        # g = open(completeName4, "w")

        # for n in range(0,48):
        #     g.write('\n' + MyUtils.plate[n] + '\n')
        #     g.write('Parameter    Value       Stderr' + '\n')
        #     for name, param in GaussFits_PLE[n].params.items():
        #         g.write(f'{name:7s} {param.value:11.5f} {param.stderr:11.5f}' + '\n')
        # g.close()

        h = open(completeName8, "w")
        for it in range(0,48):
            if type(max_index[it]) == float:
                if MyUtils.plate[it] in MyUtils.chosen:
                    h.write('\n' + MyUtils.plate[it] + '\n')
                    h.write(LinearFits_Eg[it].fit_report(min_correl=0.01))
        h.close()

        # q = open(completeName6, "w")

        # for n in range(0,48):
        #     q.write('\n' + MyUtils.plate[n] + '\n')
        #     q.write('Parameter    Value       Stderr' + '\n')
        #     for name, param in LinearFits_Eg[n].params.items():
        #         q.write(f'{name:7s} {param.value:11.5f} {param.stderr:11.5f}' + '\n')
        # q.close()

        s = open(completeName7, "w")
        for it in range(0,48):
            if MyUtils.plate[it] in MyUtils.chosen:
                s.write('\n' + MyUtils.plate[it] + '\n')
                s.write(str(Eg[it]))
        s.close()

        with open(completeName11, 'w', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow(['well', 'amplitude', 'center', 'fwhm', 'height', 'Eg'])
            for n in range(0,48):
                spamwriter.writerow([MyUtils.plate[n], MyUtils.amplitude_list[n], MyUtils.center_list[n], MyUtils.fwhm_list[n], MyUtils.height_list[n], MyUtils.Eg_list[n]])


        with open(completeName20, 'w', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=';',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow(['well', 'Parameter', 'Value', 'Stderr'])
            for n in range(0,48):
                if MyUtils.plate[n] in MyUtils.chosen:
                    spamwriter.writerow(['Gauss Fits'])
                    for name, param in GaussFits_PLE[n].params.items():
                        spamwriter.writerow([MyUtils.plate[n], name, param.value, param.stderr])
                    spamwriter.writerow(['Linear Fits'])
                    if isinstance(max_index[n], numpy.integer):
                        if not LinearFits_Eg[n] == None:
                            for name, param in LinearFits_Eg[n].params.items():
                                spamwriter.writerow([MyUtils.plate[n], name, param.value, param.stderr])
                        else:
                            spamwriter.writerow([MyUtils.plate[n]])
                            spamwriter.writerow([MyUtils.plate[n]])
                    else:
                        spamwriter.writerow([MyUtils.plate[n]])
                        spamwriter.writerow([MyUtils.plate[n]])
                    spamwriter.writerow(['Bandgap'])
                    spamwriter.writerow([MyUtils.plate[n], 'Eg', str(Eg[n])])

        letter = ['A', 'B', 'C', 'D', 'E', 'F']
            
        with open(completeName21, 'w', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow(['amplitude', '1', '2', '3', '4', '5', '6', '7', '8' ])
            for j in range(0,6):
                spamwriter.writerow([letter[j], MyUtils.amplitude_list[0+j*8], MyUtils.amplitude_list[1+j*8], MyUtils.amplitude_list[2+j*8], MyUtils.amplitude_list[3+j*8], MyUtils.amplitude_list[4+j*8], MyUtils.amplitude_list[5+j*8], MyUtils.amplitude_list[6+j*8], MyUtils.amplitude_list[7+j*8] ])
            
        with open(completeName22, 'w', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow(['center', '1', '2', '3', '4', '5', '6', '7', '8' ])
            for j in range(0,6):
                spamwriter.writerow([letter[j], MyUtils.center_list[0+j*8], MyUtils.center_list[1+j*8], MyUtils.center_list[2+j*8], MyUtils.center_list[3+j*8], MyUtils.center_list[4+j*8], MyUtils.center_list[5+j*8], MyUtils.center_list[6+j*8], MyUtils.center_list[7+j*8] ])
            
        with open(completeName23, 'w', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow(['fwhm', '1', '2', '3', '4', '5', '6', '7', '8' ])
            for j in range(0,6):
                spamwriter.writerow([letter[j], MyUtils.fwhm_list[0+j*8], MyUtils.fwhm_list[1+j*8], MyUtils.fwhm_list[2+j*8], MyUtils.fwhm_list[3+j*8], MyUtils.fwhm_list[4+j*8], MyUtils.fwhm_list[5+j*8], MyUtils.fwhm_list[6+j*8], MyUtils.fwhm_list[7+j*8] ])
            
        with open(completeName24, 'w', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow(['height', '1', '2', '3', '4', '5', '6', '7', '8' ])
            for j in range(0,6):
                spamwriter.writerow([letter[j], MyUtils.height_list[0+j*8], MyUtils.height_list[1+j*8], MyUtils.height_list[2+j*8], MyUtils.height_list[3+j*8], MyUtils.height_list[4+j*8], MyUtils.height_list[5+j*8], MyUtils.height_list[6+j*8], MyUtils.height_list[7+j*8] ])
                    
        with open(completeName25, 'w', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow(['Eg', '1', '2', '3', '4', '5', '6', '7', '8' ])
            for j in range(0,6):
                spamwriter.writerow([letter[j], MyUtils.Eg_list[0+j*8], MyUtils.Eg_list[1+j*8], MyUtils.Eg_list[2+j*8], MyUtils.Eg_list[3+j*8], MyUtils.Eg_list[4+j*8], MyUtils.Eg_list[5+j*8], MyUtils.Eg_list[6+j*8], MyUtils.Eg_list[7+j*8] ])




    def save_ref(chosen, completeName11, completeName20, completeName24, completeName25, LinearFits_direct, LinearFits_indirect, Eg_direct, Eg_indirect):

        with open(completeName20, 'w', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=';',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow(['well', 'Parameter', 'Value', 'Stderr'])
            for n in range(0,48):
                if MyUtils.plate[n] in MyUtils.chosen:
                    spamwriter.writerow(['Linear Fits'])
                    for name, param in LinearFits_direct[n].params.items():
                        spamwriter.writerow([MyUtils.plate[n], name, param.value, param.stderr])
                    for name, param in LinearFits_indirect[n].params.items():
                        spamwriter.writerow([MyUtils.plate[n], name, param.value, param.stderr])
                    spamwriter.writerow(['Bandgap'])
                    spamwriter.writerow([MyUtils.plate[n], 'Eg_direct', str(Eg_direct[n])])
                    spamwriter.writerow([MyUtils.plate[n], 'Eg_indirect', str(Eg_indirect[n])])
                    spamwriter.writerow([str(ref_correction.test[n])])
                    spamwriter.writerow([str(ref_correction.points[n])])

        with open(completeName11, 'w', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow(['well', 'amplitude', 'center', 'fwhm', 'height'])
            for n in range(0,48):
                spamwriter.writerow([MyUtils.plate[n], MyUtils.Eg_list_direct[n], MyUtils.Eg_list_indirect[n]])

        letter = ['A', 'B', 'C', 'D', 'E', 'F']

        with open(completeName25, 'w', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow(['direct Eg', '1', '2', '3', '4', '5', '6', '7', '8' ])
            for j in range(0,6):
                spamwriter.writerow([letter[j], MyUtils.Eg_list_direct[0+j*8], MyUtils.Eg_list_direct[1+j*8], MyUtils.Eg_list_direct[2+j*8], MyUtils.Eg_list_direct[3+j*8], MyUtils.Eg_list_direct[4+j*8], MyUtils.Eg_list_direct[5+j*8], MyUtils.Eg_list_direct[6+j*8], MyUtils.Eg_list_direct[7+j*8] ])

        with open(completeName24, 'w', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow(['indirect Eg', '1', '2', '3', '4', '5', '6', '7', '8' ])
            for j in range(0,6):
                spamwriter.writerow([letter[j], MyUtils.Eg_list_indirect[0+j*8], MyUtils.Eg_list_indirect[1+j*8], MyUtils.Eg_list_indirect[2+j*8], MyUtils.Eg_list_indirect[3+j*8], MyUtils.Eg_list_indirect[4+j*8], MyUtils.Eg_list_indirect[5+j*8], MyUtils.Eg_list_indirect[6+j*8], MyUtils.Eg_list_indirect[7+j*8] ])


                    

    def save_Raman1(chosen, maxima_list, Reports_Raman, LorentzFits_Raman, problem, completeName5, completeName3, completeName6):
        # write peak positions to output file
        f = open(completeName5, "w")
        for it in range(0,48):
            if MyUtils.plate[it] in MyUtils.chosen:
                f.write('\n' + MyUtils.plate[it] + '\n')
                k = it*2
                for item in maxima_list[k]:
                    if item != 0:
                    #and item != 0:
                    #print(item)
                        f.write('\n' + str(item))
                f.write('\n' +  '-------------------------------------------------------------' )
        f.close()

        g = open(completeName3, "w")
        for it in range(0,48):
            if MyUtils.plate[it] in MyUtils.chosen:
            #if plate[it] in MyUtils.chosen:
                g.write('\n' + MyUtils.plate[it] + '\n')
                g.write(Reports_Raman[it*2])
        g.close()

        height = ['l1_height', 'l2_height', 'l3_height', 'l4_height', 'l5_height', 'l6_height', 'l7_height']

        with open(completeName6, 'w', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=';',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow(['well', 'Parameter', 'Value', 'Stderr', 'problem'])
            for n in range(0,48):
                if MyUtils.plate[n] in MyUtils.chosen:
                    if len(maxima_list[n*2]) <= 8 and len(maxima_list[n*2]) >=2:
                # spamwriter.writerow(['Lorentz Fits'])
                        for name, param in LorentzFits_Raman[n*2].params.items():
                	# problem = ' '
                    # if name in height:
                    #     problem = 'no'
                    #     percent = param.value/100*5
                    #     print(percent)
                    #     if type(param.stderr) == float:
                    #         if param.stderr >= percent:
                    #             problem = 'yes'
                    #         else:
                    #             problem = 'no'
                    #     else:
                    #         problem = 'yes'
                            spamwriter.writerow([MyUtils.plate[n], name, param.value, param.stderr, str(problem[n*2])])
                # spamwriter.writerow(['Linear Fits'])
                # if max_index[n] <= 400:
                #     for name, param in LinearFits_Eg[n].params.items():
                #         spamwriter.writerow([MyUtils.plate[n], name, param.value, param.stderr])
                # spamwriter.writerow(['Bandgap'])
                # spamwriter.writerow([MyUtils.plate[n], 'Eg', str(Eg[n])])

    def save_Raman2(chosen, maxima_list, Reports_Raman, LorentzFits_Raman, problem, completeName11, completeName21, completeName22, completeName23, completeName24):

        with open(completeName11, 'w', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow(['well', 'amplitude', 'center', 'fwhm', 'height'])
            for n in range(0,48):
                spamwriter.writerow([MyUtils.plate[n], MyUtils.amplitude_list[n], MyUtils.center_list[n], MyUtils.fwhm_list[n], MyUtils.height_list[n]])

        letter = ['A', 'B', 'C', 'D', 'E', 'F']
            
        with open(completeName21, 'w', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow(['amplitude', '1', '2', '3', '4', '5', '6', '7', '8' ])
            for j in range(0,6):
                spamwriter.writerow([letter[j], MyUtils.amplitude_list[0+j*8], MyUtils.amplitude_list[1+j*8], MyUtils.amplitude_list[2+j*8], MyUtils.amplitude_list[3+j*8], MyUtils.amplitude_list[4+j*8], MyUtils.amplitude_list[5+j*8], MyUtils.amplitude_list[6+j*8], MyUtils.amplitude_list[7+j*8] ])
            
        with open(completeName22, 'w', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow(['center', '1', '2', '3', '4', '5', '6', '7', '8' ])
            for j in range(0,6):
                spamwriter.writerow([letter[j], MyUtils.center_list[0+j*8], MyUtils.center_list[1+j*8], MyUtils.center_list[2+j*8], MyUtils.center_list[3+j*8], MyUtils.center_list[4+j*8], MyUtils.center_list[5+j*8], MyUtils.center_list[6+j*8], MyUtils.center_list[7+j*8] ])
            
        with open(completeName23, 'w', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow(['fwhm', '1', '2', '3', '4', '5', '6', '7', '8' ])
            for j in range(0,6):
                spamwriter.writerow([letter[j], MyUtils.fwhm_list[0+j*8], MyUtils.fwhm_list[1+j*8], MyUtils.fwhm_list[2+j*8], MyUtils.fwhm_list[3+j*8], MyUtils.fwhm_list[4+j*8], MyUtils.fwhm_list[5+j*8], MyUtils.fwhm_list[6+j*8], MyUtils.fwhm_list[7+j*8] ])
            
        with open(completeName24, 'w', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow(['height', '1', '2', '3', '4', '5', '6', '7', '8' ])
            for j in range(0,6):
                spamwriter.writerow([letter[j], MyUtils.height_list[0+j*8], MyUtils.height_list[1+j*8], MyUtils.height_list[2+j*8], MyUtils.height_list[3+j*8], MyUtils.height_list[4+j*8], MyUtils.height_list[5+j*8], MyUtils.height_list[6+j*8], MyUtils.height_list[7+j*8] ])

    def save_trPL(Name1, Name2, Name3, completeName17, completeName27, completeName28, Fits, chosen, methode):

        f = open(Name1, "w")
        for it in range(0,48):
            if MyUtils.plate[it] in MyUtils.chosen:
                f.write('\n' + MyUtils.plate[it] + '\n')
                f.write(Fits[it*2].fit_report(min_correl=0.25))
        f.close()

        # g = open(Name2, "w")
        # for n in range(0,48):
        #     if MyUtils.plate[n] in MyUtils.chosen:
        #         g.write('\n' + MyUtils.plate[n] + '\n')
        #         g.write('Parameter    Value       Stderr' + '\n')
        #         for name, param in Fits[n*2].params.items():
        #             g.write(f'{name:7s} {param.value:11.5f} {param.stderr:11.5f}' + '\n')
        # g.close()     
        # 
        with open(Name3, 'w', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=';',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow(['well', 'Parameter', 'Value', 'Stderr'])
            for n in range(0,48):
                if MyUtils.plate[n] in MyUtils.chosen:
                    spamwriter.writerow([MyUtils.plate[n], trPL_evaluation.wave[n]])
                    spamwriter.writerow([MyUtils.plate[n], 'I(t0)', trPL_evaluation.maximum[n]])
                    for name, param in Fits[n*2].params.items():
                        spamwriter.writerow([MyUtils.plate[n], name, param.value, param.stderr]) 
                if methode == 1:
                     spamwriter.writerow([MyUtils.plate[n], 't', trPL_evaluation.t[n]])
                # if methode == 2:
                #      spamwriter.writerow([MyUtils.plate[n], 'tau', trPL_evaluation.tau_list[n]])
                #      spamwriter.writerow([MyUtils.plate[n], 'b', trPL_evaluation.b_list[n]])

    
        letter = ['A', 'B', 'C', 'D', 'E', 'F']

        if methode == 1:

            with open(completeName17, 'w', newline='') as csvfile:
                spamwriter = csv.writer(csvfile, delimiter=',',
                                        quotechar='|', quoting=csv.QUOTE_MINIMAL)
                spamwriter.writerow(['averaged t', '1', '2', '3', '4', '5', '6', '7', '8' ])
                for j in range(0,6):
                    spamwriter.writerow([letter[j], trPL_evaluation.t[0+j*8], trPL_evaluation.t[1+j*8], trPL_evaluation.t[2+j*8], trPL_evaluation.t[3+j*8], trPL_evaluation.t[4+j*8], trPL_evaluation.t[5+j*8], trPL_evaluation.t[6+j*8], trPL_evaluation.t[7+j*8] ])

        if methode == 2:

            with open(completeName27, 'w', newline='') as csvfile:
                spamwriter = csv.writer(csvfile, delimiter=',',
                                        quotechar='|', quoting=csv.QUOTE_MINIMAL)
                spamwriter.writerow(['tau', '1', '2', '3', '4', '5', '6', '7', '8' ])
                for j in range(0,6):
                    spamwriter.writerow([letter[j], trPL_evaluation.tau_list[0+j*8], trPL_evaluation.tau_list[1+j*8], trPL_evaluation.tau_list[2+j*8], trPL_evaluation.tau_list[3+j*8], trPL_evaluation.tau_list[4+j*8], trPL_evaluation.tau_list[5+j*8], trPL_evaluation.tau_list[6+j*8], trPL_evaluation.tau_list[7+j*8] ])

            with open(completeName28, 'w', newline='') as csvfile:
                spamwriter = csv.writer(csvfile, delimiter=',',
                                        quotechar='|', quoting=csv.QUOTE_MINIMAL)
                spamwriter.writerow(['b', '1', '2', '3', '4', '5', '6', '7', '8' ])
                for j in range(0,6):
                    spamwriter.writerow([letter[j], trPL_evaluation.b_list[0+j*8], trPL_evaluation.b_list[1+j*8], trPL_evaluation.b_list[2+j*8], trPL_evaluation.b_list[3+j*8], trPL_evaluation.b_list[4+j*8], trPL_evaluation.b_list[5+j*8], trPL_evaluation.b_list[6+j*8], trPL_evaluation.b_list[7+j*8] ])
