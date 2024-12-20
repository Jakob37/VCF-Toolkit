#!/bin/bash

echo "Building to vtk.sif"
time sudo /home/jakob/bin/singularity build vtk.sif Singularity

echo "Copying vtk.sif to /fs1"
scp vtk.sif Hopper:/fs1/jakob/containers/vtk.sif
