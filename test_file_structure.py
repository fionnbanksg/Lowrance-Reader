def load_calibration_file(file_path):
    calibration_data = {}
    
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith("%%") or not line:  # Skip comments and empty lines
                continue
            if '<' in line and '>' in line:
                key, value = line.split('<')
                key = key.strip()
                value = value.split('>')[0].strip()
        
                try:
                    value = float(value.replace('e', 'E'))
                except ValueError:
                    pass 
                
                calibration_data[key] = value
    
    return calibration_data


file_path = 'calibration\CALIBRATION.md'
calibration_data = load_calibration_file(file_path)
print(calibration_data)

# Assigning data to variables
freq = calibration_data.get('freq')
zer = calibration_data.get('zer')
zet = calibration_data.get('zet')
alpha = calibration_data.get('alpha')
c = calibration_data.get('c')
g = calibration_data.get('g')

# Print the variables to verify
print(f"Frequency: {freq}")
print(f"Zero: {zer}")
print(f"Zet: {zet}")
print(f"Alpha: {alpha}")
print(f"Speed of Sound (c): {c}")
print(f"Gain (g): {g}")