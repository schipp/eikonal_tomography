import numpy as np

from tqdm import tqdm
from itertools import combinations, product
from scipy.ndimage import gaussian_gradient_magnitude

from lib.synth import generate_synthetic_velocity_model
from lib.fmm import get_traveltimes_for_source_station
from lib.util import interp2d_with_nans, convert_traveltime_dict_to_map
from lib.plotting import plot_results

if __name__ == '__main__':
    # define stations and grid geometry
    # for now use only integers and (100, 100) grid
    # grid of stations
    stations = np.array(list(product(np.arange(5, 100, 5), np.arange(5, 100, 5))))
    # randomly distributed stations
    # stations = np.random.uniform(low=5, high=95, size=(50, 2)).astype(int)
    gridpoints = np.array(list(product(np.arange(1, 100+1, 1), np.arange(1, 100+1, 1))))

    # generate synthetic model to explore
    velocity_model = generate_synthetic_velocity_model(gridpoints)

    # get all traveltimes for all station pairs (this can be somewhat slow)
    # thanks to reciprocity only need to compute for combinations
    station_pair_tt = {}
    for (sta1idx, sta1), (sta2idx, sta2) in tqdm(combinations(enumerate(stations), 2), total=(len(stations)*len(stations)-1)/2):
        traveltimes = get_traveltimes_for_source_station(sta1, stations, velocity_model)
        tt = traveltimes[sta2[0], sta2[1]]
        # save into the dict
        station_pair_tt[f'{sta1idx:03d}-{sta2idx:03d}'] = tt

    # compute gradient maps for all source stations from traveltime dict
    gradients = []
    for staidx, station in enumerate(stations):
        traveltime_map = convert_traveltime_dict_to_map(staidx, stations, station_pair_tt)
        traveltime_map_interp = interp2d_with_nans(traveltime_map)
        gradient = gaussian_gradient_magnitude(traveltime_map_interp, sigma=1, mode='constant', cval=2.5)
        gradients.append(gradient)

    # -- visualizsation:

    # get synthetic travel times through model, using FMM
    traveltimes_sample = get_traveltimes_for_source_station(stations[0], stations, velocity_model)

    # get sample traveltime field as resolved by station distribution
    # start with empty traveltime map
    traveltime_map = np.zeros((100, 100))
    traveltime_map[:] = np.nan
    for sta2 in stations:
        error = np.random.uniform(-2, 2)
        # fill traveltime map with measured traveltimes at stations
        traveltime_map[sta2[0], sta2[1]] = traveltimes_sample[sta2[0], sta2[1]] + error
    # interpolate traveltime map
    traveltimes_map_interp_sample = interp2d_with_nans(traveltime_map)

    plot_results(stations, velocity_model, traveltimes_sample, traveltimes_map_interp_sample, gradients)