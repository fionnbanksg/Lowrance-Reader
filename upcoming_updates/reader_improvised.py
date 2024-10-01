"""
Script for UTAS Engineering Honours
Written by Fionn Banks-Gorton

Credits:
- Kenneth Thorø Martinsen for the tutorial on parsing Lowrance SL files
  Tutorial: https://www.datainwater.com/post/sonar_numpy/
- OpenSounder for SL file breakdown
  Documentation: https://github.com/opensounder/sounder-log-formats/blob/master/lowrance/sl-format.md
"""

import numpy as np
import math
import pandas as pd
import extract_fields
file_header_sl2 = 8
header_sl2 = 144

file_header_sl3 = 8
header_sl3 = 168

sl3_dtype = extract_fields.sl3_dtype
survey_dict = {0: 'primary', 1: 'secondary', 2: 'downscan', 3: 'left_sidescan', 4: 'right_sidescan', 5: 'sidescan'}

def x2lon(x):
    return(x/6356752.3142*(180/math.pi))

def y2lat(y):
    return(((2*np.arctan(np.exp(y/6356752.3142)))-(math.pi/2))*(180/math.pi))

def sl3_decode(data):
    position = file_header_sl3
    headers = []

    while (position <= len(data)):
        head = data[position:(position+header_sl3)]
        packet_size = int.from_bytes(head[44:44+2], "little", signed=False) 
  
        frame_size_alt = packet_size+header_sl3
       
        frame_size = frame_size = int.from_bytes(head[8:10], "little", signed = False)
        prev_size = int.from_bytes(head[10:10+2], "little", signed = False)
        
        head_sub = extract_fields.extract_fields_sl3(head)    
        headers.append(head_sub)
        if(frame_size ==0):
            position += frame_size_alt
            print(frame_size_alt)
            print(frame_size)
            print(prev_size)
        else:
            position+=frame_size
   
    print('finished death loop')
    frame_head_np = np.frombuffer(b''.join(headers), dtype=sl3_dtype)


    frame_head_df = pd.DataFrame(frame_head_np)
    
    frame_head_df["encoded_longitude"] = x2lon(frame_head_df["encoded_longitude"])
    frame_head_df["encoded_latitude"] = y2lat(frame_head_df["encoded_latitude"])

    #Get survey type label
    frame_head_df["survey_label"] = [survey_dict.get(i, "Other") for i in frame_head_df["channel_type"]]

    #Convert feet to meters
    frame_head_df[["depth", "upper_limit", "lower_limit"]] /= 3.2808399

    return(frame_head_df)

def sl2_decode():
    return 0

def read_bin(path):
    with open(path, "rb") as f:
        data = f.read()

    return(data)


def read_sl(path):
    print("reading sl file")
    format = path.split(".")[-1]

    if format == "sl2":
        print("reading sl2")
        data = read_bin(path)
        df = sl2_decode(data)

    elif format == "sl3":
        print("reading sl3")
        data = read_bin(path)
        df = sl3_decode(data)

    else:
        print("Only '.sl2' or '.sl3' file formats supported")
        return(-1)
    return(df)


df = read_sl("upcoming_updates/20MCAL3.sl3")
df_primary = df.query("survey_label == 'primary'")
print(df_primary)
df_primary.to_csv('data.csv')
