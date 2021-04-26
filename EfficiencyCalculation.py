import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob
import os
from scipy.interpolate import interp1d

''' Load SL1 experimental dataset '''

path = r'/Users/kmu/OneDrive - Oak Ridge National Laboratory/Spectrometer Efficiency Calibration/Lamp Measurement 1-14-2021'
filepaths = sorted(glob.glob(path + "/*.txt"))

filenames = pd.DataFrame()

for file in filepaths:
    filename = pd.DataFrame([os.path.basename(file)])
    filenames = pd.concat([filenames, filename], axis = 0, ignore_index = True)


def createList(r1, r2): 
    return list(range(r1, r2+1))       
r1, r2 = 0, 12
 
sl1_experimental = pd.DataFrame()

for file in filepaths:
    dfs1 = pd.read_csv(file, header = None, index_col = 0, delimiter = '\s+')
    sl1_experimental = pd.concat([sl1_experimental, dfs1], axis = 1, ignore_index = True)
        

''' Load SL1 ideal curve '''

sl1_ideal_path = r'/Users/kmu/OneDrive - Oak Ridge National Laboratory/Spectrometer Efficiency Calibration/sl1_ideal.txt'

sl1_ideal = pd.read_csv(sl1_ideal_path, header = None, index_col = 0, delimiter = '\t')

interpolation_function = interp1d(sl1_ideal.index, sl1_ideal[1], bounds_error = False, fill_value = 0)

sl1_ideal_aligned = pd.DataFrame(data = interpolation_function(sl1_experimental.index), index = sl1_experimental.index)


''' Calculate efficiency curve '''

normalized_sl1_ideal_aligned = sl1_ideal_aligned / sl1_ideal_aligned.max()
normalized_sl1_experimental = sl1_experimental / sl1_experimental.max()

efficiency_curve = 1 / (normalized_sl1_ideal_aligned.div(normalized_sl1_experimental.iloc[:,10:19].mean(axis = 1), axis = 0))

''' Load experimental data '''

experimental_data_folder = r'/Users/kmu/OneDrive - Oak Ridge National Laboratory/Spectrometer Efficiency Calibration/Pellets/Graphite with Eu2O3 16.72wt%'
experimental_data_paths = sorted(glob.glob(experimental_data_folder + "/*.txt"))

experimental_data = pd.DataFrame()
for file in experimental_data_paths:
    dfs2 = pd.read_csv(file, header = None, index_col = 0, delimiter = '\t')
    experimental_data = pd.concat([experimental_data, dfs2], axis = 1, ignore_index = True)

''' Calculate efficiency corrected spectrum '''

efficiency_corrected_experimental_data = pd.DataFrame()

for file in experimental_data_paths:
    dfs3 = pd.read_csv(file, header = None, index_col = 0, delimiter = '\t')
    dfs4 = dfs3.iloc[:,0] / efficiency_curve[0]
    efficiency_corrected_experimental_data = pd.concat([efficiency_corrected_experimental_data, dfs4], axis = 1, ignore_index = True)


