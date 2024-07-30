"""
Script for UTAS Engineering Honours
Written by Fionn Banks-Gorton

Credits:
- Kenneth Thorø Martinsen for the tutorial on parsing Lowrance SL files
  Tutorial: https://www.datainwater.com/post/sonar_numpy/
- OpenSounder for SL file breakdown
  Documentation: https://github.com/opensounder/sounder-log-formats/blob/master/lowrance/sl-format.md
"""
import pandas
import numpy
import math
import extract_fields
import pandas
import numpy as np
import pandas as pd
#.sl3 file parameters
file_header_sl3 = 8
frame_header_sl3 = 168

#.sl2 file parameters
file_header_sl2 = 8
frame_header_sl2 = 144

def x2lon(x):
    return(x/6356752.3142*(180/math.pi))

def y2lat(y):
    return(((2*np.arctan(np.exp(y/6356752.3142)))-(math.pi/2))*(180/math.pi))

#from github - opensounder, structure taken from detainwater
sl3_dtype = np.dtype([
    ('frame_offset', 'uint32'),                
    ('unknown1', 'uint32'),                    
    ('blocksize', 'int16'),                    
    ('previous_blocksize', 'int16'),           
    ('channel_type', 'int16'),                 
    ('padding1', 'int16'),                    
    ('block_frame_index', 'uint32'),          
    ('upper_limit', 'float32'),                
    ('lower_limit', 'float32'),                
    ('unknown2', 'a12'),                       
    ('creation_data_time', 'uint32'),         
    ('packet_size', 'int16'),                  
    ('padding2', 'int16'),                    
    ('depth', 'float32'),                     
    ('frequency', 'uint8'),                   
    ('padding3', 'a31'),                       
    ('speed_gps_knots', 'float32'),            
    ('temperature_celsius', 'float32'),        
    ('encoded_longitude', 'int32'),           
    ('encoded_latitude', 'int32'),             
    ('speed_water_knots', 'float32'),         
    ('course_over_ground', 'float32'),        
    ('altitude_feet', 'float32'),             
    ('heading_radians', 'float32'),            
    ('flags', 'uint16'),                       
    ('padding4', 'a6'),                       
    ('time_from_creation_ms', 'uint32'),       
    ('last_primary_channel_offset', 'uint32'), 
    ('last_secondary_channel_offset', 'uint32'),
    ('last_downscan_channel_offset', 'uint32'),
    ('last_left_sidescan_offset', 'uint32'),  
    ('last_right_sidescan_offset', 'uint32'),  
    ('last_composite_sidescan_offset', 'uint32'), 
    ('unknown3', 'a12'),                       
    ('last_three_dc_channel_offset', 'uint32'),
    # ('sounded_data', '?')                    
])

survey_dict = {0: 'primary', 1: 'secondary', 2: 'downscan', 3: 'left_sidescan', 4: 'right_sidescan', 5: 'sidescan'}

def read_sl3(data):
    headers = []
    position = 0

    while (position <= len(data)):
        current_head = data[position:(position+frame_header_sl3)]
        frame_size = int.from_bytes(current_head[8:10], "little", signed = False)
        frame_size_alternative  = int.from_bytes(current_head[44:46], "little", signed = False) + frame_header_sl3
        extracted_head = extract_fields.extract_fields_s3(current_head)
        headers.append(extracted_head)
        position += frame_size if frame_size != 0 else frame_size_alternative

    #Parse extracted header
    frame_head_np = np.frombuffer(b''.join(headers), dtype=sl3_dtype)
    frame_head_df = pandas.DataFrame(frame_head_np)
    #Convert x-y coordinates to lat/long 
    frame_head_df["encoded_longitude"] = x2lon(frame_head_df["encoded_longitude"])
    frame_head_df["encoded_latitude"] = y2lat(frame_head_df["encoded_latitude"])
    #Convert to pandas dataframe
    frame_head_df = pd.DataFrame(frame_head_np)
    frame_head_df["channel_type"] = [survey_dict.get(i, "Other") for i in frame_head_df["channel_type"]]



    #Convert feet to meters
    frame_head_df[["depth"]] /= 3.2808399

    return(frame_head_df)



def read_sl2(data):
    #still to be implemented
    return 0

def read_sl(path):
    print("reading sl file")
    format = path.split(".")[-1]

    decode_functions = {
        'sl2': read_sl2,
        'sl3': read_sl3
    }

    if format in decode_functions:
        print(f"reading {format}")
        data = read_bin(path)
        df = decode_functions[format](data)
    else:
        print("Only '.sl2' or '.sl3' file formats supported")
        return -1
    return df

def read_bin(path):
    try:
        with open(path, "rb") as f:
            data = f.read()
        return data
    except FileNotFoundError:
        print(f"File not found: {path}")
        return None
    except IOError as e:
        print(f"Error reading file {path}: {e}")
        return None
    


def main():
    path = "gui/-10DB20,.sl3"
    result = read_sl(path)
    if result != -1:
        print("Successfully read and decoded the file.")
    else:
        print("Failed to read and decode the file.")

if __name__ == "__main__":
    main()