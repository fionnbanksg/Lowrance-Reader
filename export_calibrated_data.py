from PyQt5.QtWidgets import *
import processData
import numpy as np
import os
from scipy.interpolate import PPoly
import scipy.io as sio
import math


cal_file_path = 'calibration\CALIBRATION.md'
spline_file_path = 'calibration\splines\spline_data_20m.mat'

def export_ts(primary_np, parent=None):
    calibration_data = load_calibration_file(cal_file_path)
    spline = load_voltage_spline(spline_file_path)
    TS = calculate_target_strength(calibration_data, primary_np, spline)




    options = QFileDialog.Options()
    file_path, _ = QFileDialog.getSaveFileName(
        parent, "Export Sonar Data", "", "CSV Files (*.csv);;Text Files (*.txt)", options=options
    )
    if file_path:
        file_extension = os.path.splitext(file_path)[1]
        if file_extension == '.txt':
            np.savetxt(file_path, TS.transpose(), delimiter='\t', fmt='%f')
        elif file_extension == '.csv':
            np.savetxt(file_path, TS.transpose(), delimiter=',', fmt='%f')
        return file_path
    


def load_calibration_file(file_path):
    calibration_data = {}
    
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith("%%") or not line:  # Skip comments and empty lines
                continue
            if '<' in line and '>' in line:
                key, value = line.split('<')
                key = key.strip()
                value = value.split('>')[0].strip()
        
                try:
                    value = float(value.replace('e', 'E'))
                except ValueError:
                    pass 
                
                calibration_data[key] = value
    
    return calibration_data


def calculate_target_strength(calibration_data, sonar_data, spline):
    freq = calibration_data.get('freq')
    zer = calibration_data.get('zer')
    zet = calibration_data.get('zet')
    alpha = calibration_data.get('alpha')
    c = calibration_data.get('c')
    g = calibration_data.get('g')
    pt = calibration_data.get('pt')
    v_r = spline(sonar_data)
    lda = c/freq
    range = 8
    pr = ((1e-6 * v_r)/np.sqrt(2))**2 * ((zer + zet)/ zer)**2 * 1/zet
    pr_dbm = 10 * np.log10(pr * 1e3)
    pr_db_re_1w = pr_dbm - 30

    TS = pr_db_re_1w + 20 * np.log10(range) + 2 * alpha * range - 10 * np.log10((pt*lda**2)/(16*math.pi**2)) - g
    return TS



def load_voltage_spline(spline_filepath):
    data = sio.loadmat(spline_filepath)
    pp_inverse = data['pp_inverse']

    coefficients = pp_inverse['coefs'][0, 0] 
    breaks = pp_inverse['breaks'][0, 0][0]


    if coefficients.shape[0] != len(breaks) - 1:
        coefficients = coefficients.T

    assert coefficients.shape[0] == len(breaks) - 1, "Number of coefficients does not match number of segments."
    inverse_spline = PPoly(coefficients.T, breaks)
    return inverse_spline