# custom_colors/color_profiles.py

import matplotlib.colors as mcolors
import numpy as np


def EK500colourmap():
    colors = [
        [255, 255, 255], [159, 159, 159], [95, 95, 95], [0, 0, 255], [0, 0, 127], 
        [0, 191, 0], [0, 127, 0], [255, 255, 0], [255, 127, 0], [255, 0, 191], 
        [255, 0, 0], [166, 83, 60], [120, 60, 40]
    ]
    return mcolors.ListedColormap(np.array(colors) / 255.0, name='EK500')

def EK80colourmap():
    colors = [
        [255, 255, 255], [156, 138, 168], [141, 125, 150], [126, 113, 132], 
        [112, 100, 114], [97, 88, 96], [82, 76, 78], [68, 76, 94], [53, 83, 129], 
        [39, 90, 163], [24, 96, 197], [9, 103, 232], [9, 102, 249], [9, 84, 234], 
        [15, 66, 219], [22, 48, 204], [29, 30, 189], [36, 12, 174], [37, 49, 165], 
        [38, 86, 156], [39, 123, 147], [40, 160, 138], [41, 197, 129], [37, 200, 122], 
        [30, 185, 116], [24, 171, 111], [17, 156, 105], [10, 141, 99], [21, 139, 92], 
        [68, 162, 82], [114, 185, 72], [161, 208, 62], [208, 231, 52], [255, 255, 42], 
        [254, 229, 43], [253, 204, 44], [253, 179, 45], [252, 153, 46], [252, 128, 47], 
        [252, 116, 63], [252, 110, 85], [252, 105, 108], [252, 99, 130], [252, 93, 153], 
        [252, 85, 160], [252, 73, 139], [253, 61, 118], [253, 48, 96], [254, 36, 75], 
        [255, 24, 54], [240, 30, 52], [226, 37, 51], [212, 44, 50], [198, 51, 49], 
        [184, 57, 48], [176, 57, 49], [170, 54, 51], [165, 51, 54], [159, 47, 56], 
        [153, 44, 58], [150, 39, 56], [151, 31, 45], [153, 23, 33], [154, 15, 22], 
        [155, 7, 11]
    ]
    return mcolors.ListedColormap(np.array(colors) / 255.0, name='EK80')

def Hmap():
    colors = [
        [5, 48, 97], [6, 50, 100], [7, 52, 103], [8, 54, 106], [9, 57, 109], 
        [11, 59, 112], [12, 61, 115], [13, 63, 118], [14, 65, 121], [15, 67, 124], 
        [16, 70, 127], [17, 72, 130], [18, 74, 133], [20, 76, 136], [21, 78, 139], 
        [22, 80, 142], [23, 83, 145], [24, 85, 148], [25, 87, 151], [26, 89, 154], 
        [27, 91, 157], [29, 93, 160], [30, 96, 163], [31, 98, 166], [32, 100, 169], 
        [33, 102, 172], [34, 104, 173], [36, 105, 174], [37, 107, 175], [38, 109, 176], 
        [40, 111, 176], [41, 112, 177], [42, 114, 178], [43, 116, 179], [45, 118, 180], 
        [46, 119, 181], [47, 121, 182], [49, 123, 183], [50, 125, 184], [51, 126, 184], 
        [53, 128, 185], [54, 130, 186], [55, 131, 187], [57, 133, 188], [58, 135, 189], 
        [59, 137, 190], [60, 138, 191], [62, 140, 191], [63, 142, 192], [64, 144, 193], 
        [66, 145, 194], [67, 147, 195], [70, 149, 196], [73, 151, 197], [76, 153, 198], 
        [80, 155, 199], [83, 157, 200], [86, 159, 201], [89, 161, 203], [92, 163, 204], 
        [95, 165, 205], [99, 167, 206], [102, 169, 207], [105, 171, 208], [108, 173, 209], 
        [111, 175, 210], [114, 177, 211], [118, 179, 212], [121, 181, 213], [124, 183, 214], 
        [127, 185, 216], [130, 187, 217], [133, 189, 218], [137, 191, 219], [140, 193, 220], 
        [143, 195, 221], [146, 197, 222], [148, 198, 223], [151, 199, 223], [153, 201, 224], 
        [156, 202, 225], [158, 203, 225], [161, 204, 226], [163, 206, 227], [165, 207, 228], 
        [168, 208, 228], [170, 209, 229], [173, 211, 230], [175, 212, 230], [178, 213, 231], 
        [180, 214, 232], [182, 215, 232], [185, 217, 233], [187, 218, 234], [190, 219, 234], 
        [192, 220, 235], [194, 222, 236], [197, 223, 237], [199, 224, 237], [202, 225, 238], 
        [204, 227, 239], [207, 228,239], [209, 229, 240], [211, 230, 240], [212, 230, 241], 
        [214, 231, 241], [215, 232, 241], [217, 233, 241], [218, 233, 242], [220, 234, 242], 
        [221, 235, 242], [223, 235, 243], [224, 236, 243], [226, 237, 243], [227, 238, 243], 
        [229, 238, 244], [230, 239, 244], [232, 240, 244], [233, 241, 244], [235, 241, 245], 
        [236, 242, 245], [238, 243, 245], [239, 243, 246], [241, 244, 246], [242, 245, 246], 
        [244, 246, 246], [245, 246, 247], [247, 247, 247], [247, 246, 245], [247, 245, 243], 
        [248, 244, 241], [248, 243, 240], [248, 242, 238], [248, 241, 236], [249, 239, 234], 
        [249, 238, 232], [249, 237, 230], [249, 236, 229], [250, 235, 227], [250, 234, 225], 
        [250, 233, 223], [250, 232, 221], [250, 231, 219], [251, 230, 217], [251, 229, 216], 
        [251, 228, 214], [251, 227, 212], [252, 225, 210], [252, 224, 208], [252, 223, 206], 
        [252, 222, 205], [253, 221, 203], [253, 220, 201], [253, 219, 199], [253, 217, 196], 
        [252, 215, 193], [252, 213, 191], [252, 210, 188], [251, 208, 185], [251, 206, 182], 
        [250, 204, 180], [250, 202, 177], [250, 200, 174], [249, 197, 171], [249, 195, 169], 
        [249, 193, 166], [248, 191, 163], [248, 189, 160], [248, 187, 158], [247, 184, 155], 
        [247, 182, 152], [247, 180, 149], [246, 178, 147], [246, 176, 144], [245, 174, 141], 
        [245, 171, 138], [245, 169, 136], [244, 167, 133], [244, 165, 130], [243, 162, 128], 
        [242, 160, 126], [241, 157, 124], [239, 154, 122], [238, 152, 120], [237, 149, 118], 
        [236, 146, 116], [235, 144, 114], [234, 141, 112], [232, 138, 110], [231, 136, 108], 
        [230, 133, 106], [229, 131, 104], [228, 128, 101], [227, 125, 99], [226, 123, 97], 
        [224, 120, 95], [223, 117, 93], [222, 115, 91], [221, 112, 89], [220, 109, 87], 
        [219, 107, 85], [217, 104, 83], [216, 101, 81], [215, 99, 79], [214, 96, 77], 
        [213, 93, 76], [211, 90, 74], [210, 87, 73], [208, 84, 72], [207, 82, 70], 
        [205, 79, 69], [204, 76, 67], [202, 73, 66], [201, 70, 65], [200, 67, 63], 
        [198, 64, 62], [197, 61, 61], [195, 59, 59], [194, 56, 58], [192, 53, 57], 
        [191, 50, 55], [190, 47, 54], [188, 44, 53], [187, 41, 51], [185, 38, 50], 
        [184, 36, 48], [182, 33, 47], [181, 30, 46], [179, 27, 44], [178, 24, 43], 
        [175, 23, 43], [172, 22, 42], [169, 21, 42], [166, 20, 41], [164, 19, 41], 
        [161, 18, 40], [158, 18, 40], [155, 17, 39], [152, 16, 39], [149, 15, 38], 
        [146, 14, 38], [143, 13, 37], [141, 12, 37], [138, 11, 37], [135, 10, 36], 
        [132, 9, 36], [129, 8, 35], [126, 7, 35], [123, 6, 34], [120, 6, 34], 
        [117, 5, 33], [115, 4, 33], [112, 3, 32], [109, 2, 32], [106, 1, 31], 
        [103, 0, 31]
    ]
    return mcolors.ListedColormap(np.array(colors) / 255.0, name='Hmap')