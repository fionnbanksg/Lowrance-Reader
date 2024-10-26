from PyQt5.QtWidgets import *
import processData
import numpy as np
import os

def export_other_data(dataframe, parent=None):
    if dataframe is not None:
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

def export_sonar_data(primary_np, primary_min_max, parent=None):
    if primary_np is not None:
        min_value = primary_min_max[0,0]
        max_value = primary_min_max[0, 1]
        depths = []
        depth_range = max_value - min_value
        max_rows = 3072
        for i in range(1, primary_np.shape[1]+1):
            depth = i / max_rows * depth_range
            depths.append(depth)

        depths = np.array(depths).reshape(-1, 1)
        primary_np_with_depths = np.hstack((depths, primary_np.transpose()))
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(
            parent, "Export Sonar Data", "", "CSV Files (*.csv);;Text Files (*.txt)", options=options
        )
        if file_path:
            file_extension = os.path.splitext(file_path)[1]
            if file_extension == '.txt':
                np.savetxt(file_path, primary_np_with_depths, delimiter='\t', fmt='%.2f')
            elif file_extension == '.csv':
                np.savetxt(file_path, primary_np_with_depths, delimiter=',', fmt='%.2f')
            return file_path

def process_data(primary_np, parent=None):
    if primary_np is not None:
        inputs = get_multiple_inputs_auto(parent)
        if inputs is not None:
            input1, input2, input3, input4, input5 = inputs

            options = QFileDialog.Options()
            file_path, _ = QFileDialog.getSaveFileName(
                parent, "Process Data", "", "CSV Files (*.csv);;Text Files (*.txt)", options=options
            )
            
            if file_path:
                try:
                    # Process the data with the integer values
                    data = processData.processData(primary_np, None, input1, input2, input3, input4, input5)
                    
                    file_extension = os.path.splitext(file_path)[1]
                    if file_extension == '.txt':
                        np.savetxt(file_path, data.transpose(), delimiter='\t', fmt='%f')
                    elif file_extension == '.csv':
                        np.savetxt(file_path, data.transpose(), delimiter=',', fmt='%f')
                    return file_path
                except Exception as e:
                    print(f"Error processing data: {e}")
                    return None


def process_data_with_column_selection(primary_np, parent=None):
    if primary_np is not None:
        inputs = get_multiple_inputs(parent)
        if inputs is not None:
            integer, input1, input2, input3, input4, input5 = inputs

            options = QFileDialog.Options()
            file_path, _ = QFileDialog.getSaveFileName(
                parent, "Process Data", "", "CSV Files (*.csv);;Text Files (*.txt)", options=options
            )
            
            if file_path:
                try:
                    # Process the data with the integer values
                    data = processData.processData(primary_np, integer, input1, input2, input3, input4, input5)
                    
                    file_extension = os.path.splitext(file_path)[1]
                    if file_extension == '.txt':
                        np.savetxt(file_path, data.transpose(), delimiter='\t', fmt='%f')
                    elif file_extension == '.csv':
                        np.savetxt(file_path, data.transpose(), delimiter=',', fmt='%f')
                    return file_path
                except Exception as e:
                    print(f"Error processing data: {e}")
                    return None

def get_multiple_inputs(parent=None):
    dialog = QDialog(parent)
    dialog.setWindowTitle("Input Parameters")

    layout = QVBoxLayout(dialog)
    form_layout = QFormLayout()

    integer_input = QLineEdit(dialog)
    integer_input.setText("0")
    form_layout.addRow("Input Begin Column", integer_input)

    input1 = QLineEdit(dialog)
    input1.setText("0")
    form_layout.addRow("Input increment (dB or Volts):", input1)

    input2 = QLineEdit(dialog)
    input2.setText("0")
    form_layout.addRow("Window padding:", input2)

    input3 = QLineEdit(dialog)
    input3.setText("0")
    form_layout.addRow("Width of specific value (columns)", input3)

    input4 = QLineEdit(dialog)
    input4.setText("0")
    form_layout.addRow("End of ring-down region", input4)

    input5 = QLineEdit(dialog)
    input5.setText("0")
    form_layout.addRow("Initial value (dB or volts)", input5)

    layout.addLayout(form_layout)

    button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, dialog)
    button_box.accepted.connect(dialog.accept)
    button_box.rejected.connect(dialog.reject)
    layout.addWidget(button_box)

    if dialog.exec_() == QDialog.Accepted:
        return (
            int(integer_input.text()),
            int(input1.text()),
            int(input2.text()),
            int(input3.text()),
            int(input4.text()),
            int(input5.text())
        )
    else:
        return None
    

def get_multiple_inputs_auto(parent=None):
    dialog = QDialog(parent)
    dialog.setWindowTitle("Input Parameters")

    layout = QVBoxLayout(dialog)
    form_layout = QFormLayout()


    input1 = QLineEdit(dialog)
    input1.setText("0")
    form_layout.addRow("Input increment (dBm or Volts):", input1)

    input2 = QLineEdit(dialog)
    input2.setText("0")
    form_layout.addRow("Window padding:", input2)

    input3 = QLineEdit(dialog)
    input3.setText("0")
    form_layout.addRow("Width of specific value (columns)", input3)

    input4 = QLineEdit(dialog)
    input4.setText("0")
    form_layout.addRow("End of ring-down region", input4)

    input5 = QLineEdit(dialog)
    input5.setText("0")
    form_layout.addRow("Initial value (dB or volts)", input5)

    layout.addLayout(form_layout)

    button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, dialog)
    button_box.accepted.connect(dialog.accept)
    button_box.rejected.connect(dialog.reject)
    layout.addWidget(button_box)

    if dialog.exec_() == QDialog.Accepted:
        return (
            int(input1.text()),
            int(input2.text()),
            int(input3.text()),
            int(input4.text()),
            int(input5.text())
        )
    else:
        return None