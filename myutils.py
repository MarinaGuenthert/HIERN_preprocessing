import os


class MyUtils:
    @staticmethod
    def get_absolute_path(relative_path):
        script_dir = os.path.abspath('')
        return os.path.join(script_dir, relative_path)
    
    plate = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8']
    
    center_list = []
    amplitude_list = []
    height_list = []
    fwhm_list = []
    Eg_list = []

    Eg_list_direct = []
    Eg_list_indirect = []

    chosen = []
    chosenA = ['_'] * 8
    chosenB = ['_'] * 8
    chosenC = ['_'] * 8
    chosenD = ['_'] * 8
    chosenE = ['_'] * 8
    chosenF = ['_'] * 8

    # def update_chosen_lists():

    #     for i in range(0,8):
    #         j = 0
    #         if MyUtils.plate[i] in MyUtils.chosen:
    #             MyUtils.chosenA[i-j*8] = MyUtils.plate[i]
        
    #     for i in range(0,8):
    #         j = 1
    #         if MyUtils.plate[i] in MyUtils.chosen:
    #             MyUtils.chosenB[i-j*8] = MyUtils.plate[i]

    #     for i in range(0,8):
    #         j = 2
    #         if MyUtils.plate[i] in MyUtils.chosen:
    #             MyUtils.chosenC[i-j*8] = MyUtils.plate[i]

    #     for i in range(0,8):
    #         j = 3
    #         if MyUtils.plate[i] in MyUtils.chosen:
    #             MyUtils.chosenD[i-j*8] = MyUtils.plate[i]

    #     for i in range(0,8):
    #         j = 4
    #         if MyUtils.plate[i] in MyUtils.chosen:
    #             MyUtils.chosenE[i-j*8] = MyUtils.plate[i]

    #     for i in range(0,8):
    #         j = 5
    #         if MyUtils.plate[i] in MyUtils.chosen:
    #             MyUtils.chosenF[i-j*8] = MyUtils.plate[i]



