#!/bin/bash

# if [[ $# -ne 1 ]]; then
#     echo "Usage: $0 <out sif>"
#     exit 1
# fi

echo "Building to vtk.sif"
time sudo /home/jakob/bin/singularity build vtk.sif Singularity
