# SkyCDS-Client

SkyCDS is a resilient content delivery service based on a publish/subscribe overlay over diversified cloud storage. SkyCDS splits the content delivery into metadata and content storage flow layers.

### Reference:

Gonzalez, J. L., Perez, J. C., Sosa-Sosa, V. J., Sanchez, L. M., & Bergua, B. (2015). SkyCDS: A resilient content delivery service based on diversified cloud storage. Simulation Modelling Practice and Theory, 54, 64-85.

### Content

* **moguel_upload.py**. Programa encargado de sensar la carpeta especificada y subir los archivos cada periodo de tiempo.
* **moguel_download.py**. Programa encargado de sensar la carpeta especificada y descargar los archivos cada periodo de tiempo.



### moguel_upload.py configuration

```bash
python moguel_upload.py 7b22d86e036b1bb4caf350d4bc2de4e40009159496e0a10c03a318e39e3f6ad0 c81ffa68bd5ac4d8c0c915c95f5a56305b435d0e 7c0c7ebfd042edfc3515ba8e85514ac647be7c0caa74cdc22a194da45abe1283 /home/fernando/Escritorio/skyCDS_Junio/Entrada MOGUI f0578b9cfec53e3af56e1f809e0802e8f3a5c487b7b7a0d9d374e17978c7ae95 30
```


Params:
1. tokenuser: token de usuario (obtenido de db_auth_local de skycds)
2. apikey: llave de api (obtenido de db_auth_local de skycds)
3. catalogToken:token de catalogo (obtenido de db_pub_sub_local de skycds)
4. chunk_path: ruta de la carpeta a sensar
5. organization: organización de skycds ((obtenido de db_auth_local de skycds))
6. accessToken: token de acceso (obtenido de db_auth_local de skycds)
7. interval: tiempo de sensado en segundos



### moguel_download.py configuration

```bash
python moguel_download.py 7b22d86e036b1bb4caf350d4bc2de4e40009159496e0a10c03a318e39e3f6ad0 c81ffa68bd5ac4d8c0c915c95f5a56305b435d0e 7c0c7ebfd042edfc3515ba8e85514ac647be7c0caa74cdc22a194da45abe1283 /home/fernando/Escritorio/skyCDS_Junio/Salida MOGUI f0578b9cfec53e3af56e1f809e0802e8f3a5c487b7b7a0d9d374e17978c7ae95 30 148.247.201.227
```



Params:
1. tokenuser: token de usuario (obtenido de db_auth_local de skycds)
2. apikey: llave de api (obtenido de db_auth_local de skycds)
3. catalogToken:token de catalogo (obtenido de db_pub_sub_local de skycds)
4. chunk_path: ruta de la carpeta a sensar
5. organization: organización de skycds ((obtenido de db_auth_local de skycds))
6. accessToken: token de acceso (obtenido de db_auth_local de skycds)
7. interval: tiempo de sensado en segundos
8. ip = ip del servidor que tiene skycds sin puerto

