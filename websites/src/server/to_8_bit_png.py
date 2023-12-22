import pandas as pd
import numpy as np
import cv2
def process_dicom(dicom, inv, flip, wc, ww, violut_func):
    # proc_img = cv2.resize(dicom, (320, 416), interpolation = cv2.INTER_AREA)
    proc_img = apply_windowing(dicom, ww, wc, violut_func)
    if inv:
        proc_img = 255 - proc_img
    if flip:
        proc_img = np.fliplr(proc_img)
    return proc_img 
def apply_windowing(arr,
                           window_width=None,
                           window_center=None,
                           voi_func='LINEAR',
                           y_min=0,
                           y_max=255):
    assert window_width == None or window_width > 0
    y_range = y_max - y_min
    # float64 needed (default) or just float32 ?
    # arr = arr.astype(np.float64)
    arr = arr.astype(np.float32)
    
    if window_width == None or window_center == None:
        max_val = np.max(arr)
        arr = arr / max_val * y_range
    
    elif voi_func in [0, 1]:
        # PS3.3 C.11.2.1.2.1 and C.11.2.1.3.2
        if voi_func == 0:
            if window_width < 1:
                raise ValueError(
                    "The (0028,1051) Window Width must be greater than or "
                    "equal to 1 for a 'LINEAR' windowing operation")
            window_center -= 0.5
            window_width -= 1
        below = arr <= (window_center - window_width / 2)
        above = arr > (window_center + window_width / 2)
        between = np.logical_and(~below, ~above)

        arr[below] = y_min
        arr[above] = y_max
        
        if between.any():
            arr[between] = ((
                (arr[between] - window_center) / window_width + 0.5) * y_range
                            + y_min)
    elif voi_func == 1:
        arr = y_range / (1 +
                         np.exp(-4 *
                                (arr - window_center) / window_width)) + y_min
    else:
        raise ValueError(
            f"Unsupported (0028,1056) VOI LUT Function value '{voi_func}'")
        
    return arr