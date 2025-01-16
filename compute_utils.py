import numpy as np
from scipy import interpolate
import matplotlib.pyplot as plt

def interpo_vertices(start_t, end_t, vertices_ls, uD_frame_interval):
    uD_bins_ps = int(1000/uD_frame_interval) # the number of uD bins in one second
    uD_t = np.linspace(start_t, end_t, int((end_t - start_t)*uD_bins_ps))
    mesh_t = np.linspace(start_t, end_t, len(vertices_ls))
    f_vertice = interpolate.interp1d(mesh_t, vertices_ls, axis = 0)
    vertices_ls_interpo = f_vertice(uD_t)
    return vertices_ls_interpo

def get_radial_velocity(vertices_ls, uD_frame_interval, camera_pos):
    # radial velocity of the vertices
    uD_bins_ps = int(1000/uD_frame_interval) # the number of uD bins in one second
    camera_pos_interpo =  np.expand_dims(np.expand_dims(camera_pos, axis=0), axis = 1)
    camera_pos_interpo =  np.repeat(np.repeat(camera_pos_interpo, vertices_ls.shape[0], axis = 0), vertices_ls.shape[1], axis = 1)
    vertices_v = vertices_ls[1:, :, :] - vertices_ls[:-1, :, :]
    r = vertices_ls[:-1, :, :] - camera_pos_interpo[:-1, :, :] # r (distance) vector from camera to vertices
    norm = np.expand_dims(np.linalg.norm(r, axis = 2), axis=2)
    r_unit = np.divide(r, np.repeat(norm, 3, axis = 2) ) # r unit vector
    v_radial = -np.multiply(vertices_v, r_unit).sum(axis = 2) * uD_bins_ps
    return v_radial, norm

def get_v_hist(v_radial, norm, range_ls = [-3,3], num_bins=128, distance_pow_loss=True):
    hist_ls = []
    if distance_pow_loss:
        # power loss is inversely proportional to the square of the distance
        alpha = 1/norm**2
        alpha = np.squeeze(alpha)
        row, col = np.where(np.squeeze(norm)<0.1)
        alpha[row, col] = 0

    for i in range(v_radial.shape[0]):
        if distance_pow_loss:
            hist = np.histogram(v_radial[i,:], range=range_ls, bins=num_bins, weights = alpha[i,:])
        else:
            hist = np.histogram(v_radial[i,:], range=range_ls, bins=num_bins)
        hist_ls.append(hist[0])
    return np.array(hist_ls).T

def plot_uD(vertice_hist, plot_uD_vmin, plot_uD_vmax, end_t, file_name, image_path, num_bins, range_ls, uD_frame_interval):
    uD_bins_ps = int(1000/uD_frame_interval)
    plt.figure()
    plt.imshow(vertice_hist,aspect='auto',vmin=plot_uD_vmin, vmax=plot_uD_vmax, cmap='jet')
    cbar = plt.colorbar()
    cbar.set_label('Number of Vertices')
    plt.xticks(np.linspace(0, int(end_t*uD_bins_ps), 10), np.round(np.linspace(0, end_t, 10),2))
    plt.yticks(np.linspace(0, num_bins, 5), np.linspace(range_ls[0], range_ls[1], 5))
    plt.title(file_name.replace('.json', ''))
    plt.xlabel('Time (s)')
    plt.ylabel('Doppler (m/s)')
    plt.savefig(image_path + file_name.replace('.json', '') +'_coarseuD.png')