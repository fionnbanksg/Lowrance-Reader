import numpy as np



def processData(primary_np):
    initial_db = 0
    db_step = 3


    # Define the window size
    window_size = 74
    db = initial_db
    # Initialize list to store averages and db values
    averages = []
    db_values = []
    transpose = primary_np.transpose()
    column_averages = np.mean(transpose, axis=0)
    subwindow = 15

    # Find the index where the average suddenly increases more than 4 times
    index_to_cut = 0
    for i in range(1, len(column_averages)):
        if column_averages[i] > 1.75 * column_averages[i - 1]:
            index_to_cut = i
            print(index_to_cut)
            break

    # Slice the transpose matrix to remove the beginning part
    if index_to_cut > 0:
        transpose = transpose[:, index_to_cut+1:]

    # Transpose back to original orientation
    processed_np = transpose

    for i in range(0, processed_np.shape[1], window_size):
        # Take a slice of the matrix containing the next window_size columns
        window = processed_np[150:2904, i+subwindow:i + window_size - subwindow]
        
        # Calculate the average of the numbers in the window
        avg = np.mean(window)
        
        # Save the average to the averages list
        averages.append(avg)
        
        # Save the current value of db to db_values
        db_values.append(db)
        
        # Update db
        db -= db_step

    # Convert the lists to numpy arrays
    averages_array = np.array(averages)
    db_values_array = np.array(db_values)

    # Transpose both arrays
    averages_array_transposed = averages_array[:, np.newaxis]  # Transpose averages_array
    db_values_array_transposed = db_values_array[:, np.newaxis]  # Transpose db_values_array

    # Concatenate the two transposed arrays along the columns
    return np.concatenate((db_values_array_transposed, averages_array_transposed), axis=1).transpose()
