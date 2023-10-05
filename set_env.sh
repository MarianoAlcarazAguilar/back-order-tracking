#!/bin/bash

# Verificar y crear las carpetas si no existen
carpetas=("data/raw_data/transferencias" "data/raw_data/inventarios" "data/raw_data/forecasts" "data/transformed_data/back_orders" "data/transformed_data/forecasts" "data/transformed_data/inventarios" "data/transformed_data/transferencias")

for carpeta in "${carpetas[@]}"; do
  if [ ! -d "$carpeta" ]; then
    echo "Creando carpeta: $carpeta"
    mkdir -p "$carpeta"
  else
    echo "La carpeta ya existe: $carpeta"
  fi
done

#pip install -r requirements.txt
