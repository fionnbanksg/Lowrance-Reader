import numpy as np

sl3_dtype = np.dtype([
    ('frame_offset', 'uint32'),                                  
    ('blocksize', 'int16'),                    
    ('previous_blocksize', 'int16'),           
    ('channel_type', 'int16'),                                    
    ('block_frame_index', 'uint32'),          
    ('upper_limit', 'float32'),                
    ('lower_limit', 'float32'),                
    ('blockSize', 'int16'),
    ('lastBlockSize', 'int16'), 
    ('channel_name', 'int16'), 
    ('frameIndex', 'uint32'),   
    ('creation_data_time', 'uint32'),         
    ('packet_size', 'int16'),                                  
    ('depth', 'float32'),                     
    ('frequency', 'uint8'),                                        
    ('speed_gps_knots', 'float32'),            
    ('temperature_celsius', 'float32'),        
    ('encoded_longitude', 'int32'),           
    ('encoded_latitude', 'int32'),             
    ('speed_water_knots', 'float32'),         
    ('course_over_ground', 'float32'),        
    ('altitude_feet', 'float32'),             
    ('heading_radians', 'float32'),            
    ('flags', 'uint16'),                                            
    ('time_from_creation_ms', 'uint32'),       
    ('last_primary_channel_offset', 'uint32'), 
    ('last_secondary_channel_offset', 'uint32'),
    ('last_downscan_channel_offset', 'uint32'),
    ('last_left_sidescan_offset', 'uint32'),  
    ('last_right_sidescan_offset', 'uint32'),  
    ('last_composite_sidescan_offset', 'uint32'),                    
    ('last_three_dc_channel_offset', 'uint32'),                   
])



def extract_fields_sl3(current_head):
    frame_offset = current_head[0:4]
    blocksize = current_head[8:10]
    previous_blocksize = current_head[10:12]
    channel_type = current_head[12:14]
    block_frame_index = current_head[16:20]
    upper_limit = current_head[20:24]
    lower_limit = current_head[24:28]
    blockSize = current_head[28:30]
    lastBlockSize = current_head[30:32]
    channel_name = current_head[32:34]
    frameIndex = current_head[36:40]
    creation_data_time = current_head[40:44]
    packet_size = current_head[44:46]
    depth = current_head[48:52]
    frequency = current_head[52:53]
    speed_gps_knots = current_head[84:88]
    temperature_celsius = current_head[88:92]
    encoded_longitude = current_head[92:96]
    encoded_latitude = current_head[96:100]
    speed_water_knots = current_head[100:104]
    course_over_ground = current_head[104:108]
    altitude_feet = current_head[108:112]
    heading_radians = current_head[112:116]
    flags = current_head[116:118]
    time_from_creation_ms = current_head[124:128]
    last_primary_channel_offset = current_head[128:132]
    last_secondary_channel_offset = current_head[132:136]
    last_downscan_channel_offset = current_head[136:140]
    last_left_sidescan_offset = current_head[140:144]
    last_right_sidescan_offset = current_head[144:148]
    last_composite_sidescan_offset = current_head[148:152]
    last_three_dc_channel_offset = current_head[164:168]


    head_sub = (
        frame_offset + blocksize + previous_blocksize + channel_type + block_frame_index + upper_limit + lower_limit + blockSize  + lastBlockSize +  channel_name + frameIndex +
        creation_data_time + packet_size + depth + frequency + speed_gps_knots + temperature_celsius + encoded_longitude +
        encoded_latitude + speed_water_knots + course_over_ground +
        altitude_feet + heading_radians + flags +
        time_from_creation_ms + last_primary_channel_offset +
        last_secondary_channel_offset + last_downscan_channel_offset +
        last_left_sidescan_offset + last_right_sidescan_offset +
        last_composite_sidescan_offset + last_three_dc_channel_offset
    )
    return head_sub
