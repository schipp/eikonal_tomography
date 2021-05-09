import numpy as np

def generate_synthetic_velocity_model(gridpoints, mode='voronoi_random', n_voronoi=40):
    size = (int(np.sqrt(gridpoints.shape[0])), int(np.sqrt(gridpoints.shape[0])))
    velocity_model = np.ones(size)
    if mode == 'manual':
        velocity_model *= 2.5
        velocity_model[40:60, 40:60] = 3.5
        velocity_model[10:20, 70:80] = 3.5
        velocity_model[50:70, 25:40] = 1.5
    if mode == 'voronoi_random':
        from scipy.spatial import Voronoi
        from matplotlib import patches
        # voronoi points in area
        points = np.random.uniform(low=0, high=max(size), size=(n_voronoi, 2))
        # to stabilize, define points surrounding to have finite voronoi cells
        x1 = np.array((np.arange(-5, max(size)+5, 5), np.ones(22)*-5)).T
        x2 = np.array((np.arange(-5, max(size)+5, 5), np.ones(22)*(max(size)+5))).T
        y1 = np.array((np.ones(22)*-5, np.arange(-5, max(size)+5, 5))).T
        y2 = np.array((np.ones(22)*(max(size)+5), np.arange(-5, max(size)+5, 5))).T
        points = np.append(points, x1, axis=0)
        points = np.append(points, x2, axis=0)
        points = np.append(points, y1, axis=0)
        points = np.append(points, y2, axis=0)
        vor = Voronoi(points)
        # random base model
        velocity_model *= np.random.uniform(1, 4)
        # assign random velocity in each voronoi cell
        for region in vor.regions:
            if -1 not in region and len(region) != 0:
                # pick a random velocity
                vel = np.random.uniform(1, 4)
                # assign all points in voronoi cell that velocity
                vertices = vor.vertices[region]
                pol = patches.Polygon(vertices, closed=True)
                velocity_model[np.unravel_index(np.where(pol.contains_points(gridpoints)), shape=velocity_model.shape)] = vel
    
    return velocity_model