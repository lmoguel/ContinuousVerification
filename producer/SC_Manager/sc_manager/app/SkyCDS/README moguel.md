##
moguel_upload.py

Programa encargado de sensar la carpeta especificada y subir los archivos cada periodo de tiempo

Recibe los siguientes parametros:

tokenuser: token de usuario (obtenido de db_auth_local de skycds)
apikey: llave de api (obtenido de db_auth_local de skycds)
catalogToken:token de catalogo (obtenido de db_pub_sub_local de skycds)
chunk_path: ruta de la carpeta a sensar
organization: organización de skycds ((obtenido de db_auth_local de skycds))
accessToken: token de acceso (obtenido de db_auth_local de skycds)
interval: tiempo de sensado en segundos


##
moguel_download.py

Programa encargado de sensar la carpeta especificada y descargar los archivos cada periodo de tiempo

Recibe los siguientes parametros:

tokenuser: token de usuario (obtenido de db_auth_local de skycds)
apikey: llave de api (obtenido de db_auth_local de skycds)
catalogToken:token de catalogo (obtenido de db_pub_sub_local de skycds)
chunk_path: ruta de la carpeta a sensar
organization: organización de skycds ((obtenido de db_auth_local de skycds))
accessToken: token de acceso (obtenido de db_auth_local de skycds)
interval: tiempo de sensado en segundos
ip = ip del servidor que tiene skycds sin puerto