#!/bin/bash
#

echo Levantando los servicios de ${PWD} de Supply Chain

#python borrarTodoContainers.py

pushd ${PWD}/producer
python readFile.py
popd

#pushd ${PWD}/qrs_detector
#docker-compose up -d
#python readFile.py
#popd

#pushd ${PWD}/visualization
#python readFile.py
#popd
