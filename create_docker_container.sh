docker run -d \
--name bo-container \
# Expongo el puerto 8080 del host al 8501 del contenedor, que es donde corre streamlit
-p 8080:8501 \
# Hay que asegurarse de que exista el volumen bo-container
-v bo-volume:/app/data \
# Hay que asegurarse que exista la imagen back-order-app:v1.0
back-order-app:v1.0