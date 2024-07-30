# Written by Fionn Banks-Gorton for Honours
#Processes sonar sounding data to analyse signal input power over time in a structured manner.

#Parameters:
#primary: A numpy array containing the sonar sounding data.

#Returns:
#numpy.ndarray: A 2D array where the first row contains decibel (dB) values and the second row contains average values for each processed window.

#Note: This function will be used to save a list of input power and db values. Manuel inspection will be required following this process to ensure it has performed properly.

# Required Libraries
import numpy as np

def processData(primary):
    initial_db = 0     # Initialise the starting dB value
    db_step = 3     # Decrement step for dB value in each window
    subwindow = 15     # Sub-window padding
    window_size = 74    # Full window size for sampling the data, tailored to typical data sample count within 5 seconds
    db = initial_db    # Initialise dB for use in loops
    ringing_pad = 150 # There is a ringing period in lowrance sonar data (where unintented transmitted signals return to the transducer)
    # Lists to store average values and corresponding dB values
    averages = []
    db_values = []
    
    # Transpose the matrix for easier column operations
    transpose = primary.transpose()
    column_averages = np.mean(transpose, axis=0)
    # Find the index where the column average increases abruptly (more than 1.75 times the previous)
    index_to_cut = 0
    for i in range(1, len(column_averages)):
        if column_averages[i] > 1.75 * column_averages[i - 1]:
            index_to_cut = i
            print(index_to_cut)  # Debugging output to ensure correct column was selected
            break

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
