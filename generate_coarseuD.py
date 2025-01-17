import json
import numpy as np
import cv2
import os
from compute_utils import *

data_folders = ['shrec22_real_train', 'shrec22_real_test']
# Please fill in your input path. The generated videos are in the same folder, e.g., 'shrec22_real_train_coarseuD/'
# The images for visualizations will be in 'shrec22_real_train_coarseuD/images/'
data_path = ''

start_t = 0 # the start time of the data (in s)
uD_frame_interval = 8.33 # the time interval of each coarse uD bin (in ms). This depends on STFT step size and chirp rate
vrange_ls = [-3, 3] # the range of the velocities (e.g., -3m/s to 3m/s), corresponding to the vmax
num_bins = 128 # the number of velocity bins (e.g., 2*vmax/num_bins=vres=6/128=0.046875m/s)  )
# vmax and vmin of the color in plotting coarse uD for visualizing. May need to tune this for better visualizations
plot_uD_vmin = 0 
plot_uD_vmax = 200 
camera_pos = [0, -0.3, -0.3] # camera position in the global coordinate. This should match the real capture setup
                             # Current value is set to imitate an ego-centric view to view the hand 
                             # The hand locates near the origin when visualizing in the point cloud video
cam_fps = 20.0               # Shrec22 camera is 20fps
gesture_names = ['GRAB', 'WAVE'] # the gestures to be visualized
# ['GRAB', 'PINCH', 'KNOB', 'WAVE', 'DENY', 'CROSS', 'CIRCLE', 'V', 'LEFT', 'RIGHT'] 
plot_flag = True # if plotting as images

for set_name in data_folders:
    pc_json_path = data_path + set_name + '/'
    vhist_path = data_path + set_name + '_coarseuD/'
    if not os.path.exists(vhist_path):
        os.makedirs(vhist_path)
    if plot_flag:
        if not os.path.exists(vhist_path+'images/'):
            os.makedirs(vhist_path+'images/')
    
    means = [] # list of mean values of the coarse uD (can be used for later network normalization)
    stds = [] # list of std values of the coarse uD (can be used for later network normalization)

    for file_name in sorted(os.listdir(pc_json_path)):
        if file_name.endswith('.json'):
            if file_name.split('_')[0] in gesture_names:
                json_file_path = os.path.join(pc_json_path, file_name)
                data = json.load(open(json_file_path))
                end_t = len(data)/cam_fps
                print('---Processing: ', file_name.replace('.json', ''), 'data length (s): ', end_t )

                vertices_array = []
                for i in range(len(data)):
                    data_frame = np.array(data[i])
                    vertices_array.append(data_frame)
                vertices_array = np.array(vertices_array)
                # interpolate the vertices
                vertices_interpo = interpo_vertices(start_t, end_t, vertices_array, uD_frame_interval) 
                # get radial velocity
                v_radial, norm = get_radial_velocity(vertices_interpo, uD_frame_interval, camera_pos) 
                vertice_hist = get_v_hist(v_radial, norm, vrange_ls, num_bins)

                means.append(np.mean(vertice_hist))
                stds.append(np.std(vertice_hist))
                
                np.save(vhist_path + file_name.replace('.json', '') +'.npy', vertice_hist)

                if plot_flag:
                    plot_uD(vertice_hist, plot_uD_vmin, plot_uD_vmax, end_t, file_name, vhist_path+'images/',num_bins, vrange_ls, uD_frame_interval)

    mean_value = np.mean(means)
    std_value = np.mean(stds)
    with open(os.path.join(vhist_path, 'note.txt'), 'w') as f:
        f.write(f'set_name: {set_name}\n')
        f.write(f'mean: {mean_value}\n')
        f.write(f'std: {std_value}\n')