#!/bin/bash

pushd /home/SkyCDS/
nohup python moguel_upload.py $1 $2 $3 $4 $5 $6 $7 &
popd
