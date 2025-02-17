# Gesture-uDGen
This repository contains code to generate coarse radar micro-Doppler for gestures. 

## Summary
* `generate_coarseuD.py` generates coarse micro-Doppler taking a sequence gesture meshes. 
* `compute_utils.py` has the function used in `generate_coarseuD.py`, e.g., calculating radial velocity.
* `generate_pc_video.py` takes the point cloud .json files and generates videos of point cloud visualizing the gesture.

## Dataset
The data is shrec22 dataset fitted meshes (778 vertices) json files. The format is 
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
For coarse micro-Doppler generation and ground truth gesture micro-Doppler capture in qualitative evaluation, we employed the TI AWR6843AOP radar with the following parameters, which differ from those used for gait capture.
| Parameter          | Value  | Parameter          | Value  | Parameter                 | Value  |
|----------------------|---------|----------------------|---------|-----------------------------|---------|
| Tx                  | 3       | Rx                   | 4       | Chirps per frame (per Tx)  | 64      |
| Bandwidth           | 4 GHz   | Chirp time           | 416 µs  | Samples per chirp          | 32      |
| Max range          | 0.96 m  | Range resolution     | 0.0375 m | Azimuth resolution        | 30°     |
| Maximum velocity   | 3 m/s   | Velocity resolution  | 0.09 m/s | Elevation resolution      | 30°     |
| STFT window size   | 128     | Overlap ratio        | 87.5%    | Window                     | Hamming |
