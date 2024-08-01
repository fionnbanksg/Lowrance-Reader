import numpy as np
import scipy.stats as stats
from sklearn.metrics import r2_score

def processData(primary, input_integer, db_step, subwindow, window_size, ringing_pad, initial_db):
    db = initial_db    # Initialise dB for use in loops
    
    # Lists to store statistical values and corresponding dB values
    averages = []
    db_values = []
   # Transpose the matrix for easier column operations
    transpose = primary.transpose()
    column_averages = np.mean(transpose, axis=0)
    # Find the index where the column average increases abruptly (more than 1.75 times the previous)
    index_to_cut = 0
    if input_integer == None:
        for i in range(1, len(column_averages)):
            if column_averages[i] > 1.75 * column_averages[i - 1]:
                index_to_cut = i
                print(index_to_cut)  # Debugging output to ensure correct column was selected
                break
    else:
        index_to_cut = input_integer

    # Slice the transpose matrix to remove initial setup
    if index_to_cut > 0:
        transpose = transpose[:, index_to_cut+1:]

    # Use only the modified part of the matrix for further processing
    processed_np = transpose

    # Process the data in chunks of defined window size
    for i in range(0, processed_np.shape[1], window_size):
        window = processed_np[ringing_pad:2904, i+subwindow:i + window_size - subwindow]
        avg = np.mean(window)
        averages.append(avg)
        db_values.append(db)
        db -= db_step

    averages_array = np.array(averages)
    db_values_array = np.array(db_values)

    averages_array_transposed = averages_array[:, np.newaxis]  
    db_values_array_transposed = db_values_array[:, np.newaxis]

    return np.concatenate((db_values_array_transposed, averages_array_transposed), axis=1).transpose()