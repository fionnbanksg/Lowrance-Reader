from PyQt5.QtWidgets import QFileDialog, QInputDialog
import processData
import numpy as np
import os

def export_other_data(dataframe, parent=None):
    options = QFileDialog.Options()
    file_path, _ = QFileDialog.getSaveFileName(
        parent, "Export Other Data", "", "CSV Files (*.csv);;Text Files (*.txt)", options=options
    )
    if file_path:
        file_extension = os.path.splitext(file_path)[1]
        if file_extension == '.txt':
            dataframe.to_csv(file_path, sep='\t', index=False)
        elif file_extension == '.csv':
            dataframe.to_csv(file_path, sep=',', index=False)
        return file_path

def export_sonar_data(primary_np, parent=None):
    options = QFileDialog.Options()
    file_path, _ = QFileDialog.getSaveFileName(
        parent, "Export Sonar Data", "", "CSV Files (*.csv);;Text Files (*.txt)", options=options
    )
    if file_path:
        file_extension = os.path.splitext(file_path)[1]
        if file_extension == '.txt':
            np.savetxt(file_path, primary_np.transpose(), delimiter='\t', fmt='%d')
        elif file_extension == '.csv':
            np.savetxt(file_path, primary_np.transpose(), delimiter=',', fmt='%d')
        return file_path

def process_data(primary_np, parent=None):
    options = QFileDialog.Options()
    file_path, _ = QFileDialog.getSaveFileName(
        parent, "Process Data", "", "CSV Files (*.csv);;Text Files (*.txt)", options=options
    )
    if file_path:
        data = processData.processData(primary_np, None)
        file_extension = os.path.splitext(file_path)[1]
        if file_extension == '.txt':
            np.savetxt(file_path, data.transpose(), delimiter='\t', fmt='%d')
        elif file_extension == '.csv':
            np.savetxt(file_path, data.transpose(), delimiter=',', fmt='%d')
        return file_path


def process_data_with_column_selection(primary_np, parent=None):
    # Prompt the user for an integer input
    integer, ok = QInputDialog.getInt(parent, "Input Column Number for beginning of power sweep", "Enter an integer:")
    
    if ok:
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(
            parent, "Process Data", "", "CSV Files (*.csv);;Text Files (*.txt)", options=options
        )
        
        if file_path:
            # Process the data with the integer value
            data = processData.processData(primary_np, integer)
            
            file_extension = os.path.splitext(file_path)[1]
            if file_extension == '.txt':
                np.savetxt(file_path, data.transpose(), delimiter='\t', fmt='%d')
            elif file_extension == '.csv':
                np.savetxt(file_path, data.transpose(), delimiter=',', fmt='%d')
            return file_path