#!/bin/bash
#

#-------------------------------------------------------
echo Borrando carpetas /var/lib/docker/volumes

pushd /var/lib/docker/volumes
rm -rf volumes_catalogs_8000/_data/*
rm -rf volumes_catalogs_8005/_data/*
#rm -rf volumes_catalogs_8010/_data/*
rm -rf volumes_catalogs_8015/_data/*
popd

