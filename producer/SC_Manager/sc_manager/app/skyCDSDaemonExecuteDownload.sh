#!/bin/bash

pushd /home/SkyCDS/
nohup python moguel_download.py $1 $2 $3 $4 $5 $6 $7 $8 &
popd
