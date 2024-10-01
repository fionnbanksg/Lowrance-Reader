import numpy as np
#based off data provided in https://github.com/opensounder/sounder-log-formats/blob/master/lowrance/format-2.md

sl2_dtype = np.dtype([
    ('frame_offset', 'uint32'),                               
    ('last_primary_channel_offset', 'uint32'),  
    ('last_secondary_channel_offset', 'uint32'),  
    ('last_downscan_channel_offset', 'uint32'),
    ('last_left_sidescan_offset', 'uint32'),  
    ('last_right_sidescan_offset', 'uint32'),  
    ('last_composite_sidescan_offset', 'uint32'),                    
    ('blocksize', 'int16'),                                   
    ('lastBlockSize', 'int16'),   
    ('channel_type', 'int16'),  
    ('packet_size', 'int16'),                                   
    ('frameIndex', 'uint32'),   
    ('upper_limit', 'float32'),                                
    ('lower_limit','float32'),                                                             
    ('frequency', 'uint8'),                                                               
    ('depth', 'float32'),                                
    ('keelDepth', 'float32'),                                  
    ('speed_gps_knots', 'float32'),                             
    ('temperature_celsius', 'float32'),                      
    ('encoded_longitude', 'int32'),                          
    ('encoded_latitude', 'int32'),                          
    ('speed_water_knots', 'float32'),                        
    ('course_over_ground', 'float32'),                       
    ('altitude_feet', 'float32'),                             
    ('heading_radians', 'float32'),                          
    ('flags', 'uint16'),                                                                       
    ('time1', 'uint32'),                                      
])

def extract_fields_sl2(current_head):
    frame_offset = current_head[0:4]
    last_primary_channel_offset = current_head[4:8]
    last_secondary_channel_offset = current_head[8:12]
    last_downscan_channel_offset = current_head[12:16]
    last_left_sidescan_offset = current_head[16:20]
    last_right_sidescan_offset = current_head[20:24]
    last_composite_sidescan_offset = current_head[24:28]
    blockSize = current_head[28:30]
    lastBlockSize = current_head[30:32]
    channel_type = current_head[32:34]
    packet_size = current_head[34:36]
    frameIndex = current_head[36:40]
    upper_limit = current_head[40:44]
    lower_limit = current_head[44:48]
    frequency = current_head[50:51]
    depth = current_head[64:68]
    keelDepth = current_head[68:72]
    speed_gps_knots = current_head[100:104]
    temperature_celsius = current_head[104:108]
    encoded_longitude = current_head[108:112]
    encoded_latitude = current_head[112:116]
    speed_water_knots = current_head[116:120]
    course_over_ground = current_head[120:124]
    altitude_feet = current_head[124:128]
    heading_radians = current_head[128:132]
    flags = current_head[132:134]
    time1 = current_head[140:144]

    head_sub = (
        frame_offset + last_primary_channel_offset + last_secondary_channel_offset + last_downscan_channel_offset +
        last_left_sidescan_offset + last_right_sidescan_offset + last_composite_sidescan_offset + blockSize + lastBlockSize +
        channel_type + packet_size + frameIndex + upper_limit + lower_limit + frequency +
        depth + keelDepth  + speed_gps_knots + temperature_celsius + encoded_longitude +
        encoded_latitude + speed_water_knots + course_over_ground + altitude_feet + heading_radians + flags + time1
    )
    return head_sub
