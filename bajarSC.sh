echo Dando de baja los servicios de ${PWD}

#python borrarTodoContainers.py

pushd ${PWD}/producer/SC_Manager
docker-compose down -v
rm -rf sc_manager/app/DaemonOutputs/*
rm -rf sc_manager/app/tiempos/*
popd

pushd ${PWD}/producer/PRO
docker-compose down -v
rm -rf bb_manager/app/DaemonOutputs/*
rm -rf bb_manager/app/tiempos/*
popd

#pushd ${PWD}/qrs_detector/
#docker-compose down -v
#popd

#pushd ${PWD}/qrs_detector/SC_Manager
#docker-compose down -v
#rm -rf sc_manager/app/DaemonOutputs/*
#rm -rf sc_manager/app/tiempos/*
#popd

#pushd ${PWD}/qrs_detector/QRS
#docker-compose down -v
#rm -rf bb_manager/app/DaemonOutputs/*
#rm -rf bb_manager/app/tiempos/*
#popd

#pushd ${PWD}/visualization/SC_Manager
#docker-compose down -v
#rm -rf sc_manager/app/DaemonOutputs/*
#rm -rf sc_manager/app/tiempos/*
#popd

#pushd ${PWD}/visualization/VIS
#docker-compose down -v
#rm -rf bb_manager/app/DaemonOutputs/*
#rm -rf bb_manager/app/tiempos/*
#popd
