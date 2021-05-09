import numpy as np
from scipy import interpolate

def interp2d_with_nans(array):
    x = np.arange(0, array.shape[1])
    y = np.arange(0, array.shape[0])
    #mask invalid values
    array = np.ma.masked_invalid(array)
    xx, yy = np.meshgrid(x, y)
    #get only the valid values
    x1 = xx[~array.mask]
    y1 = yy[~array.mask]
    newarr = array[~array.mask]
    return interpolate.griddata((x1, y1), newarr.ravel(), (xx, yy), method='cubic')


def convert_traveltime_dict_to_map(staidx, stations, station_pair_tt):
    # TODO: cleanup
    traveltime_map = np.zeros((100, 100))
    traveltime_map[:] = np.nan
    for key, value in station_pair_tt.items():
        if f'{staidx:03d}' in key:
            if f'{staidx:03d}' == key.split('-')[0]:
                sta2idx = int(key.split('-')[1])
                tt = station_pair_tt[f'{staidx:03d}-{sta2idx:03d}']
            elif f'{staidx:03d}' == key.split('-')[1]:
                sta2idx = int(key.split('-')[0])
                tt = station_pair_tt[f'{sta2idx:03d}-{staidx:03d}']
            else:
                continue
            traveltime_map[stations[sta2idx][0], stations[sta2idx][1]] = tt
    
    return traveltime_map