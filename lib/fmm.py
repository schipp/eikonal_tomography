import skfmm
import numpy as np

def get_traveltimes_for_source_station(source_station, stations, velocity_model):
    phi = np.ones((100, 100))
    phi[source_station[0], source_station[1]] = -1 
    traveltimes = skfmm.travel_time(phi, speed=velocity_model)
    return traveltimes