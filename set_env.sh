#!/bin/bash

# Verificar y crear las carpetas si no existen

carpetas=("raw_data/transferencias" "raw_data/inventarios" "raw_data/forecasts" "transformed_data/back_orders" "transformed_data/forecasts" "transformed_data/inventarios" "transformed_data/transferencias")

for carpeta in "${carpetas[@]}"; do
  if [ ! -d "$carpeta" ]; then
    echo "Creando carpeta: $carpeta"
    mkdir -p "$carpeta"
  else
    echo "La carpeta ya existe: $carpeta"
  fi
done

pip install -r requirements.txt