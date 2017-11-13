# Mesh to PointCloud

This tool can uniformly sample 3d points from mesh. The output is a simple ascii format `[x] [y] [z]` point cloud file.

## Requirements
- python3
- numpy
- trimesh

## Usage

```
python3 sample.py [-h] -i INPUT_FILE -o OUTPUT_FILE [-n NUMBER_OF_POINTS] [--normalize]
python3 sample.py -i model.off -o output.txt -n 1000 --normalize
```

## TODO

- `.pcd`, `.xyz`, and `.pts` .etc file formats support
