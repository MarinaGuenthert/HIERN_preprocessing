import os


class path:
    
    completeName1 = 'test'
    completeName2 = 'test'
    completeName3 = 'test'
    completeName4 = 'test'
    completeName5 = 'test'
    completeName6 = 'test'
    completeName7 = 'test'
    completeName8 = 'test'
    completeName9 = 'test'

    completeNameD = 'test'
    completeNameEg = 'test'

    completeName10 = 'test'
    completeName11 = 'test'
    completeName12 = 'test'
    completeName13 = 'test'
    completeName14 = 'test'
    completeName15 = 'test'

    completeName20 = 'test'
    completeName21 = 'test'
    completeName22 = 'test'
    completeName23 = 'test'
    completeName24 = 'test'
    completeName25 = 'test'
    
    def PL_join_path(folder_selected):
        folderPath = folder_selected
        fitted_Graphs = "PL_overview_fit.png"
        norm_fitted_Graphs = "PL_overview_fit_norm.png"
        all_parameters = "PL_all_fit_results.txt"
        fitted_parameters = "PL_overview_fit_parameters.txt"
        D_print = "PL_extracted_fit_parameters.png"
        D_video = "3D_animation_extracted_fit_parameters.mp4"
        table = "PL_fit_parameters_stderr.csv"
        table_all = "PL_fit_parameters.csv"
        table_amplitude = "PL_fit_amplitude.csv"
        table_center = "PL_fit_center.csv"
        table_fwhm = "PL_fit_fwhm.csv"
        table_height = "PL_fit_height.csv"
        
        path.completeName1 = os.path.join(folderPath, fitted_Graphs)
        path.completeName2 = os.path.join(folderPath, norm_fitted_Graphs)
        path.completeName3 = os.path.join(folderPath, all_parameters)
        path.completeName4 = os.path.join(folderPath, fitted_parameters)
        path.completeName5 = os.path.join(folderPath, D_print)
        path.completeName7 = os.path.join(folderPath)
        path.completeNameD = os.path.join(folderPath, D_video)
        path.completeName10 = os.path.join(folderPath, table)
        path.completeName11 = os.path.join(folderPath, table_all)
        path.completeName21 = os.path.join(folderPath, table_amplitude)
        path.completeName22 = os.path.join(folderPath, table_center)
        path.completeName23 = os.path.join(folderPath, table_fwhm)
        path.completeName24 = os.path.join(folderPath, table_height)

        
    def PLE_join_path(folder_selected):
        folderPath = folder_selected
        fitted_Graphs = "PLE_overview_fit.png"
        norm_fitted_Graphs = "PLE_overview_fit_norm.png"
        all_parameters = "PLE_all_fit_results.txt"
        fitted_parameters = "PLE_overview_fit_parameters.txt"
        linear_fits = "PLE_overview_fit_for_bandgap.png"
        linear_fits_parameters = "PLE_overview_fit_paramaters_bandgap.txt"
        bandgap = "PLE_bandgaps.txt"
        all_linear_parameters = "PLE_all_linear_fit_results.txt"
        D_video = "3D_animation_extracted_fit_parameters.mp4"
        Eg_video = "3D_animation_bandgap.mp4"
        D_print = "PLE_extracted_fit_parameters.png"
        Eg_print = "PLE_extracted_bandgap.png"
        table_all = "PLE_all_parameters.csv"
        table = "PLE_all_parameters_stderr.csv"
        # table_norm = "PLE_all_parameters_table.csv"
        table_amplitude = "PLE_fit_amplitude.csv"
        table_center = "PLE_fit_center.csv"
        table_fwhm = "PLE_fit_fwhm.csv"
        table_height = "PLE_fit_height.csv"
        table_Eg = "PLE_fit_Eg.csv"

        path.completeName0 = os.path.join(folderPath)
        path.completeName1 = os.path.join(folderPath, fitted_Graphs)
        path.completeName2 = os.path.join(folderPath, norm_fitted_Graphs)
        path.completeName3 = os.path.join(folderPath, all_parameters)
        path.completeName4 = os.path.join(folderPath, fitted_parameters)
        path.completeName5 = os.path.join(folderPath, D_print)
        path.completeName6 = os.path.join(folderPath, linear_fits_parameters)
        path.completeName7 = os.path.join(folderPath, bandgap)
        path.completeName8 = os.path.join(folderPath, all_linear_parameters)
        path.completeName9 = os.path.join(folderPath, linear_fits)
        path.completeName10 = os.path.join(folderPath, Eg_print)
        path.completeNameD = os.path.join(folderPath, D_video)
        path.completeNameEg = os.path.join(folderPath, Eg_video)
        path.completeName11 = os.path.join(folderPath, table_all)
        path.completeName20 = os.path.join(folderPath, table)
        path.completeName21 = os.path.join(folderPath, table_amplitude)
        path.completeName22 = os.path.join(folderPath, table_center)
        path.completeName23 = os.path.join(folderPath, table_fwhm)
        path.completeName24 = os.path.join(folderPath, table_height)
        path.completeName25 = os.path.join(folderPath, table_Eg)

    def ref_join_path(folder_selected):

        folderPath = folder_selected
        fitted_Graphs = "reflectance_overview_fit.png"
        norm_fitted_Graphs = "reflectance_overview_fit.png"
        all_parameters = "reflectance_all_fit_results.txt"
        fitted_parameters = "reflectance_overview_fit_parameters.txt"
        Eg_video = "3D_animation_bandgaps.mp4"
        Tauc_direct = "reflectance_Tauc_direct.png"
        Tauc_indirect = "reflectance_Tauc_indirect.png"
        table = "reflectance_all_parameters.csv"
        Eg_print = "reflectance_extracted_bandgap.png"
        indirect_table = "reflectance_indirect_Eg.csv"
        direct_table = "reflectance_direct_Eg.csv"

        path.completeName0 = os.path.join(folderPath)
        path.completeName1 = os.path.join(folderPath, fitted_Graphs)
        path.completeName2 = os.path.join(folderPath, norm_fitted_Graphs)
        path.completeName3 = os.path.join(folderPath, all_parameters)
        path.completeName4 = os.path.join(folderPath, fitted_parameters)
        path.completeName5 = os.path.join(folderPath, Tauc_direct)
        path.completeName6 = os.path.join(folderPath, Tauc_indirect)
        path.completeNameEg = os.path.join(folderPath, Eg_video)
        path.completeName10 = os.path.join(folderPath, Eg_print)
        path.completeName20 = os.path.join(folderPath, table)
        path.completeName24 = os.path.join(folderPath, indirect_table)
        path.completeName25 = os.path.join(folderPath, direct_table)

    def Raman_join_path(folder_selected):
        folderPath = folder_selected
        fitted_Graphs = "Raman_overview_fit.png"
        norm_fitted_Graphs = "Raman_overview_peaks.png"
        all_parameters = "Raman_all_fit_results.txt"
        fitted_parameters = "Raman_overview_fit_parameters.txt"
        peak_positions = "Raman_peak_positions.txt"
        table = "Raman_parameters.csv"
        table_all = "Raman_fit_parameters.csv"
        table_amplitude = "Raman_fit_amplitude.csv"
        table_center = "Raman_fit_center.csv"
        table_fwhm = "Raman_fit_fwhm.csv"
        table_height = "Raman_fit_height.csv"

        path.completeName1 = os.path.join(folderPath, fitted_Graphs)
        path.completeName2 = os.path.join(folderPath, norm_fitted_Graphs)
        path.completeName3 = os.path.join(folderPath, all_parameters)
        path.completeName4 = os.path.join(folderPath, fitted_parameters)
        path.completeName5 = os.path.join(folderPath, peak_positions)
        path.completeName6 = os.path.join(folderPath, table)
        path.completeName7 = os.path.join(folderPath)
        path.completeName11 = os.path.join(folderPath, table_all)
        path.completeName21 = os.path.join(folderPath, table_amplitude)
        path.completeName22 = os.path.join(folderPath, table_center)
        path.completeName23 = os.path.join(folderPath, table_fwhm)
        path.completeName24 = os.path.join(folderPath, table_height)
        

    def trPL_join_path(folder_selected):
        folderPath = folder_selected

        fitted_Graphs1 = "trPL_overview_lifetimes1.png"
        norm_fitted_Graphs1 = "trPL_overview_norm_fit1.png"
        all_parameters1 = "trPL_all_fit_results1.txt"
        fitted_parameters1 = "trPL_overview_fit_parameters1.txt"
        table1 = "trPL_fit_parameters1.csv"
        table_t = "trPL_fit_t.csv"

        fitted_Graphs2 = "trPL_overview_lifetimes2.png"
        norm_fitted_Graphs2 = "trPL_overview_norm_fit2.png"
        all_parameters2 = "trPL_all_fit_results2.txt"
        fitted_parameters2 = "trPL_overview_fit_parameters2.txt"
        table2 = "trPL_fit_parameters2.csv"
        table_tau = "trPL_fit_tau.csv"
        table_b = "trPL_fit_b.csv"

        lifetimes1 = "3D_lifetime1.mp4"
        lifetimes2 = "3D_lifetimes2.mp4"

        path.completeName0 = os.path.join(folderPath)
        path.completeName10 = os.path.join(folderPath, fitted_Graphs1)
        path.completeName11 = os.path.join(folderPath, norm_fitted_Graphs1)
        path.completeName12 = os.path.join(folderPath, all_parameters1)
        path.completeName13 = os.path.join(folderPath, fitted_parameters1)
        path.completeName14 = os.path.join(folderPath, lifetimes1)
        path.completeName15 = os.path.join(folderPath, table1)
        path.completeName17 = os.path.join(folderPath, table_t)

        path.completeName20 = os.path.join(folderPath, fitted_Graphs2)
        path.completeName21 = os.path.join(folderPath, norm_fitted_Graphs2)
        path.completeName22 = os.path.join(folderPath, all_parameters2)
        path.completeName23 = os.path.join(folderPath, fitted_parameters2)
        path.completeName24 = os.path.join(folderPath, lifetimes2)
        path.completeName25 = os.path.join(folderPath, table2)
        path.completeName27 = os.path.join(folderPath, table_tau)
        path.completeName28 = os.path.join(folderPath, table_b)


