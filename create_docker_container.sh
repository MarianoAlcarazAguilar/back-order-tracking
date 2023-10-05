#! /bin/bash

# Creamos volumen para los datos solo si este no existe
VOLUME_NAME="bo-data"
IMAGE_NAME="bo-image:latest"
CONTAINER_NAME="bo-container"

# Verificar si la imagen ya existe
if docker image ls -q "$IMAGE_NAME" | grep -q .; then
    echo "La imagen $IMAGE_NAME ya existe."
else
    # Construir la imagen si no existe
    docker build -t "$IMAGE_NAME" .
    echo "La imagen $IMAGE_NAME ha sido creada."
fi

# Comprobar si el volumen ya existe
if docker volume ls -q | grep -q "$VOLUME_NAME"; then
    echo "El volumen $VOLUME_NAME ya existe."
else
    # Crear el volumen si no existe
    docker volume create "$VOLUME_NAME"
    echo "El volumen $VOLUME_NAME ha sido creado."
fi

# Verificar si el contenedor ya existe
if docker ps -a --format '{{.Names}}' | grep -q "$CONTAINER_NAME"; then
    echo "El contenedor $CONTAINER_NAME ya existe."
else
    # Crear el contenedor si no existe
    docker run -d \
    -v bo-data:/app/data \
    --name bo-container \
    -p 80:8501 \
    bo-image:latest
    echo "El contenedor $CONTAINER_NAME ha sido creado."
fi

# Iniciar el contenedor si no está en ejecución
if ! docker ps -q --filter "name=$CONTAINER_NAME"; then
    docker start "$CONTAINER_NAME"
    echo "El contenedor $CONTAINER_NAME ha sido iniciado."
fi