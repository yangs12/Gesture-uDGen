import json
import numpy as np
import matplotlib.pyplot as plt
import cv2
import os

data_folders = ['shrec22_real_train', 'shrec22_real_test']
# Please fill in your input path. The generated videos are in the same folder, e.g., 'shrec22_real_train_pc_videos/'
data_path = '' 

cam = [0, -0.3, -0.3] # camera location
cam_fps = 20.0 # camera fps
gesture_names = ['GRAB', 'WAVE'] # the gestures to be visualized
# ['GRAB', 'PINCH', 'KNOB', 'WAVE', 'DENY', 'CROSS', 'CIRCLE', 'V', 'LEFT', 'RIGHT'] 


for set_name in data_folders:
    # input point cloud path
    pc_json_path = data_path + set_name + '/' 
    # output image and video path
    images_folder = data_path + set_name + '_pc_videos/' 
    if not os.path.exists(images_folder):
        os.makedirs(images_folder)

    for file_name in sorted(os.listdir(pc_json_path)):
        if file_name.endswith('.json'):
            json_file_path = os.path.join(pc_json_path, file_name)
            
            if file_name.split('_')[0] in gesture_names:
                print('---Processing: ', file_name.replace('.json', '') )
                # load the point cloud json
                data = json.load(open(json_file_path))

                # create a folder for saving point cloud images for each file
                image_folder = images_folder + file_name.replace('.json', '/') 
                
                if not os.path.exists(image_folder):
                    os.makedirs(image_folder)
                for i in range(len(data)):
                    data_frame = np.array(data[i])
                    fig = plt.figure(figsize=(6, 6))
                    ax = fig.add_subplot(projection='3d')
                    ax.view_init(elev=-30, azim=-90)
                    scale = 0.3
                    ax.set_xlim([-scale, scale])
                    ax.set_zlim([-scale, scale])
                    ax.set_ylim([-scale, scale])
                    ax.scatter(data_frame[:, 0], data_frame[:, 1], data_frame[:, 2], alpha=0.1)
                    ax.scatter(cam[0], cam[1], cam[2], c='r', marker='o', label='camera')
                    ax.legend()
                    ax.set_xlabel('X')
                    ax.set_ylabel('Y')
                    ax.set_zlabel('Z')
                    plt.title(file_name + '  Frame ' + str(i))
                    plt.savefig(image_folder + 'pt_frame' + str(i) + '.png')
                    plt.close()
                
                # write the images into a video
                video_name = set_name + '_' + file_name.replace('.json', '') + '.mp4'
                img_array = []
                for i in range(len(data)):
                    filename = image_folder + 'pt_frame' + str(i) + '.png'
                    img = cv2.imread(filename)
                    height, width, layers = img.shape
                    size = (width, height)
                    img_array.append(img)

                out = cv2.VideoWriter(images_folder + video_name, cv2.VideoWriter_fourcc(*'mp4v'), cam_fps, size)

                for i in range(len(img_array)):
                    out.write(img_array[i])
                out.release()
                
                # remove the folder of images after generating the video
                for file in os.listdir(image_folder):
                    file_path = os.path.join(image_folder, file)
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                os.rmdir(image_folder)

