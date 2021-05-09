import matplotlib
import pylab as plt
import numpy as np

def plot_results(stations, velocity_model, traveltimes_sample, traveltimes_map_interp_sample, gradients):
    cmap = matplotlib.cm.get_cmap('RdBu')
    norm = matplotlib.colors.Normalize(vmin=1, vmax=4)
    fig, axs = plt.subplots(1, 3, sharex=True, sharey=True, figsize=(9, 3))
    fig.subplots_adjust(left=0.05, right=.9, bottom=0, top=1, wspace=.4)
    ax = axs[0]
    ax.set_aspect('equal')
    xx, yy = np.meshgrid(np.arange(1, 100+1, 1), np.arange(1, 100+1, 1))
    pcm = ax.pcolormesh(xx, yy, velocity_model.T, cmap='RdBu', shading='nearest', vmin=1, vmax=4)
    x0, y0, w, h = ax.get_position().bounds
    cax = fig.add_axes((x0+w, y0, w*0.05, h))
    cbar = plt.colorbar(pcm, cax=cax)
    cbar.ax.set_ylabel('phase velocity [km/s]')

    ax.scatter(*stations.T, c='k', marker='v', ec='w', lw=.25, s=5)
    # ax.scatter(*stations[0], c='r', marker='v', ec='w', lw=.25)


    ax.set_title('synthetic velocity model')

    # # ---

    # ax = axs.flatten()[1]
    # ax.set_aspect('equal')

    # pcm = ax.pcolormesh(xx, yy, traveltimes_sample.T, cmap='inferno', vmin=0, vmax=50)

    # x0, y0, w, h = ax.get_position().bounds
    # cax = fig.add_axes((x0+w, y0, w*0.05, h))
    # plt.colorbar(pcm, cax=cax)

    # ax.set_title('traveltimes full')

    # # ---

    # ax = axs.flatten()[2]
    # ax.set_aspect('equal')
    # # pcm = ax.contourf(traveltimes_map_interp.T, cmap='inferno', levels=20) # , vmin=1, vmax=4)
    # pcm = ax.pcolormesh(xx, yy, traveltimes_map_interp_sample.T, cmap='inferno', vmin=0, vmax=50)
    # # plt.colorbar(pcm)

    # ax.set_title('traveltimes recovered\ninterpolated')

    # ---

    # eikonal tomography
    ax = axs[1]
    ax.set_title('eikonal tomography')
    ax.set_aspect('equal')
    mean_grad = np.mean(np.array(gradients), axis=0)
    # pcm = ax.contourf(1/mean_grad.T, cmap='RdBu', levels=30) #  vmin=1, vmax=4)
    pcm = ax.pcolormesh(xx, yy, 1/mean_grad.T, cmap='RdBu', shading='nearest', vmin=1, vmax=4)

    ax.scatter(*stations.T, c='k', marker='v', ec='w', s=5, lw=.25)

    x0, y0, w, h = ax.get_position().bounds
    cax = fig.add_axes((x0+w, y0, w*0.05, h))
    cbar = plt.colorbar(pcm, cax=cax)
    cbar.ax.set_ylabel('phase velocity [km/s]')

    # ---

    ax = axs[2]
    ax.set_title('velocity uncertainty')
    ax.set_aspect('equal')
    std_grad = np.nanstd(np.array(gradients), axis=0)
    # pcm = ax.contourf(std_grad.T, levels=30) # , vmin=1, vmax=4)
    pcm = ax.pcolormesh(xx, yy, std_grad.T, shading='nearest')

    x0, y0, w, h = ax.get_position().bounds
    cax = fig.add_axes((x0+w, y0, w*0.05, h))
    cbar = plt.colorbar(pcm, cax=cax)
    cbar.ax.set_ylabel('standard deviation [km/s]')

    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    fig.savefig('test.png', dpi=300)