from reader import read_sl, read_bin
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


path = 'example_sl3_file.sl3'
sl3_bin_data = read_bin(path)
df = read_sl(path) #returns Pandas Dataframe
df_primary = df.query("survey_label == 'primary' & max_range < 60") #Subset Pandas Dataframe

#144 is the frame header size for the '.sl2' format. For '.sl3' it is 168
primary_list = [np.frombuffer(sl3_bin_data[(f+168):(f+(p-168))], dtype="uint8") for f, p in zip(df_primary["first_byte"], df_primary["frame_size"])]
primary_np = np.stack(primary_list)

plt.imshow(primary_np.transpose(), cmap="cividis")
plt.show()


#Write data to files
df.to_csv('output_dataframe.csv', sep=',', index=False)
np.savetxt('sonar_data.csv', primary_np, delimiter=',', fmt='%d')
