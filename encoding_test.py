import chardet


with open(r'C:\Users\mguen\Documents\Studium\Master_of_Science\HI-ERN\Researchmodule\measurements\luminescence\time-resolved\Data\A1.dat', 'rb') as rawdata:
    result = chardet.detect(rawdata.read(100000))
print(result)