from sonarlight import Sonar

sl3 = 'TEST1DEFAULT.sl3'

#Output:
'''
Summary of SL2 file:

- Primary channel with 3182 frames
- Secondary channel with 3182 frames
- Downscan channel with 3182 frames
- Sidescan channel with 3181 frames

Start time: 2023-09-13 08:20:36.840000
End time: 2023-09-13 08:22:52.770999808

File info: version 2, device 2, blocksize 3200, frame version 8
'''

#View raw data store in Pandas dataframe
sl3.df

#Each row contains metadata and pixel for each recorded frame.
#Pixels are stored in the "frames" column.
#The dataframe can be saved for further processing, 
#for example the Parquet file format that supports nested data structues.
sl3.df.to_parquet('sl3.parquet')

#Or to '.csv' file
sl3.df.to_csv("sl3.csv")

#Or to '.csv' file after dropping the "frames" column containing nested arrays
df_csv = sl3.df.copy().drop(["frames"], axis=1)
df_csv.to_csv("sl3.csv")