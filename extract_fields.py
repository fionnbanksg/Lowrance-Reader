def extract_fields_s3(current_head):
    # Extracting specific fields based on the given dtype offsets
    frame_offset = current_head[0:4]
    unknown1 = current_head[4:8]
    blocksize = current_head[8:10]
    previous_blocksize = current_head[10:12]
    channel_type = current_head[12:14]
    padding1 = current_head[14:16]
    block_frame_index = current_head[16:20]
    upper_limit = current_head[20:24]
    lower_limit = current_head[24:28]
    unknown2 = current_head[28:40]
    creation_data_time = current_head[40:44]
    packet_size = current_head[44:46]
    padding2 = current_head[46:48]
    depth = current_head[48:52]
    frequency = current_head[52:53]
    padding3 = current_head[53:84]
    speed_gps_knots = current_head[84:88]
    temperature_celsius = current_head[88:92]
    encoded_longitude = current_head[92:96]
    encoded_latitude = current_head[96:100]
    speed_water_knots = current_head[100:104]
    course_over_ground = current_head[104:108]
    altitude_feet = current_head[108:112]
    heading_radians = current_head[112:116]
    flags = current_head[116:118]
    padding4 = current_head[118:124]
    time_from_creation_ms = current_head[124:128]
    last_primary_channel_offset = current_head[128:132]
    last_secondary_channel_offset = current_head[132:136]
    last_downscan_channel_offset = current_head[136:140]
    last_left_sidescan_offset = current_head[140:144]
    last_right_sidescan_offset = current_head[144:148]
    last_composite_sidescan_offset = current_head[148:152]
    unknown3 = current_head[152:164]
    last_three_dc_channel_offset = current_head[164:168]

    # Concatenating extracted fields
    head_sub = (
        frame_offset + unknown1 + blocksize + previous_blocksize + channel_type +
        padding1 + block_frame_index + upper_limit + lower_limit + unknown2 +
        creation_data_time + packet_size + padding2 + depth + frequency +
        padding3 + speed_gps_knots + temperature_celsius + encoded_longitude +
        encoded_latitude + speed_water_knots + course_over_ground +
        altitude_feet + heading_radians + flags + padding4 +
        time_from_creation_ms + last_primary_channel_offset +
        last_secondary_channel_offset + last_downscan_channel_offset +
        last_left_sidescan_offset + last_right_sidescan_offset +
        last_composite_sidescan_offset + unknown3 + last_three_dc_channel_offset
    )
    return head_sub
