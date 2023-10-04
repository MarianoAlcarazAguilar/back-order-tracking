#! /bin/bash

# Creamos volumen para los datos solo si este no existe
VOLUME_NAME="bo-data"

# Comprobar si el volumen ya existe
if docker volume ls -q | grep -q "$VOLUME_NAME"; then
    echo "El volumen $VOLUME_NAME ya existe."
else
    # Crear el volumen si no existe
    docker volume create "$VOLUME_NAME"
    echo "El volumen $VOLUME_NAME ha sido creado."
fi

docker run -d \
-v bo-data:/app/data \
--name bo-container \
-p 80:8501 \
bo-image:v1