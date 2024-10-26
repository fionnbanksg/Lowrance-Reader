from PyQt5.QtWidgets import *
import processData
import numpy as np
import os
from scipy.interpolate import PPoly
import scipy.io as sio
import math


cal_file_path = 'calibration/CALIBRATION.md'
spline_file_path = 'calibration/splines/spline_data_20m.mat'

def export_ts(primary_np, primary_min_max, parent=None):
    if primary_np is not None:
        calibration_data = load_calibration_file(cal_file_path)
        print(primary_min_max.transpose())
        TS = calculate_target_strength(calibration_data, primary_min_max, primary_np)
        min_value = primary_min_max[0,0]
        max_value = primary_min_max[0, 1]
        depths = []
        depth_range = max_value - min_value
        max_rows = 3072
        for i in range(1, primary_np.shape[1]+1):
            depth = i / max_rows * depth_range
            depths.append(depth)

        depths = np.array(depths).reshape(-1, 1)
        TS_with_depths = np.hstack((depths, TS.transpose()))
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(
            parent, "Export Sonar Data", "", "CSV Files (*.csv);;Text Files (*.txt)", options=options
        )
        if file_path:
            file_extension = os.path.splitext(file_path)[1]
            if file_extension == '.txt':
                np.savetxt(file_path, TS_with_depths, delimiter='\t', fmt='%.3f')
            elif file_extension == '.csv':
                np.savetxt(file_path, TS_with_depths, delimiter=',', fmt='%.3f')
            return file_path
    

def process_ts(row, column, primary_np, primary_min_max, parent=None):
    calibration_data = load_calibration_file(cal_file_path)
    spline = load_voltage_spline(spline_file_path)
    TS = calculate_target_strength(calibration_data, primary_min_max, primary_np, spline)

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
            if line.startswith("%%") or not line:  
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



def calculate_target_strength(calibration_data, primary_min_max, sonar_data):
    freq = calibration_data.get('freq')
    zer = calibration_data.get('zer')
    zet = calibration_data.get('zet')
    alpha = calibration_data.get('alpha')
    c = calibration_data.get('c')
    g = calibration_data.get('g')
    pt = calibration_data.get('pt')
    spline_path = calibration_data.get('spline')
    spline = load_voltage_spline(spline_path)
    v_r = spline(sonar_data)
    sonar_data = np.array(sonar_data)

    rows = [] 
    ranges = []  

    for i in range(sonar_data.shape[0]):  
        row_depths = []  
        max_range = primary_min_max[i, 0]
        min_range = primary_min_max[i, 1]
        recorded_range = max_range - min_range
        max_rows = 3072
        for j in range(sonar_data.shape[1]):  
            depth_at_row = j / max_rows * recorded_range + min_range
            row_depths.append(depth_at_row)  
        rows.append(row_depths) 

    ranges = np.array(rows)



    lda = c/freq
    pr = ((1e-6 * v_r)/np.sqrt(2))**2 * ((zer + zet)/ zer)**2 * 1/zet
    pr_dbm = 10 * np.log10(pr * 1e3)
    pr_db_re_1w = pr_dbm - 30

    TS = pr_db_re_1w + 20 * np.log10(ranges) + 2 * alpha * ranges - 10 * np.log10((pt*lda**2)/(16*math.pi**2)) - g
    return TS

def calculate_target_strength_singular(row, col, calibration_data, primary_min_max, sonar_data, spline):
    freq = calibration_data.get('freq')
    zer = calibration_data.get('zer')
    zet = calibration_data.get('zet')
    alpha = calibration_data.get('alpha')
    c = calibration_data.get('c')
    g = calibration_data.get('g')
    pt = calibration_data.get('pt')
    sonar_data = np.array(sonar_data)
    
    range_max = primary_min_max[col, 1]
    range_min = primary_min_max[col, 0]
    total_range = range_max - range_min
    depth = row/3072 * total_range
    val = sonar_data[col, row]
    voltage = spline(val)
    lda = c/freq
    voltage = 5e-3*3
    voltage = 0.177098 *math.exp(0.0645578 *val)*1e-6*3.33
    voltage = 0.154476 *math.exp(0.0654347 * val)*1e-6*3.33 #40m
    pr = (( voltage)/np.sqrt(2))**2 * ((zer + zet)/ zer)**2 * 1/zet

    TS = 10*math.log10(pr)  + 2 * alpha * depth - 10 * math.log10((pt*lda**2*g**2)/(16*math.pi**2)) #omitted 40log(r) term due to lowrance already including tvg
    return TS




def load_voltage_spline(spline_filepath):
    data = sio.loadmat(spline_filepath)
    pp_inverse = data['pp_inverse']
    coefficients = pp_inverse['coefs'][0, 0] 
    breaks = pp_inverse['breaks'][0, 0][0]
    if coefficients.shape[0] != len(breaks) - 1:
        coefficients = coefficients.T

    assert coefficients.shape[0] == len(breaks) - 1, "Error: number of coefficients not equal to number of segments."
    inverse_spline = PPoly(coefficients.T, breaks)
    return inverse_spline
