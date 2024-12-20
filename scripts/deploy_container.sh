#!/bin/bash

# if [[ $# -ne 1 ]]; then
#     echo "Usage: $0 <sif>"
#     exit 1
# fi

echo "Copying vtk.sif to /fs1"
scp vtk.sif Hopper:/fs1/jakob/containers/vtk.sif
