#Hyperledger

* Se requiere levantar los servicios de la red de verificabilidad, para ello se debe ingresar a la carpeta Hyperledger>>image-network y ejecutar el comando ./network.sh up.


#Cadenas de valor
Para crear las cadenas de valor es necesario ingresar a la carpeta producer la cual contiene el código necesario para la gestión de estas estructuras de procesamiento.

Se debe configurar el archivo general_configuration.cfg para tener cada uno de los elementos de cada cadena y habilitar los archivos de ficheros de cada una de las etapas contempladas.


Cabe destacar que se deben configurar las ips de la red de verificabilidad para una comunicación exitosa dentro de los gestores de bloques de construcción y de cadenas de suministros.

Por otro lado se debe agregar el código necesario del aplicativo en cada una de las etapas de las cadenas, esto dentro de cada uno de los bloques de construcción inmersos (Dentro de la carpeta DISCH) de cada BB.
