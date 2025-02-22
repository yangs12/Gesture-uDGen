# Gesture-uDGen
This repository contains code to generate coarse radar micro-Doppler for gestures. The proposed pipeline can be easily adapted to work on more diverse datasets with a greater variety of gestures, gesture directions, and subjects. Additionally, while this project has demonstrated the possibility of generating coarse micro-Doppler as the foundation for high-resolution micro-Doppler synthesis, generating micro-Doppler signatures comparable with real-world data requires refining coarse micro-Doppler into fine-grained synthetic micro-Doppler using generative models.


## Summary
* `generate_coarseuD.py` generates coarse micro-Doppler taking a sequence gesture meshes. 
* `compute_utils.py` has the functions used in `generate_coarseuD.py`, e.g., calculating radial velocity.
* `generate_pc_video.py` takes the point cloud .json files and generates videos of point cloud visualizing the gesture.

## Dataset
The dataset contains sequences of fitted hand meshes (778 vertices) json files, e.g., shrec22 dataset. The format is 
```
shrec22_real_train
  ├── CIRCLE_s0.json
  ...
shrec22_real_test
  ├── CIRCLE_s0.json
  ...
```

## Environment setup
1. Clone this repository
2. Create a conda environment
```
conda create --name coarseuD_gen python=3.10
conda activate coarseuD_gen
pip install -r requirements.txt
```

## Gesture Parameters
For coarse micro-Doppler generation, we employed the TI AWR6843AOP radar with the following parameters. 
| Parameter          | Value  | Parameter          | Value  | Parameter                 | Value  |
|----------------------|---------|----------------------|---------|-----------------------------|---------|
| Tx                  | 3       | Rx                   | 4       | Chirps per frame (per Tx)  | 64      |
| Bandwidth           | 4 GHz   | Chirp time           | 416 µs  | Samples per chirp          | 32      |
| Maximum range          | 0.96 m  | Range resolution     | 0.0375 m | Azimuth resolution        | 30°     |
| Maximum velocity   | 3 m/s   | Velocity resolution  | 0.09 m/s | Elevation resolution      | 30°     |
| STFT window size   | 128     | Overlap ratio        | 87.5%    | Window                     | Hamming |

These parameters are optimized for gesture recognition. For instance, the maximum range aligns with the ego-centric perspective of hands, and multiple transmitters and receivers enhance angle diversity for better hand identification/tracking. In contrast to gait recognition, where subjects are typically at a longer range (5–15m), the direction of hand gestures might play a more significant role due to their close-range motion.


## Finetuning Coarse Micro-Doppler to Final Synthetic Micro-Doppler
To finetune coarse micro-Doppler data, generative networks such as a conditional GAN and diffusion models could be used. Here we take conditional GAN as an example.

The pix2pix conditional GAN network could be utilized <a href="https://github.com/phillipi/pix2pix.git"> (link) </a>. You can refer to this gait micro-Doppler synthesis repository for details on constructing and training the conditional GAN: <a href="https://github.com/yangs12/High-Resolution-Gait-Micro-Doppler-Synthesis-from-Videos-Over-Diverse-Trajectories.git"> (link) </a>. 

### Dataset Preparation
* Paired data: The pix2pix network requires paired input-output data. Therefore, each training sample should consist of a paired coarse micro-Doppler and a fine, real micro-Doppler signature, generated and captured using identical parameters (e.g., [gesture parameters](#gesture-parameters)). 
* Data split: The dataset need to be split into train (for conditional GAN training), evaluation, and test sets (for generating synthetic data for later evaluations, such as evaluation classifier training and testing).
* Dataloader and data format: To construct the dataset and dataloader, the input–ground truth pairs share the same dimensions and filenames across corresponding folders. For details, please refer to pix2pix dataset guidance <a href="https://github.com/junyanz/pytorch-CycleGAN-and-pix2pix/blob/master/docs/datasets.md"> (link) </a>.

### Preprocessing and Training
Gesture motion shares similar challenges with gait motion, where subtle finger movements in gesture are overshadowed by global palm motion, as fine limb motions in gait are masked by overall torso movement. Therefore, the networks in the gait micro-Doppler simulation repository could be repurposed <a href="https://github.com/yangs12/High-Resolution-Gait-Micro-Doppler-Synthesis-from-Videos-Over-Diverse-Trajectories/tree/main/pytorch-CycleGAN-and-pix2pix/models.md"> (link) </a>.

* Training Considerations
  * Classifier loss and feature Loss: These two loss terms require a pretrained MobileNetv2 classifier on the training data for conditional GAN.
  * Temporal flipping: Since flipping the micro-Doppler means reversing the time sequence, the gait pipeline makes sure no temporal flipping for the dataset. 
  * Temporal cropping: One step in the gait preprocessing is cropping 1.28-second signatures into 0.64-second snapshots in training, to match walking dynamics (step time 0.64-second) and reduce phase sensitivity. For gestures, cropping may not be necessary since gestures can be segmented with a clear start and end time.
  

## Differences between Fintuning Gesture and Gait Coarse Micro-Doppler
When repurposing the gait micro-Doppler synthesis pipeline for gesture applications, here shows some key differences and some challenges:
* Dataset
  * Paired data: Gesture synthesis requires paired coarse and real micro-Doppler signatures, collected under consistent gesture-specific configurations. 
  * Effects of range and direction: Unlike gait (typically captured at long distance), gestures are recorded at close range. This increases the gesture micro-Doppler signatures' sensitivity to motion directions. Besides, gesture motion directions can be more diverse than gait motion. 
  * Clutter: Gesture datasets might include background clutter (e.g., chairs, tables), unlike the relatively clutter-free gait datasets (MVDoppler).
* Preprocessing and Model
  * Temporal Length: Gestures vary in duration (e.g., pinch vs. swipe) and their dynamics can be fast-changing, so input lengths may differ from gait and across gestures. 
  * Temporal cropping: While temporal cropping is important for gait pipeline to manage model's robustness to phase variations, it might be unnecessary for segmented gesture data. The gesture motion is also more non-periodic.
  * Network Hyperparameters: Gestures usually involve finer movements than gait motion. Thus, the hyperparameters may need adjustments to fit the different feature complexities, e.g., the generator architecture, discriminator layers, number of epochs, etc.

  
