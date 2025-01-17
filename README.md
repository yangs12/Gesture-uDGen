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

