import numpy as np

def processData(primary, input_integer, db_step, subwindow, window_size, ringing_pad, initial_db):
    db = initial_db   
    averages = []
    medians = []
    std_devs = []
    db_values = []

    transpose = primary.transpose()
    column_averages = np.mean(transpose, axis=0)
    
    index_to_cut = 0

    if input_integer is None:
        for i in range(1, len(column_averages)):
            if column_averages[i] > 1.75 * column_averages[i - 1]:
                index_to_cut = i
                print(index_to_cut)  
                break
    else:
        index_to_cut = input_integer
    if index_to_cut > 0:
        transpose = transpose[:, index_to_cut+1:]
    processed_np = transpose
    for i in range(0, processed_np.shape[1], window_size):
        window = processed_np[ringing_pad:2904, i+subwindow:i + window_size - subwindow]
        
        avg = np.mean(window)
        median = np.median(window)
        std_dev = np.std(window)
        averages.append(avg)
        medians.append(median)
        std_devs.append(std_dev)
        db_values.append(db)
        db += db_step
    averages_array = np.array(averages)
    medians_array = np.array(medians)
    std_devs_array = np.array(std_devs)
    db_values_array = np.array(db_values)
    averages_array_transposed = averages_array[:, np.newaxis]
    medians_array_transposed = medians_array[:, np.newaxis]
    std_devs_array_transposed = std_devs_array[:, np.newaxis]
    db_values_array_transposed = db_values_array[:, np.newaxis]
    result = np.concatenate((db_values_array_transposed, averages_array_transposed, 
                             medians_array_transposed, std_devs_array_transposed), axis=1).transpose()
                             
    return result
